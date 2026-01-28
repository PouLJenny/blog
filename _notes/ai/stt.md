# Speech-to-Text

## 路径

🎬 视频文件
   ↓（提取音频）
🔊 ffmpeg -i video.mp4 audio.wav
   ↓
🗣️ Whisper / FunASR / SenseVoice
   ↓
📜 得到字幕文本
   ↓
🧩 用大语言模型（如 ChatGLM、LLaMA、Qwen、Mistral）
     → 生成视频摘要、要点总结



## OpenAI Whisper

https://github.com/openai/whisper


## STT前的音频降噪处理

### demucs

此项目已经归档了

[github](https://github.com/facebookresearch/demucs/tree/main)
[安装依赖](https://github.com/facebookresearch/demucs/blob/main/environment-cpu.yml)

```shell
## 注意，由于demucs不怎么更新了，使用的时候需要用python3.9版本安装，不然使用起来有一些问题
pip install demucs

## 基本命令
demucs input.mp3

## 只提取人声，提取当当前目录
demucs -n htdemucs --two-stems vocals -o ./  2025-09-29-ppt-cut.mp3
```

# EOF