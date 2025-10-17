FROM alpine:3.19

# Install required packages
RUN apk add --no-cache \
    python3 \
    py3-requests \
    pulseaudio-utils \
    jq \
    curl

# Copy files
COPY run.sh /run.sh
COPY monitor.py /monitor.py

RUN chmod a+x /run.sh /monitor.py

CMD ["/run.sh"]
