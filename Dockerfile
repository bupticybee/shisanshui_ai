FROM python:3.6
WORKDIR /app
ADD . .
RUN pip  install -r requirements.txt
RUN mv resources/cmake-3.17.0-Linux-x86_64.tar.gz . \
    && tar -zxvf cmake-3.17.0-Linux-x86_64.tar.gz \
    && mv cmake-3.17.0-Linux-x86_64 cmake-3.17.0 \
    && ln -sf /cmake-3.17.0/bin/* /usr/bin
RUN rm -rf build
RUN mkdir build && cd build && /app/cmake-3.17.0/bin/cmake .. && make && make install && cd ..
RUN cd install && mv s3spy.cpython-36m-x86_64-linux-gnu.so ../s3spy.so && cd ..