ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM $BUILD_FROM

# Install required packages
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-requests \
    pulseaudio-utils \
    bash

# Copy files
COPY run.sh /
COPY monitor.py /

RUN chmod a+x /run.sh /monitor.py

CMD [ "/run.sh" ]
