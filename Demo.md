# llama.cpp ARM 推理服务部署指南

本文档将指导你使用 Demo.Dockerfile 部署 Qwen3-0.6B 大语言模型推理服务。

## 前置条件

- 已安装 Docker 或 Podman
- 具备互联网访问能力
- 建议配置：鲲鹏 920 处理器，至少 16GB 内存

## 操作步骤

### 1. 下载 Dockerfile

下载 Demo.Dockerfile：

```bash
git clone https://github.com/higkoo/MyLLaMA.git
cd MyLLaMA
```

### 2. 构建 Docker 镜像

执行以下命令构建镜像：

```bash
docker build -t llama-qwen3-0.6b -f Demo.Dockerfile .
```

> **说明**：构建过程会自动完成以下工作：
> - 基于华为云镜像创建容器
> - 安装 Python 和 modelscope
> - 从 modelscope 下载 Qwen3-0.6B-GGUF 模型
> - 配置 llama-server 启动参数

### 3. 启动推理服务

镜像构建完成后，运行以下命令启动服务：

```bash
docker run -d \
  --name llama-server \
  -p 12233:12233 \
  llama-qwen3-0.6b
```

> **参数说明**：
> - `-d`：后台运行容器
> - `--name llama-server`：给容器命名为 llama-server
> - `-p 12233:12233`：将主机的 12233 端口映射到容器内部

### 4. 验证服务是否启动

查看容器运行状态：

```bash
docker ps
```

如果看到 STATUS 列显示 "Up"，说明服务已启动。

### 5. 访问推理页面

打开浏览器，访问以下地址：

```
http://你的服务器IP:12233
```

例如：`http://192.168.1.100:12233`

你将看到 llama.cpp 的 Web UI 界面，可以直接输入问题进行对话。

## API 调用示例

除了 Web UI，你也可以通过 API 调用：

```bash
curl -X POST http://你的服务器IP:12233/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "你好，给我讲个笑话"}],
    "max_tokens": 500,
    "temperature": 0.7
  }'
```

## 常用命令

### 查看容器日志

```bash
docker logs -f llama-server
```

### 停止服务

```bash
docker stop llama-server
```

### 重启服务

```bash
docker restart llama-server
```

### 删除容器

```bash
docker rm -f llama-server
```

## 技术说明

### Dockerfile 内容解析

```dockerfile
# 使用华为云的预构建镜像（已优化鲲鹏920）
FROM swr.cn-east-3.myhuaweicloud.com/higkoo/llama-kunpeng920:b9496

# 安装依赖和下载模型
RUN rm -fv /etc/apt/sources.list.d/debian.sources && \
    apt update && \
    apt -y install python3-pip && \
    pip3 install --break-system-packages modelscope -i https://mirrors.aliyun.com/pypi/simple && \
    modelscope download unsloth/Qwen3-0.6B-GGUF Qwen3-0.6B-UD-IQ1_S.gguf --local_dir /tmp

# 暴露端口
EXPOSE 12233

# 启动命令
CMD ["llama-server", "--host", "0.0.0.0", "--port", "12233", ...]
```

### 启动参数说明

| 参数 | 说明 |
|------|------|
| `-t 20` | 使用 20 个线程 |
| `-tb 40` | 批处理线程数 40 |
| `-a 'Qwen3:0.6B'` | 指定模型架构 |
| `-c 40960` | 上下文窗口大小 |
| `--flash-attn on` | 启用 Flash Attention |
| `--ui` | 启用 Web UI |