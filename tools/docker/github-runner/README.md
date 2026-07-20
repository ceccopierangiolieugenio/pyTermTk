# Build the Docker
```bash
# This is in case you want to build the Docker with the token embedded
# Require to change the Dockerfile
#   _GITHUB_TOKEN=<your_github_runner_token>
#   docker build --build-arg RUNNER_TOKEN=${_GITHUB_TOKEN} -t github-runner .

docker build -t github-runner .

# To force an x86 build
docker buildx build -t github-runner --platform linux/amd64 .
```

# Run the runner
you can spawn as many runner as you want just changing the name
```bash
GITHUB_TOKEN=<your_github_runner_token>
RUNNER_NAME=runner_X
docker run -it --rm github-runner ${_GITHUB_TOKEN} ${_RUNNER_NAME}
```

# Run the runner using Docker Compose
```bash
GITHUB_TOKEN=<your_github_runner_token>
docker compose up -d --scale runner=5

docker compose ps

# Scale up or down
docker compose up -d --scale runner=10
docker compose up -d --scale runner=3
```

## note:
```bash
_GITHUB_TOKEN=<your_github_runner_token>
./config.sh \
    --url https://github.com/ceccopierangiolieugenio/pyTermTk \
    --work _work --replace \
    --runnergroup Default \
    --name test-sh \
    --token ${_GITHUB_TOKEN} \
    --labels "self-hosted,Linux,ARM64"
```