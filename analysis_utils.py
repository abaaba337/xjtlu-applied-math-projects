"""Shared numerical routines used by the research notebooks."""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


def track_tfidf(df, cal_window=7, min_df=0.0, max_df=1.0):
    """Rolling document-window TF-IDF; missing vocabularies remain NaN.

    A window counts observations, not calendar days. A missing day is not
    silently treated as a document. Average only over that window's terms.
    """
    if not isinstance(cal_window, int) or cal_window == 0 or cal_window < -1:
        raise ValueError("cal_window must be a positive integer or -1")
    if not df.index.is_unique or not df.index.is_monotonic_increasing:
        raise ValueError("Document dates must be unique and sorted")
    if df.shape[1] != 1:
        raise ValueError("Expected one text column")
    texts = df.iloc[:, 0].fillna("").tolist()
    vectorizer = TfidfVectorizer(min_df=0.0 if min_df == 0 else min_df, max_df=max_df)
    analyzer = vectorizer.build_analyzer()
    rows = []
    for i in range(len(texts)):
        start = 0 if cal_window == -1 else max(0, i - cal_window + 1)
        window = texts[start:i + 1]
        if not any(analyzer(text) for text in window):
            rows.append({})
            continue
        matrix = vectorizer.fit_transform(window)
        rows.append(dict(zip(vectorizer.get_feature_names_out(),
                             matrix[-1].toarray().ravel())))
    scores = pd.DataFrame(rows, index=df.index, dtype=float)
    return scores, scores.mean(axis=1).to_frame("TF-IDF")


def formalize_fip(value):
    """Preserve state (2 digits) and county (5 digits) identifiers."""
    if pd.isna(value):
        return np.nan
    number = float(value)
    if not np.isfinite(number) or not number.is_integer() or not 0 < number <= 99999:
        raise ValueError(f"Invalid FIPS identifier: {value!r}")
    width = 5 if isinstance(value, str) and len(value.strip()) == 5 else (2 if number < 100 else 5)
    return str(int(number)).zfill(width)


def transform_mobilitydata(mob_df, mob_feature_col="dtspp",
                          start_day="2020-03-01", end_day="2020-09-01"):
    """County/date pivot with the experiment's five-day interpolation limit."""
    data = mob_df[["fips", "date", mob_feature_col]].copy()
    data["date"] = pd.to_datetime(data["date"], errors="raise")
    data["fips"] = data["fips"].map(formalize_fip)
    if data[["fips", "date"]].isna().any().any():
        raise ValueError("Mobility keys must not be missing")
    if data.duplicated(["fips", "date"]).any():
        raise ValueError("Duplicate county/date mobility observations")
    index = pd.date_range(start_day, end_day)
    if index.empty:
        raise ValueError("start_day must not follow end_day")
    data = data[data.date.between(index[0], index[-1])]
    result = data.pivot(index="date", columns="fips", values=mob_feature_col)
    result = result.reindex(index).interpolate(limit=5, limit_direction="forward")
    return result.add_prefix(mob_feature_col + "_")


def prepare_dtm(docs, corpuses, dates):
    """Remove empty bags by position and keep documents/time slices aligned."""
    dates = pd.to_datetime(dates, errors="raise")
    if dates.isna().any() or not dates.is_monotonic_increasing:
        raise ValueError("DTM dates must be present and sorted")
    if len(docs) != len(corpuses):
        raise ValueError("Document and corpus groups must align")
    new_docs, new_corpuses, time_slices, day_lists = [], [], [], []
    for texts, bags in zip(docs, corpuses):
        if len(texts) != len(dates) or len(bags) != len(dates):
            raise ValueError("Documents, bags, and dates must align")
        keep = [i for i, bag in enumerate(bags) if len(bag)]
        if not keep:
            raise ValueError("No non-empty documents remain for DTM")
        days = dates.take(keep)
        new_docs.append([texts[i] for i in keep])
        new_corpuses.append([bags[i] for i in keep])
        time_slices.append(pd.Series(days).value_counts(sort=False).tolist())
        day_lists.append(days.tolist())
    return new_docs, new_corpuses, time_slices, day_lists
