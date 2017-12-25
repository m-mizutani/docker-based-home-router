FROM ubuntu:xenial
LABEL maintainer="mizutani@sfc.wide.ad.jp"

RUN apt-get update && apt-get install -y kea-dhcp4-server
RUN mkdir -p /etc/kea/
COPY kea-config.json /etc/kea/kea-config.json

CMD ["kea-dhcp4", "-c", "/etc/kea/kea-config.json"]
