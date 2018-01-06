FROM ubuntu:xenial
LABEL maintainer="mizutani@sfc.wide.ad.jp"

RUN apt-get update && apt-get install -y wget lsb-release
RUN mkdir -p /opt \
  && wget http://apt-stable.ntop.org/16.04/all/apt-ntop-stable.deb \
	&& dpkg -i apt-ntop-stable.deb \
	&& apt-get update && apt-get install -y nprobe

COPY nprobe.conf /etc/nprobe/nprobe.conf
CMD nprobe /etc/nprobe/nprobe.conf

