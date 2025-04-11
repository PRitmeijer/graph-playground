FROM debian:bullseye-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y curl ca-certificates unzip && \
    rm -rf /var/lib/apt/lists/*

# Install yq (Go-based) manually
RUN curl -L https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64 -o /usr/bin/yq && \
    chmod +x /usr/bin/yq

# Install Rover
RUN curl -sSL https://rover.apollo.dev/nix/latest | sh

# Add rover to PATH
ENV PATH="/root/.rover/bin:$PATH"

# Create folders
COPY /config /config
RUN mkdir -p /output

# Copy script and set working dir
COPY /docker/fetch-schemas.sh /app/fetch-schemas.sh
WORKDIR /app
RUN chmod +x fetch-schemas.sh

CMD ["/app/fetch-schemas.sh"]