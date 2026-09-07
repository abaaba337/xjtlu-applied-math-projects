# XJTLU CMIT Deep Learning and Mathematical Imaging

Centre for Mathematical Imaging Techniques（CMIT）课程与科研资料，包含神经网络基础、循环网络、图像分割、去噪实验，以及离散层析中的小切换分量研究。

## 内容与运行路线

| 内容 | 入口 | 说明 |
| --- | --- | --- |
| 课程讲义与实验 | [CMIT Lecture Notes.ipynb](Notes/CMIT%20Lecture%20Notes.ipynb) | 数值计算、神经网络、股票序列、CNN、U-Net、图像去噪；图片位于相邻主题目录 |
| 练习 | [Exercise.ipynb](Exercise/Exercise.ipynb) | 数值与图像练习、分类和分割 |
| PyTorch 教学 | [Lec3_torch.ipynb](PPT/Lec3_torch.ipynb) | 配合 `PPT/` 下的课件 |
| 独立循环网络示例 | [train.py](Notes/Notes_RNN/StockPrediction243/GatedUnitsInRNN-main/train.py) | 随附股票 CSV，可直接进行小规模训练 |
| CMIT Project B | [Small Switching Components 报告](CMIT%20partII%20final%20report.pdf) | 从启发式搜索到机器学习，研究离散层析的方向向量与多项式系数绝对值之和；保留作者与引用 |

Project B 的完整搜索与强化学习代码没有随附，报告内容不等同于神经网络课程示例的实验结果。

## 环境与入口

在本项目目录中创建并激活 Python 环境，再运行：

```sh
python -m pip install -r requirements.txt
python -m unittest -v
python Notes/Notes_RNN/StockPrediction243/GatedUnitsInRNN-main/train.py --epochs 2 --max-rows 48
jupyter lab
```

每本笔记本先运行新增的路径单元，再按章节运行相应导入、数据准备、模型、训练和评估单元。课程多处重用 `CNN`、`CustomDataset`、`train` 等教学名称，切换章节时重启内核并重新执行该节前置单元。全本运行会触发下载及长时间训练，不作为最小验证方式。

独立股票训练入口根据脚本位置寻找 `data/stock.csv`，无需切换到脚本目录。`--data` 可指定自己的同字段 CSV；`--max-rows` 仅用于快速检查，省略即使用全量数据。训练默认不写文件；需要保存时传 `--output results/stock-model.pt`，已有目标文件会被拒绝覆盖。随附旧 checkpoint 保留，但不会自动加载为新训练的初始状态。

## 数据与模型

- 股票 CSV、教学图像及部分 `.pth` 权重已包含；MNIST/FashionMNIST 由相关单元首次下载。
- DRIVE 血管分割数据需另行准备。设置 `CMIT_DRIVE_DIR`，或放在 `Notes/Notes_IMProcess/DRIVE/`。目录需含 `training/images/21_training.tif` 至 `40_training.tif`、对应 `training/1st_manual/21_manual1.gif` 等，以及 `test/images/01_test.tif` 至 `20_test.tif` 和对应人工掩码。加载器兼容无前导零的编号与 PNG 图像，缺失或重复候选会报错。
- 保留课程提供的 [DRIVE 材料链接](https://drive.google.com/file/d/1IZ_1ZcJUAzZyjDHpuN2KUkcfJ23lhTl9/view?usp=sharing) 与 [课程材料链接](https://1drv.ms/u/s!ArOH3MAbgkX8ga8O_9cmPvYUD1dbVg?e=jYSmRz)；未验证其当前可访问性。
- `Notes323CNN.pth` 与 `Notes332Denoising.pth` 已验证与对应模型结构匹配，读取使用 `weights_only=True` 与 CPU 映射。U-Net 权重没有随附，比较图使用前面实际训练的 `Unet_model`；不能跳过训练再生成所谓训练结果。
- 教学单元中的保存操作可能更新随附文件；复现实验时将输出改到 `results/` 或使用独立工作副本。旧 `.pkl` 仅作保留材料，优先使用受限的 state-dict 读取方式。

## 整理与验证

修正股票脚本返回整份数据作为训练集造成的测试泄漏；缩放器仅拟合训练段，按时间顺序划分。训练增加截断反向传播、逐轮状态重置与无梯度评估，学习率调度周期改为训练轮数。保留自定义门控单元的教学公式，未将其替换为另一种网络。

股票笔记本同样只用训练窗口涉及的行拟合标准化器，逆变换使用同一缩放器；修复 batch size 为 1 时维度消失。两个分割笔记本共用 [cmit_utils.py](cmit_utils.py)，图像使用双线性插值，二值掩码使用最近邻插值，并检查图像与标注配对。

回归检查覆盖实际股票数据的分割、两轮小样本训练、评估状态隔离、浮点类型、掩码边界、DRIVE 文件名、笔记本中的标准化单元与 LSTM 单样本输出，以及随附 CNN/去噪权重兼容性。测试环境为 Python 3.13、PyTorch 2.14 CPU、torchvision 0.29、NumPy 2.5、pandas 3.0、scikit-learn 1.9。

没有运行完整 DRIVE 训练、全部课程笔记本或 Project B 的历史搜索实验；缺失数据和历史环境仍限制完整科研复现。笔记本执行输出已清除，避免将旧输出误认作本次验证结果。
