# XJTLU Music Evolution and Social Interactions

本科数学建模项目，研究音乐风格影响网络、音频特征变化与社会环境的关联。完整的 2021 ICM Problem D 报告、团队信息与 MATLAB 附录见 [研究报告](report.pdf)。

## 研究路线

1. 用艺术家/风格有向关系描述局部影响，以 PageRank 计算全局影响。
2. 对音频特征标准化与 PCA 降维，再以 KMeans 和模拟退火探索聚类。
3. 用 FTTO 思路研究特征、流行度与作品数量的时间转折，并讨论社会事件背景。

报告中的社会环境讨论属于关联分析，不将时间上的共同变化解释为已识别的因果效应。

## 可运行部分

[music_analysis.py](music_analysis.py) 是依据报告公式与附录整理的 Python 数值实现：

| 函数 | 输入与行为 |
| --- | --- |
| `pagerank` | 方阵 `weights[target, source]`，按列归一化；默认阻尼 0.85；空出边列均匀分配，明确补足边界约定 |
| `pca_features` | 每行一条音乐观测、每列一个数值音频特征；先标准化再 PCA，默认保留 7 个分量，返回得分与已拟合变换器 |
| `annealed_kmeans` | 在 PCA 得分空间扰动中心并重新拟合，依据候选解损失决定接受与否，独立保留历史最优解，固定种子便于复查 |

修正了附录模拟退火代码对旧解再次计算损失、无法正确比较候选解的问题。附录未提供 `change`、`MSE` 等辅助函数，因此当前中心扰动是明确的新实现，并不声称与当时 MATLAB 的随机搜索路径等价。

## 运行

在本目录、已激活的 Python 环境中运行：

```sh
python -m pip install -r requirements.txt
python music_analysis.py --demo
python -m unittest -v
```

`--demo` 生成标记为 `synthetic: true` 的合成数据，只检验计算路线。输出含 PCA 方差解释率、最优聚类损失轨迹、簇大小和一个小图的 PageRank。测试检查 PageRank 方程与概率和、标准化、最优损失保留和固定种子的可重复性。

自有数值特征 CSV 须有一行表头，无空值、文本、ID 或年份列：

```sh
python music_analysis.py --features audio_features.csv --components 7 --clusters 5 --steps 20
```

分量数不得超过样本数与特征数中的较小值；聚类数不得超过样本数。年份应作为独立时间索引，不混入音频特征标准化。库函数返回的 scaler/PCA 可用于同一分析的后续变换，避免重新拟合造成坐标不一致。

## 完整度与复现边界

报告保留全部研究叙述。真实的 `full_data.csv`、`DATA3.xlsx`、按年特征表和完整影响网络尚未恢复。FTTO 的辅助函数与完整数据处理链也不齐全，因此没有用替代公式冒充该部分的复现。当前可验证 PageRank、PCA 与聚类核心实现；不能据合成演示声称复现报告中的音乐排名、历史拐点或实验图表。

已在 Python 3.13、NumPy 2.5、scikit-learn 1.9 环境执行核心测试。依赖按实际导入列出，不将其视为历史研究环境的版本锁定。
