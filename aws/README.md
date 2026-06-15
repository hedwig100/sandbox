# aws - ECS deploy practice

依存ゼロのPython製ミニWebアプリを、**ALB → ECS(Fargate)** 構成で全体公開。
インフラは Terraform 管理、state は S3 backend(ネイティブロック)。

## 実行

```
aws login
cd terraform/bootstrap
eval "$(aws configure export-credentials --format env)"
  terraform -chdir=terraform/bootstrap plan
eval "$(aws configure export-credentials --format env)"
  terraform -chdir=terraform/bootstrap apply

cd terraform
terraform init -backend-config=backend.hcl
terraform plan
terraform apply
```

## 構成
```
Internet ─▶ ALB(:80) ─▶ Target Group ─▶ ECS Service (Fargate, 2 tasks)
                                              └─ container :8080
                                                    │ (SG: 5432 from ECS only)
                                                    ▼
                                        RDS PostgreSQL (private subnet ×2AZ)
                                        password ← Secrets Manager で注入
```
- VPC + パブリックサブネット2つ(ALB/ECS) + プライベートサブネット2つ(RDS) / IGW
- SG: ALBは80を全開放、ECSはALBからのみ、RDSはECSからの5432のみ
- ECR / CloudWatch Logs / IAM(task execution role)
- RDS PostgreSQL(`db.t4g.micro`, single-AZ)/ Secrets Manager(DBパスワード)
- ヘルスチェック: `/health`

## アプリのエンドポイント
- `GET /` → `Hello from ECS! host=<hostname> visits=<DBに記録した累計アクセス数>`
  - DB未接続のローカル実行時は `... (no db)` を返す
- `GET /health` → `ok`

## セットアップ(初回)
```bash
# 1. state バケット名を一意な値に変更
#    terraform/backend.hcl の bucket = "ecs-sandbox-tfstate-change-me" を編集

# 2. AWS 認証 (例: SSO)
aws sso login   # or: export AWS_PROFILE=...

# 3. state用S3バケットを作成 (bootstrap、ローカルstate、初回のみ)
terraform -chdir=terraform/bootstrap init
terraform -chdir=terraform/bootstrap apply \
  -var "state_bucket=<backend.hclと同じバケット名>"

# 4. メインstackをS3 backendで初期化
terraform -chdir=terraform init -backend-config=backend.hcl
```

## インフラ操作(Terraformはそのまま)
```bash
terraform -chdir=terraform plan
terraform -chdir=terraform apply
terraform -chdir=terraform destroy
```

## コンテナのデプロイ
インフラ(`apply`済み)に対して、イメージを build & push してローリング更新するだけ:
```bash
./deploy.sh
```
やること: ECRへ build/push → `aws ecs update-service --force-new-deployment` →
App URL を表示。コードを変えるたびに叩けばOK。

> 初回 `apply` 直後はECRにイメージが無いためタスクが起動失敗を繰り返します。
> 一度 `./deploy.sh` でイメージをpushすればECSが自動でpullして立ち上がります。

## 後片付け
```bash
terraform -chdir=terraform destroy
# state バケットも消すなら
terraform -chdir=terraform/bootstrap destroy -var "state_bucket=<your-bucket>"
```

## ローカルで動作確認だけしたい
```bash
docker build -t ecs-sandbox .
docker run --rm -p 8080:8080 ecs-sandbox
curl localhost:8080
```

## 主な変数 (`terraform/variables.tf`)
| 変数 | デフォルト | 用途 |
|------|-----------|------|
| `region` | `ap-northeast-1` | リージョン |
| `desired_count` | `2` | タスク数 |
| `container_port` | `8080` | コンテナ/TGのポート |
| `cpu` / `memory` | `256` / `512` | Fargateサイズ |
