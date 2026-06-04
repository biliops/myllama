FROM swr.cn-east-3.myhuaweicloud.com/higkoo/llama-kunpeng920:b9496

RUN rm -fv /etc/apt/sources.list.d/debian.sources && \
    apt update && \
    apt -y install python3-pip && \
    pip3 install --break-system-packages modelscope -i https://mirrors.aliyun.com/pypi/simple && \
    modelscope download unsloth/Qwen3-0.6B-GGUF Qwen3-0.6B-UD-IQ1_S.gguf --local_dir /tmp

COPY Qwen3-0.6.jinja /tmp/Qwen3-0.6.jinja

EXPOSE 12233

CMD ["llama-server", "--host", "0.0.0.0", "--port", "12233", \
     "-t", "20", "-tb", "40", "-np", "1", "-a", "Qwen3:0.6B", "-lv", "3", \
     "-m", "/tmp/Qwen3-0.6B-UD-IQ1_S.gguf", "--jinja", "--chat-template-file", "/tmp/Qwen3-0.6.jinja", \
     "--flash-attn", "on", "-ctk", "q4_0", "-ctv", "q4_0", "-c", "40960", "-b", "512", "-ub", "256", "--cache-ram", "8", \
     "-fit", "on", "--cont-batching", "--repack", "--no-mmap", "--kv-unified", "--cache-idle-slots", \
     "--mlock", "--mmap", "--warmup", "--props", "--metrics", \
     "--temp", "0.6", "--top_p", "0.95", "--top_k", "20", "--min_p", "0.0", \
     "--presence-penalty", "0.0", "--repeat-penalty", "1.0", \
     "--ui", "--path", "/opt/llama-b9496-ui"]