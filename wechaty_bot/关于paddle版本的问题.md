1.由于paddle的版本问题：
paddle>=2.3.0    pip install --upgrade paddlepaddle==2.3.0 或者最新版本 
numpy>=1.22.4

paddle的主要问题 不要直接 pip insatll paddle   
如果出现 no moudel xxx  或者出现对应包下 类或方法找不到的情况  即版本找不到  直接在lib 的sitpackages 中
将其对应的包删除 包有两个 一定要把两个对应的都删除掉
如 paddleehub  和  paddlehub-2.4.0.dist-info  两个需要都进行删除

