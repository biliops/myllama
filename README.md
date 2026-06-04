# MyLLaMA - llama.cpp ARM 极致性能优化项目

基于 llama.cpp 在华为鲲鹏 920 (KunPeng 920) ARM 处理器上的极致性能优化项目，专注于 CPU 推理场景。

## 项目背景

### 1. 硬件环境
- **处理器**: 华为鲲鹏 920 (KunPeng 920)
- **架构**: ARMv8.2-A
- **核心数**: 支持多核心并行计算
- **内存**: 高性能 DDR4 内存

### 2. 优化动机
- **原生性能瓶颈**: 标准 llama.cpp 在 ARM 平台上未充分利用硬件特性
- **指令集优化**: ARM NEON 指令集具备强大的向量计算能力
- **内存访问优化**: 鲲鹏架构的内存层次结构需要针对性优化
- **多核并行**: 充分利用多核心优势提升推理吞吐量

### 3. 优化成果
详细的优化过程和性能对比请参考: [llama.cpp在arm处理器下的极致性能.pdf](llama.cpp在arm处理器下的极致性能.pdf)

---

## 快速开始

### 环境要求
```bash
# 架构要求
uname -m  # 输出: aarch64

# 确认 ARM 版本
cat /proc/cpuinfo | grep "model name"
```

### 编译安装

```bash
# 克隆项目
git clone git@github.com:biliops/MyLLaMA.git
cd MyLLaMA

# 编译优化版本
./install.sh
```

### 运行服务

```bash
# 启动推理服务
./start.sh

# 或直接运行
./llama-server --help
```

---

## 使用方法

### 命令行接口

```bash
# 基础推理
./llama-server \
  --model models/llama-7b.gguf \
  --threads 32 \
  --batch-size 512

# 性能测试
./llama-server \
  --model models/llama-7b.gguf \
  --benchmark \
  --threads 64
```

### API 接口

服务启动后提供 HTTP API:

```bash
# 发送推理请求
curl -X POST http://localhost:8080/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Hello, my name is",
    "max_tokens": 100
  }'
```

---

## 性能优化亮点

| 优化维度 | 优化策略 | 性能提升 |
|---------|---------|---------|
| **指令集** | ARM NEON 向量化 | ~30% |
| **内存布局** | 连续内存预取 | ~15% |
| **线程调度** | NUMA 感知调度 | ~20% |
| **缓存利用** | 数据预加载优化 | ~10% |
| **算子融合** | 计算图优化 | ~25% |

---

## 项目结构

```
MyLLaMA/
├── llama-server        # 优化后的推理服务二进制
├── install.sh          # 编译安装脚本
├── start.sh            # 服务启动脚本
├── app.py              # Python API 封装
├── test_llama_server.py # 测试脚本
├── requirements.txt    # Python 依赖
├── templates/          # Web 界面模板
├── models/             # 模型文件目录(需自行放置)
└── llama.cpp在arm处理器下的极致性能.pdf  # 优化文档
```

---

## 性能基准测试

测试环境: KunPeng 920, 64 cores, 128GB RAM

| 模型 | 原始 llama.cpp | 优化后 | 提升幅度 |
|-----|--------------|-------|---------|
| LLaMA-7B | ~18 tokens/s | ~45 tokens/s | **+150%** |
| LLaMA-13B | ~10 tokens/s | ~28 tokens/s | **+180%** |

---

## 许可证

MIT License

---

## 参考文档

- [llama.cpp 官方仓库](https://github.com/ggerganov/llama.cpp)
- [鲲鹏 920 技术白皮书](https://www.huawei.com/cn/products/servers/processors/kunpeng-920)
- [ARM NEON 编程指南](https://developer.arm.com/architectures/instruction-sets/simd-isas/neon)
