FROM ubuntu:xenial-20210416
LABEL maintainer="mizutani@sfc.wide.ad.jp"

RUN apt-get update && apt-get install -y kea-dhcp4-server kea-admin mysql-client
RUN mkdir -p /etc/kea/
COPY kea-config.json /etc/kea/kea-config.json

RUN mkdir -p /usr/local/bin/
COPY startup.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/startup.sh
CMD ["/usr/local/bin/startup.sh"]
