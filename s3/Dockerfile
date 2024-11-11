# Dockerfile
FROM localstack/localstack

# Copy the local scripts into the image
COPY . /etc/localstack/init/ready.d

# Set execute permissions on the scripts
RUN chmod +x /etc/localstack/init/ready.d/*.sh