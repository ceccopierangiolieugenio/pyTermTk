# Use the latest Ubuntu image as the base
FROM ubuntu:latest
# FROM --platform=linux/arm64 ubuntu:latest
# FROM --platform=linux/amd64 ubuntu:latest

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Update and install default applications
RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    maven ant sudo \
    libicu74 sqlite3 \
    gh git curl wget jq \
    zip unzip tar \
    && apt-get clean

# Clean up
RUN rm -rf /var/lib/apt/lists/*

RUN echo 'ubuntu ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Switch to the ubuntu user
USER ubuntu

WORKDIR /home/ubuntu

# x86-64
RUN curl -o actions-runner-linux-x64-2.323.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.323.0/actions-runner-linux-x64-2.323.0.tar.gz
RUN echo "0dbc9bf5a58620fc52cb6cc0448abcca964a8d74b5f39773b7afcad9ab691e19  actions-runner-linux-x64-2.323.0.tar.gz" | shasum -a 256 -c

# arm-64
# RUN curl -o actions-runner-linux-arm64-2.323.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.323.0/actions-runner-linux-arm64-2.323.0.tar.gz
# RUN echo "9cb778fffd4c6d8bd74bc4110df7cb8c0122eb62fda30b389318b265d3ade538  actions-runner-linux-arm64-2.323.0.tar.gz" | shasum -a 256 -c

RUN mv actions-runner-linux-* actions-runner-linux.tgz

RUN mkdir -p /home/ubuntu/runner_1

WORKDIR /home/ubuntu/runner_1

RUN tar xzf ../actions-runner-linux.tgz

# # Add this line to accept the token as a build argument
# ARG RUNNER_TOKEN
# # Use the token in the configuration step
# RUN ./config.sh --url https://github.com/ceccopierangiolieugenio/pyTermTk --token ${RUNNER_TOKEN}

COPY script.sh script.sh
RUN sudo chmod +x script.sh

ENTRYPOINT ["./script.sh"]
