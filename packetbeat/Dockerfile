FROM alpine:3.15.3

RUN apk --no-cache add curl libpcap libc6-compat
RUN mkdir -p /opt/ \
  && cd /opt \
	&& curl -O https://artifacts.elastic.co/downloads/beats/packetbeat/packetbeat-6.1.1-linux-x86_64.tar.gz \
  && tar xzf packetbeat-6.1.1-linux-x86_64.tar.gz \
	&& mv packetbeat-6.1.1-linux-x86_64/packetbeat /opt/packetbeat \
	&& rm -rf /opt/packetbeat-6.1.1-linux-x86_64*
COPY packetbeat.yml /opt/
RUN chmod 600 /opt/packetbeat.yml
CMD /opt/packetbeat -c /opt/packetbeat.yml
