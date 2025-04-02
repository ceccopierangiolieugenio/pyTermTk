# Build the Docker
```bash
_GITHUB_TOKEN=<your_github_runner_token>
docker build --build-arg RUNNER_TOKEN=${_GITHUB_TOKEN} -t github-runner .
```

# Run the runner
you can spawn as many runner as you want just changing the name
```bash
_GITHUB_TOKEN=<your_github_runner_token>
_RUNNER_NAME=runner_X
docker run -it --rm github-runner ${_GITHUB_TOKEN} ${_RUNNER_NAME}
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