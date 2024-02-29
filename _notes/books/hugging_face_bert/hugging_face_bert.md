# Hugging face


Python 3.6
transformers 4.18
datasets 2.3
PyTorch 1.10


## 安装依赖

我的arch linux在安装的时候，使用的是python 3.8.18，3.6的会提示版本过低

可以使用下面的`requirements.txt`文件
```txt
datasets==2.3
transformers==4.18
scipy==1.10.1
scikit-learn
sentencepiece
## CPU only
torch==1.10.1+cpu 
torchvision==0.11.2+cpu 
torchaudio==0.10.1
```
使用下面的命令直接安装即可
`pip install -r requirements.txt -f  https://download.pytorch.org/whl/cpu/torch_stable.html`



