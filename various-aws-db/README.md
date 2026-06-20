# various-aws-db - DynamoDB from Python (ECS-only access)

Python(boto3)製のミニWebアプリから DynamoDB を触る練習。
肝は **DynamoDB を「VPC内のECSからのみ」アクセス可能にロックする** こと。
インフラは Terraform 管理、state は S3 backend(ネイティブロック)。

## 構成
```
Internet ─▶ ALB(:80) ─▶ ECS Service (Fargate)
                              └─ container :8080 (boto3)
                                      │  DynamoDB API
                                      ▼
                          ┌─────────────────────────┐
                          │ DynamoDB Gateway VPC EP  │  ← VPC内からの唯一の経路
                          └─────────────────────────┘
                                      │ (aws:SourceVpce = この EP のときだけ許可)
                                      ▼
                              DynamoDB テーブル
```

### 「ECSからのみ・VPC内からのみ」を実現する2層
1. **VPC内からのみ**: DynamoDB の **Gateway VPC Endpoint** を作り、
   テーブルの **リソースベースポリシー** が
   「`aws:SourceVpce` がこのエンドポイント以外のデータ操作(GetItem/PutItem/Query/Scan…)を **Deny**」。
   → 手元のPCの管理者権限やマネジメントコンソールからでも **データは触れない**。
2. **ECSからのみ**: DynamoDB のデータ権限は **ECSタスクロール(IAM)** にだけ付与。
   このロールを引き受けるのはECSタスクだけ。

> control-plane 操作(DescribeTable / UpdateTable / PutResourcePolicy 等)は Deny の対象外。
> なので Terraform やコンソールからの **テーブル管理は普通にできる**(自分をロックアウトしない)。

> ECSはECRからのイメージ取得のためpublic subnet + public IP 配置(NATゲートウェイ不要)。
> DynamoDB通信だけはルートテーブル経由でGateway Endpointを通るので、
> ECSに外向き通信があってもDynamoDBのロックは弱まりません。

## セットアップ(初回)
```bash
# 1. state バケット名を一意な値に変更
#    terraform/backend.hcl の bucket = "hedwig100-dynamodb-sandbox-tfstate" を編集

# 2. AWS 認証
aws sso login   # or: export AWS_PROFILE=...

# 3. state用S3バケットを作成 (bootstrap、ローカルstate、初回のみ)
terraform -chdir=terraform/bootstrap init
terraform -chdir=terraform/bootstrap apply \
  -var "state_bucket=<backend.hclと同じバケット名>"

# 4. メインstackをS3 backendで初期化
terraform -chdir=terraform init -backend-config=backend.hcl
```

## インフラ操作
```bash
terraform -chdir=terraform plan
terraform -chdir=terraform apply
terraform -chdir=terraform destroy
```

## コンテナのデプロイ
インフラ(`apply`済み)に対して、イメージを build & push してローリング更新:
```bash
./deploy.sh
```
> 初回 `apply` 直後はECRにイメージが無いためタスクが起動失敗を繰り返します。
> 一度 `./deploy.sh` でイメージをpushすればECSが自動でpullして立ち上がります。

## DynamoDBで遊ぶ
ALBのURL(`terraform -chdir=terraform output -raw alb_url`)に対して:
```bash
URL=$(terraform -chdir=terraform output -raw alb_url)

curl "$URL/"                       # 訪問を記録しカウンタを加算 -> visits=N
curl "$URL/items"                  # 直近アイテムをScanして一覧
curl -X PUT "$URL/items/hello" -d 'world'   # PutItem (pk=hello, value=world)
curl "$URL/items/hello"            # GetItem
```

## ロック確認(VPC外からは触れない)
手元のPCから直接DynamoDBを叩くと **AccessDenied** になるのが正解:
```bash
TABLE=$(terraform -chdir=terraform output -raw dynamodb_table)

# データ操作は拒否される(VPCエンドポイント経由ではないため)
aws dynamodb get-item --table-name "$TABLE" \
  --key '{"pk":{"S":"counter#visits"}}'
# -> AccessDeniedException: ... explicit deny in a resource-based policy

# 一方、管理系(control-plane)はできる
aws dynamodb describe-table --table-name "$TABLE" --query 'Table.TableStatus'
# -> "ACTIVE"
```

## ローカルで動作確認だけしたい(DynamoDB Localを使う)
本物のテーブルはVPC外から触れないので、ローカル試験は DynamoDB Local で:
```bash
docker run --rm -p 8000:8000 amazon/dynamodb-local
# 別シェル: 環境変数でローカルエンドポイントへ向ける等、app.py を調整して試す
```

## 後片付け
```bash
terraform -chdir=terraform destroy
# state バケットも消すなら
terraform -chdir=terraform/bootstrap destroy -var "state_bucket=<your-bucket>"
```

## 主な変数 (`terraform/variables.tf`)
| 変数 | デフォルト | 用途 |
|------|-----------|------|
| `region` | `ap-northeast-1` | リージョン |
| `name` | `dynamodb-sandbox` | リソース名プレフィックス/テーブル名 |
| `desired_count` | `1` | タスク数 |
| `container_port` | `8080` | コンテナ/TGのポート |
| `cpu` / `memory` | `256` / `512` | Fargateサイズ |
