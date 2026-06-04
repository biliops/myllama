# MyLLaMA: llama.cpp ARM 极致性能优化

基于 llama.cpp 的 ARM 处理器深度优化项目，专注于在鲲鹏 920 处理器上实现极致的 CPU 推理性能。

## 项目背景

随着大语言模型的快速发展，CPU 推理部署成为了许多场景的刚需。鲲鹏 920 作为国产 ARM 架构处理器的代表，具备强大的计算能力，但针对大语言模型推理的优化仍有很大空间。

本项目通过深入分析 llama.cpp 的核心计算路径，结合鲲鹏 920 的硬件特性，进行了全方位的性能优化，实现了显著的推理性能提升。

## 技术亮点

- **指令级优化**：充分利用 ARMv8.2+ 指令集特性
- **内存布局优化**：优化数据访问模式，提升缓存命中率
- **线程调度优化**：针对 NUMA 架构优化线程分配策略
- **量化策略优化**：在精度与性能之间找到最佳平衡点

## 快速开始

### 环境要求

- 鲲鹏 920 处理器及兼容 ARMv8.2+ 架构
- Linux 操作系统（推荐 CentOS 7.6+ 或 Ubuntu 18.04+）
- 至少 16GB 内存（建议 32GB+）

### 安装与运行

```bash
# 克隆项目
git clone git@github.com:biliops/MyLLaMA.git
cd MyLLaMA

# 安装依赖
bash install.sh

# 启动服务
bash start.sh
```

### 使用示例

```bash
# 运行推理服务
./llama-server --model ./models/llama-7b.gguf --port 8080

# API 调用示例
curl -X POST http://localhost:8080/completions \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, world!", "max_tokens": 100}'
```

## 性能对比

经过优化后，在鲲鹏 920 处理器上的推理性能相比原始 llama.cpp 实现有显著提升：

| 模型 | 原始 llama.cpp | 优化后 | 提升幅度 |
|------|--------------|--------|----------|
| LLaMA-7B | ~15 tokens/s | ~45 tokens/s | 200% |
| LLaMA-13B | ~8 tokens/s | ~28 tokens/s | 250% |

## 参考资料

更多技术细节请参考：[技术分享](https://ima.qq.com/note/share/_AweMLuO9AmVLJwWaFZmNg)

## 许可证

MIT License