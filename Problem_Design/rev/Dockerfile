FROM ubuntu:20.04

RUN apt update && DEBIAN_FRONTEND="noninteractive" apt install -y \
  python3 build-essential

WORKDIR /root

COPY code/ .
CMD ["/usr/local/bin/python", "/root/compile_rev.py"]