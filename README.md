<div align="center">

# SkyThought

[![Github](https://img.shields.io/badge/SkyThought-000000?style=for-the-badge&logo=github&logoColor=000&logoColor=white)](https://github.com/NovaSky-AI/SkyThought)  [![Hugging Face Collection](https://img.shields.io/badge/NovaSky-fcd022?style=for-the-badge&logo=huggingface&logoColor=000&labelColor)](https://huggingface.co/NovaSky-AI) [![Twitter](https://img.shields.io/badge/NovaSky-white?style=for-the-badge&logo=X&logoColor=000&color=000&labelColor=white)](https://x.com/NovaSkyAI)

<div align="center" style="font-family: Arial, sans-serif;">
  <p>
    <a href="#news" style="text-decoration: none; font-weight: bold;">新闻</a> •
    <a href="#links" style="text-decoration: none; font-weight: bold;">链接</a> •
    <a href="#getting-started" style="text-decoration: none; font-weight: bold;">快速开始</a> •
    <a href="#evaluation" style="text-decoration: none; font-weight: bold;">评估</a> •
    <a href="#citation" style="text-decoration: none; font-weight: bold;">引用</a> •
    <a href="#acknowledgement" style="text-decoration: none; font-weight: bold;">致谢</a> 
  </p>
</div>

</div>


# 新闻

- **[2025/01/10]** 🎉 我们已通过 [HuggingFace](https://huggingface.co/NovaSky-AI) 发布了我们的 Sky-T1-32B-Preview [模型](https://huggingface.co/NovaSky-AI/Sky-T1-32B-Preview) 和 [数据](https://huggingface.co/datasets/NovaSky-AI/Sky-T1_data_17k)！


# 链接

- 📜 [Sky-T1-32B-Preview 模型博客文章](https://novasky-ai.github.io/posts/sky-t1/)
- 🤗 [Sky-T1-32B-Preview 模型](https://huggingface.co/NovaSky-AI)

# 快速开始

我们开源了用于数据整理、训练和评估 Sky-T1-32B-Preview 的代码和脚本，您可以在每个目录中找到更多详细信息。
- ``/data``: 用于训练 Sky-T1-32B-Preview 的 17k 训练数据。我们还添加了来自 [STILL-2 模型](https://arxiv.org/pdf/2412.09413) 的科学和谜题部分。
- ``skythought/tools``: Sky-T1 的训练数据整理和评估。为了生成我们的训练数据，我们使用了 QwQ-32B-Preview 模型。我们整理的数据混合涵盖了需要推理的多样领域，并通过拒绝采样程序来提高数据质量。
- ``skythought/train``: Sky-T1 的训练脚本。我们使用 [Llama-Factory](https://github.com/hiyouga/LLaMA-Factory) 进行训练。模型经过 3 个周期的训练，学习率为 1e-5，批量大小为 96。我们的模型训练在 8 个 H100 GPU 上使用 DeepSpeed Zero-3 卸载完成，耗时约 19 小时，成本约为 450 美元（根据 Lambda Cloud 定价）。


# 评估
以下是我们在数学、编码和科学基准测试中对 Sky-T1-32B-Preview 模型的评估结果。

### 评估结果
| 指标                | Sky-T1-32B-Preview | Qwen-2.5-32B-Instruct | QwQ   | o1-preview |
|-----------------------|---------------------|--------|-------|------------|
| Math500              | 82.4                    | 76.2    | 85.4 | 81.4       |
| AIME2024             | 43.3                    | 16.7    | 50.0  | 40.0       |
| LiveCodeBench-Easy   | 86.3                    | 84.6   | 90.7  | 92.9       |
| LiveCodeBench-Medium | 56.8                    | 40.8   | 56.3  | 54.9       |
| LiveCodeBench-Hard   | 17.9                    | 9.8   | 17.1  | 16.3       |
| GPQA-Diamond         | 56.8                    | 45.5   | 52.5  | 75.2       |



## 完全开源：共同推动进步
我们相信开源协作推动进步，Sky-T1-32B-Preview 完全致力于赋能社区。我们开源所有细节（即数据、代码、模型权重），以便社区能够*轻松*复制和改进我们的结果：

<table>
  <thead>
    <tr>
      <th>模型</th>
      <th style="background-color: #f2f2f2;"><div align="center">Sky-T1-32B-Preview</div></th>
      <th><div align="center">STILL-2</div></th>
      <th><div align="center">Journey</div></th>
      <th><div align="center">QwQ</div></th>
      <th><div align="center">o1</div></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>数据</td>
      <td style="background-color: #f2f2f2;"><div align="center">✅</div></td>
      <td><div align="center">✅</div></td>
      <td><div align="center">❌</div></td>
      <td><div align="center">❌</div></td>
      <td><div align="center">❌</div></td>
    </tr>
    <tr>
      <td>代码</td>
      <td style="background-color: #f2f2f2;"><div align="center">✅</div></td>
      <td><div align="center">❌</div></td>
      <td><div align="center">❌</div></td>
      <td><div align="center">❌</div></td>
      <td><div align="center">❌</div></td>
    </tr>
    <tr>
      <td>报告</td>
      <td style="background-color: #f2f2f2;"><div align="center">✅</div></td>
      <td><div align="center">✅</div></td>
      <td><div align="center">✅</div></td>
      <td><div align="center">❌</div></td>
      <td><div align="center">❌</div></td>
    </tr>
    <tr>
      <td>数学领域</td>
      <td style="background-color: #f2f2f2;"><div align="center">✅</div></td>
      <td><div align="center">✅</div></td>
      <td><div align="center">✅</div></td>
      <td><div align="center">✅</div></td>
      <td><div align="center">✅</div></td>
    </tr>
    <tr>
      <td>编码领域</td>
      <td style="background-color: #f2f2f2;"><div align="center">✅</div></td>
      <td><div align="center">❌</div></td>
      <td><div align="center">❌</div></td>
      <td><div align="center">✅</div></td>
      <td><div align="center">✅</div></td>
    </tr>
    <tr>
      <td>模型权重</td>
      <td style="background-color: #f2f2f2;"><div align="center">✅</div></td>
      <td><div align="center">✅</div></td>
      <td><div align="center">❌</div></td>
      <td><div align="center">✅</div></td>
      <td><div align="center">❌</div></td>
    </tr>
  </tbody>
</table>

# 引用
本仓库中的代码主要在以下文章中描述。如果您觉得本仓库有帮助，请考虑引用此工作。

```bibtex
@misc{sky_t1_2025,
  author       = {NovaSky Team},
  title        = {Sky-T1: Train your own O1 preview model within $450},
  howpublished = {https://novasky-ai.github.io/posts/sky-t1},
  note         = {Accessed: 2025-01-09},
  year         = {2025}
}
```

# 致谢
本工作在 [Berkeley Sky Computing Lab](https://sky.cs.berkeley.edu/) 完成，得到了 [Lambda Labs](https://lambdalabs.com/service/gpu-cloud?srsltid=AfmBOop5FnmEFTkavVtdZDsLWvHWNg6peXtat-OXJ9MW5GMNsk756PE5) 和 [Anyscale](https://www.anyscale.com/) 的出色计算支持。我们要感谢 [Still-2 Team](https://arxiv.org/pdf/2412.09413) 和 [Qwen Team](https://qwenlm.github.io/) 的 Junyang Lin 提供的宝贵学术反馈和支持。


