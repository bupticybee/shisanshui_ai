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