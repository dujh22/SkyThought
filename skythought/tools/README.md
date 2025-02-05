# 数据生成和评估工具

本文档描述了 Sky-T1 的训练数据整理和评估脚本的步骤。

## 要求

首先按如下方式创建环境。

```shell
conda create -n eval python==3.10
conda activate eval 
pip install -r requirements.txt
```

要运行 OpenAI 模型，请导出 OpenAI 密钥。

```shell
export OPENAI_API_KEY={openai_api_key}
```

## 训练数据整理

### 步骤 0（可选，仅适用于 NUMINA 数学数据集）：标记 NUMINA 的数学难度

将一个或多个 OPENAI_API_KEY 放在一个文件中，例如 keys.txt（每行一个）。如果有多个密钥，脚本将以循环方式使用它们以加快生成速度。使用 GPT-4o-mini 标记数学难度：

#### 示例用法：

```
python label_math_difficulty.py --source [amc_aime, math, olympiads] --keys keys.txt
```

预期输出为 labeled_source_0_-1.json。我们还提供了在 labeled_numina_difficulty 文件夹下下载这些文件的说明（从 HuggingFace 下载）。

### 步骤 1：数据推理

在多个数据集上推理 QwQ 的结果。在预览版本中，我们使用以下数据集的数据。

```shell
python inference_and_check.py --dataset APPS --model Qwen/QwQ-32B-Preview --tp 8 --max_tokens 16384 --split test --source all --result-dir $SKYT_HOME/data --inference

python inference_and_check.py --dataset TACO --model Qwen/QwQ-32B-Preview --tp 8 --max_tokens 16384 --split train --source MEDIUM --filter-difficulty --result-dir $SKYT_HOME/data --inference

python inference_and_check.py --dataset TACO --model Qwen/QwQ-32B-Preview --tp 8 --max_tokens 16384 --split test --source all --result-dir $SKYT_HOME/data --inference

python inference_and_check.py --dataset NUMINA --model Qwen/QwQ-32B-Preview --tp 8 --max_tokens 16384 --split train --source math --filter-difficulty --result-dir $SKYT_HOME/data --inference

python inference_and_check.py --dataset NUMINA --model Qwen/QwQ-32B-Preview --tp 8 --max_tokens 16384 --split train --source amc_aime --filter-difficulty --result-dir $SKYT_HOME/data --inference

python inference_and_check.py --dataset NUMINA --model Qwen/QwQ-32B-Preview --tp 8 --max_tokens 16384 --split train --source olympiads --end 20000 --filter-difficulty --result-dir $SKYT_HOME/data --inference
```

### 步骤 2：格式化响应

在获得训练数据的列表文件后，将其转换为统一格式（注意：这使用 GPT-4o-mini 重写。输出很长，我们的预览数据大约需要 100 美元）。

```shell
python convert_format.py --input_dir $SKYT_HOME/data --keys keys.txt
```

### 步骤 3：对格式化数据进行拒绝采样（使用前面脚本的示例用法）

```shell
python inference_and_check.py --dataset APPS --model Qwen/QwQ-32B-Preview --tp 8 --max_tokens 16384 --split test --source all --result-dir $SKYT_HOME/data --check
```

其他数据集类似。

### 转换为 ShareGPT 格式进行训练

在获得多个转换文件后，将它们合并在一起并转换为 ShareGPT 格式以进行训练。在我们的预览模型中，我们还添加了 [STILL-2 模型](https://arxiv.org/pdf/2412.09413) 中的科学和谜题部分，感兴趣的读者可以下载他们的数据部分并简单地连接到上面获得的数据。

```shell
python convert_to_data.py --input_dir $SKYT_HOME/data --output $SKYT_HOME/data/train_data.json
```

## 生成和评估

文件 `inference_and_check.py` 提供了生成序列（例如，用于蒸馏或基准评估）和检查生成的解决方案是否正确（例如，用于拒绝采样或基准评估）的便捷方法。

### 蒸馏和拒绝采样

目前我们支持从各种自托管模型对 NUMINA、APPS 和 TACO 数据集进行蒸馏和拒绝采样。对于 NUMINA，来源可以是 `[amc_aime, math, olympiads]` 中的一个。

#### 示例用法

```shell
python inference_and_check.py --dataset APPS --model Qwen/QwQ-32B-Preview --tp 8 --max_tokens 16384 --split test --source all --result-dir $SKYT_HOME/data

python inference_and_check.py --dataset TACO --model Qwen/QwQ-32B-Preview --tp 8 --max_tokens 16384 --split train --source MEDIUM --filter-difficulty --result-dir $SKYT_HOME/data

python inference_and_check.py --dataset TACO --model Qwen/QwQ-32B-Preview --tp 8 --max_tokens 16384 --split test --source all --result-dir $SKYT_HOME/data

python inference_and_check.py --dataset NUMINA --model Qwen/QwQ-32B-Preview --tp 8 --max_tokens 16384 --split train --source math --filter-difficulty --result-dir $SKYT_HOME/data --math_difficulty_lower_bound 4 --math_difficulty_lower_bound 9

python inference_and_check.py --dataset NUMINA --model Qwen/QwQ-32B-Preview --tp 8 --max_tokens 16384 --split train --source amc_aime --filter-difficulty --result-dir $SKYT_HOME/data --math_difficulty_lower_bound 1 --math_difficulty_lower_bound 9

python inference_and_check.py --dataset NUMINA --model Qwen/QwQ-32B-Preview --tp 8 --max_tokens 16384 --split train --source olympiads --end 20000 --filter-difficulty --result-dir $SKYT_HOME/data --math_difficulty_lower_bound 9 --math_difficulty_lower_bound 9
```

#### TODO

添加 Best-of-N 采样。

### 基准评估

我们提供了一个包装脚本 `eval.py` 来方便地运行推理基准测试。我们目前支持 `AIME`、`MATH500`、`GPQADiamond` 和 `MMLU`。此脚本可用于启动多个基准测试的评估，然后汇总并记录所有基准测试的准确性。

**注意**：`GPQADiamond` 数据集是受限的，需要首先在此 Huggingface [链接](https://huggingface.co/datasets/Idavidrein/gpqa) 上获得访问权限（立即授予），然后在终端会话中使用 `huggingface-cli login` 登录到你的 Huggingface 账户。

#### 示例用法

```shell
python eval.py --model Qwen/QwQ-32B-Preview --evals=AIME,MATH500,GPQADiamond --tp=8 --output_file=results.txt
```

示例结果：`{"AIME": <aime_accuracy>, "MATH500": <math500_accuracy>, "GPQADiamond": <gpqa_diamond_accuracy>}`

⚠️：如果是加载本地模型路径，需要同时修改补充：skythought/tools/util/model_utils.py中
