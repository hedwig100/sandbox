#!/usr/bin/env bash
# Deploy the container only: build -> push to ECR -> force a fresh ECS rollout.
#
# Infra (ALB/ECS/ECR/...) is managed separately with plain Terraform:
#   terraform -chdir=terraform init -backend-config=backend.hcl
#   terraform -chdir=terraform plan
#   terraform -chdir=terraform apply
# Run this script after the stack exists to ship a new image.
set -euo pipefail
cd "$(dirname "$0")"

TF_DIR="terraform"

REPO_URL=$(terraform -chdir="$TF_DIR" output -raw ecr_repository_url)
CLUSTER=$(terraform -chdir="$TF_DIR" output -raw cluster_name)
SERVICE=$(terraform -chdir="$TF_DIR" output -raw service_name)
REGION=$(terraform -chdir="$TF_DIR" output -raw region 2>/dev/null || echo "${AWS_REGION:-ap-northeast-1}")
REGISTRY="${REPO_URL%/*}"

echo "==> Building and pushing $REPO_URL:latest"
aws ecr get-login-password --region "$REGION" \
  | docker login --username AWS --password-stdin "$REGISTRY"
docker build --platform linux/amd64 -t "$REPO_URL:latest" .
docker push "$REPO_URL:latest"

echo "==> Forcing new ECS deployment"
aws ecs update-service --cluster "$CLUSTER" --service "$SERVICE" \
  --force-new-deployment --region "$REGION" >/dev/null

echo "Done. App URL: $(terraform -chdir="$TF_DIR" output -raw alb_url)"
