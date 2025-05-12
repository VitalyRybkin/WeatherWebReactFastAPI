FROM prom/prometheus:latest

COPY prometheus.yaml /etc/prometheus/prometheus.yaml

EXPOSE 9090

ENTRYPOINT [ "/bin/prometheus" ]
CMD ["--config.file=/etc/prometheus/prometheus.yaml"]