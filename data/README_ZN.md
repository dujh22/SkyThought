# 下载数据集
以下是下载用于训练 Sky-T1-32B-Preview 模型的 17k 数据集的说明。

## HuggingFace
数据集可在 [HuggingFace](https://huggingface.co/datasets/NovaSky-AI/Sky-T1_data_17k) 上获取。下载方法如下：
```python
from datasets import load_dataset
ds = load_dataset("NovaSky-AI/Sky-T1_data_17k")
```