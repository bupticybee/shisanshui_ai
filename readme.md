# 十三水AI

十三水ai，由于十三水ai信息集过大，无法直接采用CFR算法求解，所以我采用了独创的算法Deterministic CFR算法求解（使用类似Deterministic MCTS的方法，并且用在CFR上）。

这是我知识范围内首次Deterministic MCTS和CFR算法的结合，并且在我的实验中，这种算法在十三水上非常有效。

经验证算法十分有效，可以稳定击败我(> 60%胜率)， 也可以以超过56%的胜率击败baseline，另一款 [十三水开源AI](https://github.com/dannisliang/QPAlgorithm)， 也以55%的胜率战胜仅使用CFR的baseline。

## 编译&运行

### 在docker容器中运行

编译容器

```bash
docker build -t s3s_py:0.1 .
```

在容器中运行

```bash
docker run -it s3s_py:0.1 /bin/bash
python3 test_benchmark.py
```

###  本地运行
python 环境初始化

```bash
pip3 install pytest
```

pybind 环境初始化

```bash
cd pybind11
mkdir build
cd build
cmake ..
make check -j 4
make install
```
