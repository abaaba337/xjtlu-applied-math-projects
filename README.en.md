# XJTLU Applied Mathematics Projects

<p><a href="README.md"><kbd>简体中文</kbd></a> &nbsp; <a href="README.en.md"><kbd><strong>English ✓</strong></kbd></a></p>

Undergraduate research, mathematical modelling, and computational experiments at Xi'an Jiaotong-Liverpool University. Four projects organise their own code, reports, and execution guides, distinguishing learning materials, subsequent code reconstruction, and validated results.

| Project | Research topics | Start here |
| --- | --- | --- |
| [XJTLU-CMIT-Deep-Learning-and-Mathematical-Imaging](XJTLU-CMIT-Deep-Learning-and-Mathematical-Imaging/) | Centre for Mathematical Imaging Techniques: neural networks, image segmentation and denoising exercises, and a report on small switching components in discrete tomography | [Course and experiment guide](XJTLU-CMIT-Deep-Learning-and-Mathematical-Imaging/README.md) |
| [XJTLU-COVID-Tweet-Analysis](XJTLU-COVID-Tweet-Analysis/) | COVID tweets, news topics, public attention, and US county-level mobility indicators | [Workflow for the nine notebooks](XJTLU-COVID-Tweet-Analysis/README.md) |
| [XJTLU-Circuit-Board-Layout-Optimisation](XJTLU-Circuit-Board-Layout-Optimisation/) | Circuit board allocation under crossing and turning constraints, intersection matrices, and greedy algorithms | [Report, algorithm, and three cases](XJTLU-Circuit-Board-Layout-Optimisation/README.md) |
| [XJTLU-Music-Evolution-and-Social-Interactions](XJTLU-Music-Evolution-and-Social-Interactions/) | Musical influence networks, audio feature dimensionality reduction, clustering, and associations with the social environment | [Report and numerical experiments](XJTLU-Music-Evolution-and-Social-Interactions/README.md) |

## Running and validating

Enter the selected project and follow its README to install dependencies and prepare data. There is no single application entry point covering all four projects. Running them independently avoids conflicts between teaching modules with identical names and different experimental environments.

| Project | Minimal checks from the project directory | Data availability |
| --- | --- | --- |
| CMIT | `python -m unittest -v` | Stock examples, teaching images, and some weights are included; prepare DRIVE, MNIST, and other datasets as documented |
| COVID | `python -m pytest -q` | Key raw and intermediate datasets are still missing; checks do not constitute reproduction on real data |
| Circuit Board | `python -m unittest -v`; `python board_layout.py` | The report's three ten-route matrix cases can be recomputed directly |
| Music | `python -m unittest -v`; `python music_analysis.py --demo` | The demo uses synthetic data; real music datasets and some helper functions are missing |

The September 2026 validation covers data splits, paths, image masks, model compatibility, TF-IDF, FIPS codes, policy completion, dynamic topic time alignment, board allocation constraints, and PageRank/PCA/clustering. The competition Python implementations are runnable reconstructions based on the reports, not the complete code environments used when the reports were written. Research conclusions remain subject to the reports and their data requirements.

## Maintenance

Read [AGENTS.md](AGENTS.md) before making changes. [CLAUDE.md](CLAUDE.md) references the same rules through `@AGENTS.md`. Report authors, team information, course materials, and existing citations are retained; no new licence is granted for third-party data, slides, or code.
