FROM scratch

RUN apt-get -qqy update \
    && apt-get -qqy --no-install-recommends install \
        sudo \
        supervisor \
    && apt-get autoclean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/*
RUN apt install pip
RUN apt install docker
RUN apt install docker.io
RUN apt install axel
RUN apt install p7zip-full

COPY requirements.txt requirements.txt

CMD ["pip install -r requirements.txt"]
CMD ["python3 test.py"]
