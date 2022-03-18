FROM alpine:3.15

RUN apk --no-cache add unbound
RUN mkdir -p /etc/unbound
COPY unbound.conf /etc/unbound/unbound.conf
CMD ["unbound", "-d", "-c", "/etc/unbound/unbound.conf"]
EXPOSE 53