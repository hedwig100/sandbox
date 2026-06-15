# aws - ECS deploy practice app

依存ゼロのPython製ミニWebアプリ。ECS(Fargate)へのデプロイ練習用。

## エンドポイント
- `GET /` → `Hello from ECS! host=<container hostname>`
- `GET /health` → `ok` (ヘルスチェック用)

## ローカルで動かす
```bash
docker build -t ecs-sandbox .
docker run --rm -p 8080:8080 ecs-sandbox
curl localhost:8080
curl localhost:8080/health
```

## ECRへpush（例）
```bash
AWS_REGION=ap-northeast-1
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REPO=ecs-sandbox

aws ecr create-repository --repository-name $REPO --region $AWS_REGION
aws ecr get-login-password --region $AWS_REGION \
  | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

docker build -t $REPO .
docker tag $REPO:latest $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO:latest
docker push $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO:latest
```

あとはECSクラスタ/タスク定義/サービスを作って、コンテナポート `8080`、
ヘルスチェックパス `/health` を指定すればOK。
