ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM $BUILD_FROM

# Install required packages
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-requests \
    pulseaudio-utils

# Copy monitor script
COPY monitor.py /

# Copy rootfs
COPY rootfs /

RUN chmod a+x /monitor.py \
    /etc/services.d/monitor/run \
    /etc/services.d/monitor/finish
