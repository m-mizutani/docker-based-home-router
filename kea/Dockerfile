FROM mztn/kea:latest
LABEL maintainer="mizutani@sfc.wide.ad.jp"

RUN mkdir -p /etc/kea/
COPY kea-config.json /etc/kea/kea-config.json

CMD ["kea-dhcp4", "-c", "/etc/kea/kea-config.json"]
