FROM python:latest

RUN pip install cvdupdate schedule
RUN cvd config set --dbdir /clamav
RUN mkdir -p /opt/clamav-mirror

COPY main.py /opt/clamav-mirror

WORKDIR /opt/clamav-mirror

CMD python3 main.py

VOLUME /clamav

EXPOSE 8081
