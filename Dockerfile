FROM python:3.6-alpine
WORKDIR /Nexus
COPY requirments.txt requirments.txt
RUN pip install -r requirments.txt
COPY upstream_listener.py upstream_listener.py
ENV receiver_queue upstream
ENV downstream_sender downstream1
ENV downstream_listener downstream2
ENV gcd_sender gcd1
ENV gcd_listener gcd2
ENV src_system Nexus
ENV mq_host mq
ENV tracer_ip tracer
ENV sleep_time 60
CMD ["python","upstream_listener.py"]
