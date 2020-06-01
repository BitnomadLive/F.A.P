FROM python:2

WORKDIR /root

RUN apt-get update && \
    apt-get upgrade -y

RUN apt-get install -y apt-utils

RUN apt-get install -y python-lzma python-pip python3-pip python3-pexpect unzip 

RUN wget ftp://ftp.si.debian.org/debian/pool/main/c/cramfs/cramfsprogs_1.1-6_amd64.deb

RUN dpkg -i ./cramfsprogs_1.1-6_amd64.deb

RUN apt-get install -y git-core wget build-essential liblzma-dev liblzo2-dev zlib1g-dev unrar-free && \
    pip install -U pip

RUN apt-get install -y fakeroot

RUN pip install nose coverage

RUN apt-get install python-crypto

RUN apt-get install python3-crypto

RUN git clone https://github.com/firmadyne/sasquatch && \
    cd sasquatch && \
    make && \
    make install && \
    cd .. && \
    rm -rf sasquatch

RUN git clone https://github.com/ReFirmLabs/binwalk.git && \
    cd binwalk && \
    ./deps.sh --yes && \
    python3 setup.py install && \
    pip3 install 'git+https://github.com/ahupp/python-magic' && \
    pip install 'git+https://github.com/sviehb/jefferson' && \
    cd .. && \
    rm -rf binwalk

RUN \
  adduser --disabled-password \
          --gecos '' \
          --home /home/extractor \
          extractor

RUN pip install psycopg2

USER extractor
WORKDIR /home/extractor

RUN git clone https://github.com/firmadyne/extractor.git

# Change interpretor in extractor.py to python3
RUN sed -i 's/env python/env python3/' ./extractor/extractor.py

RUN pip3 install psycopg2




