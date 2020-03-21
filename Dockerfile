FROM python:3.6-alpine
WORKDIR /Nexus
COPY requirments.txt requirments.txt
RUN pip install -r requirments.txt
COPY upstream_listener.py upstream_listener.py
ENV host 172.17.0.1
ENV sender_queue downstream
ENV receiver_queue upstream
ENV src_system Nexus
ENV mq_host 172.17.0.2
ENV tracer_ip 172.17.0.3 
CMD ["python","upstream_listener.py"]
