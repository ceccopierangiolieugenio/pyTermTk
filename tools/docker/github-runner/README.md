# Build the Docker
```bash
# This is in case you want to build the Docker with the token embedded
# Require to change the Dockerfile
#   _GITHUB_TOKEN=<your_github_runner_token>
#   docker build --build-arg RUNNER_TOKEN=${_GITHUB_TOKEN} -t github-runner .

docker buildx build -t github-runner-pytermtk  .

# To force an x86 build
docker buildx build -t github-runner-pytermtk --platform linux/amd64 .
```

# Run the runner using Docker Compose

```bash
GITHUB_TOKEN=<your_github_runner_token>
RUNNER_NAME=pytermtk_runner_01
TAGS="pytermtk-ubuntu-latest,self-hosted,Linux,X64"
URL='https://github.com/ceccopierangiolieugenio/pyTermTk'
docker compose up -d --scale runner=5

docker compose ps

# Scale up or down
docker compose up -d --scale runner=10
docker compose up -d --scale runner=3
```

# Run multiple runners if you don't have Docker Compose

```bash
GITHUB_TOKEN=<your_github_runner_token>
RUNNER_NAME=pytermtk_runner_01
TAGS="pytermtk-ubuntu-latest,self-hosted,Linux,X64"
URL='https://github.com/ceccopierangiolieugenio/pyTermTk'


for i in $(seq 1 5); do
  docker run -d --rm \
    --name "${RUNNER_NAME}_${i}" \
    --label app=github-runner-pytermtk-eugenio \
    github-runner-pytermtk-eugenio:latest \
    "${GITHUB_TOKEN}" "${RUNNER_NAME}_${i}" "${URL}" "${TAGS}" >/dev/null
done
```