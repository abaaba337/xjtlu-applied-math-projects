"""Portable data workspaces and an offline input inventory."""

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = Path(os.environ.get("COVID_DATA_DIR", ROOT / "data")).expanduser().resolve()

INPUTS = {
    "tweets": ["Copy of Copy of Coronavirus [EN] [Scaled x4] [Pittsburgh].csv",
               "stopwords_en.txt", "extra_stopwords_en.txt"],
    "news": ["cbs_Pittsburgh.csv", "stopwords_en.txt", "stopwords_html.txt",
             "stopwords_punctuation.txt"],
    "national-news": ["covid-news-en-us-clean-keyonly.csv",
                      "stopwords_en.txt", "extra_stopwords_en.txt"],
    "mobility": ["Delta TSPP/DTSPP_US_Mobility_formalized.csv",
                 "Google/Google_US_Mobility_formalized.csv",
                 "Descartes Labs/DL_US_Mobility_formalized.csv",
                 "Facebook/Facebook_US_Mobility_formalized.csv",
                 "Gov/Gov_US_Mobility_formalized.csv",
                 "Policy/Chicago/Local-Policy-Responses-formalized.csv",
                 "Local-Policy-Responses-formalized-matched-localonly.csv",
                 "matched-us-covidcase-counties-2020.csv"],
    "mobility/trends": ["google-trends-locations.json", "google-trend-geocode2metro.csv",
                        "county-msa-csa.csv"],
}


def workspace(section):
    """Resolve only a known workspace; create output folders, never fake inputs."""
    if section not in INPUTS:
        raise ValueError(f"Unknown workspace: {section}")
    path = DATA / section
    path.mkdir(parents=True, exist_ok=True)
    (path / "result").mkdir(exist_ok=True)
    (path / "plot").mkdir(exist_ok=True)
    if section == "news":
        for directory in ["TFIDF", "LDA/Title", "LDA/Keyword", "LDA/Content",
                          "LDA/KeywordAndTitle", *(f"LDA_KLD/Doc{i}" for i in range(1, 5))]:
            (path / "Data/CBS_KDKA" / directory).mkdir(parents=True, exist_ok=True)
        (path / "Plot/CBS_KDKA").mkdir(parents=True, exist_ok=True)
    return str(path) + os.sep


if __name__ == "__main__":
    missing = []
    for section, names in INPUTS.items():
        for name in names:
            path = DATA / section / name
            exists = path.is_file()
            print(f"{'OK' if exists else 'MISSING'}: {path}")
            if not exists:
                missing.append(path)
    print(f"{len(missing)} missing external inputs; see data/README.md for generated artifacts.")
    raise SystemExit(bool(missing))
