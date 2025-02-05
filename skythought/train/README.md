## 训练

我们使用 [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) 的一个分支进行训练。

### 步骤0

可进一步参照LLaMA-Factory/Readme完成相关运行环境的配置。

注意需要把位置切换到SkyThought/skythought/train/LLaMA-Factory目录下一定！

配置环境：

安装 LLaMA Factory

拉取代码

```
git clone --depth 1 https://github.com/hiyouga/LLaMA-Factory.git
```

环境创建

-- 前提安装anconda,避免跟其他软件的环境起冲突,单独建一个虚拟环境

```
conda create -n llamafactory  python=3.11
conda  activate llamafactory
```

安装依赖包

```
cd LLaMA-Factory
pip install -e ".[torch,metrics]"
```

LLaMA Board 可视化微调（由 Gradio 驱动）

```
llamafactory-cli webui
```

可能还存在缺失的安装包：

pip3 install deepspeed

pip install wandb

### 步骤 1

请将工具目录生成的数据路径或我们提供的数据路径，添加到 LLaMA-Factory/data/dataset_info.json 中 Sky-T1 条目的 file_name 字段。

```json
"Sky-T1": {
    "file_name": "your data path here",
    "formatting": "sharegpt",
    "columns": {
      "messages": "conversations",
      "system": "system"
    },
```

### 步骤 2：运行

首先登录wandb

```
wandb login
76ea5b2b06f6f9a718116bb3ec0bd54936f2fded
```

然后进行训练

```
FORCE_TORCHRUN=1 NNODES=1 NODE_RANK=0 MASTER_PORT=29501 llamafactory-cli train examples/train_full/qwen2_full_sft.yaml
```

在 8 个 H100 GPU 上从 32B 模型开始训练。感兴趣的读者可以参考 examples/train_full/qwen2_full_sft.yaml 中的详细设置。

---

这条命令在使用 `llamafactory-cli` 工具进行训练任务。以下是对各个参数的解释：

1. **`FORCE_TORCHRUN=1`**：

   - 这是一个环境变量，通常用于强制使用 `torchrun` 来启动分布式训练。`torchrun` 是 PyTorch 提供的一个工具，用于简化分布式训练的启动过程。
2. **`NNODES=1`**：

   - 这个环境变量指定了训练过程中使用的节点数量。在分布式训练中，`NNODES` 表示参与训练的机器（节点）数量。这里设置为 `1`，表示只使用一个节点进行训练。
3. **`NODE_RANK=0`**：

   - 这个环境变量用于指定当前节点的排名（编号）。在多节点训练中，每个节点都有一个唯一的编号，通常从 `0` 开始。这里设置为 `0`，表示这是第一个（也是唯一一个）节点。
4. **`MASTER_PORT=29501`**：

   - 这个环境变量指定了主节点（master node）用于通信的端口号。在分布式训练中，主节点负责协调其他节点的训练过程。`29501` 是用于节点间通信的端口号。
5. **`llamafactory-cli train`**：

   - 这是命令行工具 `llamafactory-cli` 的一个子命令，用于启动训练过程。`train` 表示执行训练任务。
6. **`examples/train_full/qwen2_full_sft.yaml`**：

   - 这是一个配置文件的路径，通常是一个 YAML 文件，包含了训练的详细配置参数，如模型架构、数据集路径、训练超参数等。`qwen2_full_sft.yaml` 可能是一个特定的训练配置文件。

总结来说，这条命令是在单节点上使用 `torchrun` 启动 `llamafactory-cli` 工具进行训练，使用的配置文件是 `qwen2_full_sft.yaml`。

---

### 常见报错处理

##### 1.无法连接到huggingface下载模型

需要把模型手动下载到服务器本地。

修改skythought/train/LLaMA-Factory/examples/train_full/qwen2_full_sft.yaml中的模型相关参数：

```
### model
model_name_or_path: Qwen/Qwen2.5-32B-Instruct
```

##### 2.-bash: llamafactory-cli: command not found

出现"`-bash: llamafactory-cli: command not found`"错误的原因通常是因为系统找不到名为 `llamafactory-cli`的可执行文件。可以先按照llama-factory项目的一般安装要求完成相关安装，然后再按照本项目要求完成相关环境配置。

##### 3. AssertionError: no_sync context manager is incompatible with gradient partitioning logic of ZeRO stage 3

不是所有的模型都支持deepspeed3！！

解决方法：替换deepspeed版本 **pip** install deepspeed==0.15.4

这个错误表明你当前的配置存在冲突:你正在使用 DeepSpeed ZeRO stage 3 优化，同时代码尝试使用 no_sync context manager 进行梯度累积
这两个功能是不兼容的，因为: ZeRO stage 3 会对梯度进行分区处理，而 no_sync 管理器试图阻止梯度同步，这与 ZeRO stage 3 的工作方式冲突
解决方案:
1.修改 DeepSpeed 配置，使用较低的 ZeRO stage (比如 stage 2 或 1)
2.或者调整训练参数，避免使用梯度累积（gradient accumulation）:
