# S3S

## build

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

编译容器

```bash
docker build -t s3s_py:0.1 .
```

在容器中运行

```bash
docker run -it s3s_py:0.1 /bin/bash
python3 test_benchmark.py
```