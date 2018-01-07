FROM ubuntu:xenial
LABEL maintainer="mizutani@sfc.wide.ad.jp"

RUN apt-get update && apt-get install -y softflowd

CMD softflowd -i $DEVICE -n $NETFLOW_COLLECTOR -d

