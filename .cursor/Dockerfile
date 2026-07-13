# Python 3.12 base for SWESimBench / user.skill Cloud Agents.
# Do not COPY the project; Cursor checks out the commit.
FROM public.ecr.aws/docker/library/python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
      ca-certificates curl git unzip \
    && rm -rf /var/lib/apt/lists/*

# AWS CLI v2 for private S3 hydrate (credentials via CURSOR_AWS_ASSUME_IAM_ROLE_ARN).
RUN curl -fsSL "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o /tmp/awscliv2.zip \
    && unzip -q /tmp/awscliv2.zip -d /tmp \
    && /tmp/aws/install \
    && rm -rf /tmp/aws /tmp/awscliv2.zip

WORKDIR /workspace
