# MyLLaMA: llama.cpp ARM 极致性能优化

基于 llama.cpp 的 ARM 处理器深度优化项目，专注于在鲲鹏 920 处理器上实现极致的 CPU 推理性能。

## 项目背景

随着大语言模型的快速发展，CPU 推理部署成为了许多场景的刚需。鲲鹏 920 作为国产 ARM 架构处理器的代表，具备强大的计算能力，但针对大语言模型推理的优化仍有很大空间。

本项目通过深入分析 llama.cpp 的核心计算路径，结合鲲鹏 920 的硬件特性，进行了全方位的性能优化，实现了显著的推理性能提升。

## 技术亮点

- **指令级优化**：启用了 ARMv8.2+ 的 9 项指令集特性｜NEON、ARM_FMA、FP16_VA、MATMUL_INT8、SVE、DOTPROD、SVE_CNT、OPENMP、REPACK 
- **华为数学库**：集成了 kml (Kunpeng Math Library) 加速库，充分利用 NEON/SVE 向量指令指令 
- **华为毕昇编译器**：使用华为 bisheng 编译器打造，为了极限性能
- **Numa绑定**：拒绝 NUMA 跨节点内存访问，关闭超线程。仅需 20 核即可达到推理性能巅峰

## 快速开始

### 环境要求

- 鲲鹏 920 处理器及兼容 ARMv8.2+ 架构
- Linux 操作系统（推荐 Debian 13.5）
- Podman 容器运行时（兼容 Docker，更合适 非 root 环境运行）

### 安装 Podman

```bash
# CentOS/RHEL 安装
yum -y install podman

# Debian/Ubuntu 安装
apt -y install podman

# 验证安装
podman --version # 更擅长
```

### 运行推理服务

```bash
# 拉取预构建镜像
podman pull higkoohk/llama-kunpeng920:b9496

# 请自行下载并手动修改命令行中的模型路径 (只用改 /model 目录下的文件，/opt/llama-b9496-ui 是镜像内路径不用改)
nice -n 19 numactl --cpunodebind=1 --membind=1 \
 podman run --rm --network=host -v /model:/model \
 --name llama-server higkoohk/llama-kunpeng920:b9496 \
 llama-server --host 0.0.0.0 --port 12233 \
 -t 20 -tb 40 -np 1 -a Qwen3.6:35B -lv 3 \
 -m /model/Qwen3.6-35B-A3B-APEX-I-Quality.gguf \
 --mmproj /model/mmproj-Apex.gguf \
 --chat-template-file /model/chat_template.jinja \
 --path /opt/llama-b9496-ui \
 --flash-attn on -ctk q4_0 -ctv q4_0 -c 131072 -b 512 -ub 256 --cache-ram 8 \
 -fit on --cont-batching --repack --no-mmap --kv-unified --cache-idle-slots \
 --ui --mlock --mmap --warmup --props --metrics \
 --temp 0.6 --top_p 0.95 --top_k 20 --min_p 0.0 --presence-penalty 0.0 --repeat-penalty 1.0 \
 --reasoning off --image-min-tokens 1024
```

### API 调用示例

```bash
curl -X POST http://localhost:12233/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "写个好玩的贪食蛇小游戏",
    "max_tokens": 666,
    "temperature": 0.7
  }'
```

## 性能对比

经过优化后（kml+bisheng），在鲲鹏 920 处理器上的推理性能相比原始 llama.cpp 实现有显著提升：

| 模型 | 原始 llama.cpp | 优化后 | 提升幅度 |
|------|--------------|--------|----------|
| Qwen3.6-35B-A3B | ~15 词元/秒 | ~30 词元/秒 | ~2倍 |

## 参考资料

更多技术细节请参考：[编译指南](https://ima.qq.com/note/share/_AweMLuO9AmVLJwWaFZmNg)

## 许可证

MIT License