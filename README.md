# XJTLU Applied Mathematics Projects

<details name="readme-language">
<summary><strong>English</strong></summary>

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

</details>

<details name="readme-language" open>
<summary><strong>简体中文</strong></summary>

西交利物浦大学本科阶段的科研、数学建模与计算实验。四个项目分别组织代码、报告和运行说明，学习材料、后续代码整理与已验证结果在各项目中明确区分。

| 项目 | 研究内容 | 从这里开始 |
| --- | --- | --- |
| [XJTLU-CMIT-Deep-Learning-and-Mathematical-Imaging](XJTLU-CMIT-Deep-Learning-and-Mathematical-Imaging/) | Centre for Mathematical Imaging Techniques：神经网络、图像分割与去噪课程实验；离散层析的小切换分量研究报告 | [课程与实验路线](XJTLU-CMIT-Deep-Learning-and-Mathematical-Imaging/README.md) |
| [XJTLU-COVID-Tweet-Analysis](XJTLU-COVID-Tweet-Analysis/) | COVID 推文、新闻主题、公众关注度与美国县级出行指标 | [九本笔记本的运行顺序](XJTLU-COVID-Tweet-Analysis/README.md) |
| [XJTLU-Circuit-Board-Layout-Optimisation](XJTLU-Circuit-Board-Layout-Optimisation/) | 带交叉与转折约束的电路板布线分配，排斥矩阵与贪心算法 | [报告、算法与三组算例](XJTLU-Circuit-Board-Layout-Optimisation/README.md) |
| [XJTLU-Music-Evolution-and-Social-Interactions](XJTLU-Music-Evolution-and-Social-Interactions/) | 音乐影响网络、音频特征降维、聚类与社会环境关联 | [报告与数值实验](XJTLU-Music-Evolution-and-Social-Interactions/README.md) |

## 运行与验证

进入具体项目，按其 README 安装依赖和准备数据。没有覆盖四个项目的统一业务入口；独立运行可以避免同名教学模块和不同实验环境相互干扰。

| 项目 | 本项目目录下的最小检查 | 数据状态 |
| --- | --- | --- |
| CMIT | `python -m unittest -v` | 股票示例、教学图像及部分权重已包含；DRIVE、MNIST 等需按说明准备 |
| COVID | `python -m pytest -q` | 关键原始与中间数据仍缺失，检查不等于真实数据复现 |
| Circuit Board | `python -m unittest -v`；`python board_layout.py` | 报告中的三组十线路矩阵可直接复算 |
| Music | `python -m unittest -v`；`python music_analysis.py --demo` | 演示使用合成数据；真实音乐数据与部分辅助函数缺失 |

2026-09 整理验证覆盖数据划分、路径、图像掩码、模型兼容性、TF-IDF、FIPS、政策补全、动态主题时间对齐、分板约束及 PageRank/PCA/聚类。竞赛 Python 代码是依据报告整理的可运行复现，不代表报告写作时的完整代码环境。科研结论以报告及其数据条件为准。

## 维护

修改前阅读 [AGENTS.md](AGENTS.md)。[CLAUDE.md](CLAUDE.md) 通过 `@AGENTS.md` 引用同一份规则。保留报告作者、团队信息、课程材料和已有引用；没有给第三方数据、课件或代码新增统一授权。

</details>
