# Backend config for the S3 state store.
# The bucket name must be globally unique -- change it before first use.
bucket       = "hedwig100-ecs-sandbox-tfstate"
key          = "ecs-sandbox/terraform.tfstate"
region       = "ap-northeast-1"
encrypt      = true
use_lockfile = true # S3 native locking (no DynamoDB needed)
