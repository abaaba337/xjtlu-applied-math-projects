import ast
import json
from pathlib import Path

import nbformat
import numpy as np
import pandas as pd
import pytest
from IPython.core.inputtransformer2 import TransformerManager
from sklearn.feature_extraction.text import TfidfVectorizer

from analysis_utils import formalize_fip, prepare_dtm, track_tfidf, transform_mobilitydata
import project_paths

ROOT = Path(__file__).resolve().parents[1]


def notebook(path):
    return json.loads((ROOT / 'notebooks' / path).read_text(encoding='utf-8'))


def test_notebooks_are_portable_and_parseable():
    paths = list((ROOT / 'notebooks').rglob('*.ipynb'))
    assert len(paths) == 9
    for path in paths:
        nb = nbformat.read(path, as_version=4)
        nbformat.validate(nb)
        for cell in nb.cells:
            assert 'D:/Python_project/' not in cell.source
            if cell.cell_type == 'code':
                assert cell.outputs == [] and cell.execution_count is None
                ast.parse(TransformerManager().transform_cell(cell.source))


def test_tfidf_keeps_repeated_terms_and_uses_correct_window():
    df = pd.DataFrame({'text': ['vaccine health', 'vaccine school', 'school open']},
                      index=pd.date_range('2020-01-01', periods=3))
    scores, average = track_tfidf(df, cal_window=2)
    vectorizer = TfidfVectorizer()
    expected = vectorizer.fit_transform(df.text.iloc[1:])[-1].toarray().ravel()
    np.testing.assert_allclose(scores.iloc[-1][vectorizer.get_feature_names_out()], expected)
    assert scores.loc[df.index[1], 'vaccine'] > 0
    assert np.isnan(scores.loc[df.index[-1], 'health'])
    assert average.iloc[-1, 0] == pytest.approx(expected.mean())
    empty = pd.DataFrame({'text': ['', None]}, index=[0, 1])
    assert track_tfidf(empty)[1].isna().all().all()
    with pytest.raises(ValueError, match='unique and sorted'):
        track_tfidf(df.iloc[::-1])
    with pytest.raises(ValueError, match='positive integer'):
        track_tfidf(df, cal_window=0)


def test_mobility_preserves_fips_and_rejects_duplicate_keys():
    assert formalize_fip('01001') == '01001'
    assert formalize_fip(1001.0) == '01001'
    assert formalize_fip('02') == '02'
    with pytest.raises(ValueError):
        formalize_fip(1001.5)
    df = pd.DataFrame({'fips': [1001, 1001], 'date': ['2020-01-01', '2020-01-03'],
                       'dtspp': [1.0, 3.0]})
    result = transform_mobilitydata(df, start_day='2020-01-01', end_day='2020-01-03')
    assert result['dtspp_01001'].tolist() == [1.0, 2.0, 3.0]
    with pytest.raises(ValueError, match='Duplicate'):
        transform_mobilitydata(pd.concat([df, df]))


def test_dtm_alignment_with_duplicate_text_and_empty_bags():
    docs = [[['same'], ['same'], ['third'], ['fourth']]]
    bags = [[[], [(0, 1)], [(1, 1)], [(1, 2)]]]
    dates = pd.Series(['2020-01-01', '2020-01-02', '2020-01-02', '2020-01-03'])
    cleaned, corpus, slices, days = prepare_dtm(docs, bags, dates)
    assert cleaned[0] == [['same'], ['third'], ['fourth']]
    assert corpus[0] == bags[0][1:]
    assert slices == [[2, 1]] and len(days[0]) == 3
    # No empty documents must still produce valid time slices.
    assert prepare_dtm([docs[0][1:]], [bags[0][1:]], dates.iloc[1:])[2] == [[2, 1]]
    with pytest.raises(ValueError, match='sorted'):
        prepare_dtm(docs, bags, dates.iloc[::-1])


def test_tweet_pos_columns_are_not_overwritten(tmp_path, monkeypatch):
    nb = notebook('tweets/01-cleaning.ipynb')
    source = next(''.join(c['source']) for c in nb['cells']
                  if ''.join(c['source']).startswith('# Extra Filter'))
    monkeypatch.chdir(tmp_path)
    data = pd.DataFrame({'cleaned_text': ['health strong run'],
                         'cleaned_text_verb_noun': ['health run'],
                         'cleaned_text_noun': ['health']})
    ns = {'tw_pitt': data, 'filter_words2': lambda text: text}
    exec(source, ns)
    assert data.cleaned_text_verb_noun.iloc[0] == 'health run'
    assert data.cleaned_text_noun.iloc[0] == 'health'


def test_policy_fill_preserves_observed_local_dates():
    nb = notebook('mobility/03-combined-indicators.ipynb')
    source = next(''.join(c['source']) for c in nb['cells']
                  if ''.join(c['source']).startswith('# Fill only missing local dates'))
    pairs = [('localsipstart', 'stsipstart'), ('localsipend', 'stsipend'),
             ('localbusclose', 'stbusclose'), ('localbusopen', 'stbusopen'),
             ('localresclose', 'stresclose'), ('localresopen', 'stresopen')]
    data = {key: ['2020-03-03', None] for key, _ in pairs}
    data.update({key: ['2020-03-01', '2020-03-02'] for _, key in pairs})
    ns = {'poly': pd.DataFrame(data)}
    exec(source, ns)
    for local, _ in pairs:
        assert ns['poly'][local].tolist() == ['2020-03-03', '2020-03-02']


def test_workspaces_are_independent_and_do_not_create_inputs(tmp_path, monkeypatch):
    monkeypatch.setattr(project_paths, 'DATA', tmp_path)
    tweets = Path(project_paths.workspace('tweets'))
    news = Path(project_paths.workspace('news'))
    assert tweets != news and (news / 'Data/CBS_KDKA/LDA/Title').is_dir()
    assert not (tweets / 'stopwords_en.txt').exists()
    with pytest.raises(ValueError, match='Unknown workspace'):
        project_paths.workspace('../outside')
