FROM fluent/fluentd:v1.0.2

RUN mkdir -p /var/log/fluentd/
RUN chown 1000 /var/log/fluentd/

COPY fluent.conf /fluentd/etc/
