## 训练

我们使用 [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) 的一个分支进行训练。

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

`FORCE_TORCHRUN=1 NNODES=1 NODE_RANK=0 MASTER_PORT=29501 llamafactory-cli train examples/train_full/qwen2_full_sft.yaml`

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
