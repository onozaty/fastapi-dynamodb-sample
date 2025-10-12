# fastapi-dynamodb-sample

FastAPI + DynamoDB のサンプルプロジェクト

## セットアップ

依存関係のインストール:

```bash
uv sync
```

DynamoDB Localにテーブルを作成:

```bash
bash ./dynamodb/create-tables-local.sh
```

## 開発サーバー

開発サーバーを起動する前に、上記のセットアップを完了してください。

```bash
uv run fastapi dev
```

## コード品質チェック

### Linter/Formatter (Ruff)

```bash
# Linter実行
uv run ruff check

# フォーマット
uv run ruff format
```

### 型チェック (Pyright)

```bash
uv run pyright
```

## テスト

```bash
uv run pytest
```

## DynamoDB Local

開発環境ではDynamoDB Localが起動しています:

- **エンドポイント**: `http://dynamodb-local:8000`

### テーブルの作成

```bash
bash ./dynamodb/create-tables-local.sh
```

このスクリプトは `dynamodb/table-definitions/` ディレクトリ内のJSON定義ファイルを読み込み、テーブルを作成します。

### AWS CLIでの操作例

```bash
# 環境変数でダミー認証情報を設定
export AWS_ACCESS_KEY_ID=dummy
export AWS_SECRET_ACCESS_KEY=dummy

# テーブル一覧
aws dynamodb list-tables \
  --endpoint-url http://dynamodb-local:8000 \
  --region ap-northeast-1

# テーブル定義の確認
aws dynamodb describe-table \
  --table-name items \
  --endpoint-url http://dynamodb-local:8000 \
  --region ap-northeast-1

# テーブルの削除
aws dynamodb delete-table \
  --table-name items \
  --endpoint-url http://dynamodb-local:8000 \
  --region ap-northeast-1
```

## AWS Lambda (AWS SAM を使用したデプロイ)

このプロジェクトは Docker イメージとして Lambda 上で稼働するための `Dockerfile` と `template.yaml` を含んでいます。AWS SAM CLI を利用することで、コンテナイメージのビルド・ECR へのプッシュ・API Gateway/Lambda/DynamoDB テーブルの作成を一括で行えます。

### 前提条件

- 認証情報が設定されていること

### デプロイ手順

1. ビルドします。

    ```bash
    sam build
    ```

2. 一度目のデプロイはガイド付きで実行し、ECR リポジトリなどの設定を保存します。

    ```bash
    sam deploy --guided
    ```

    以下は設定例です。必要に応じて変更してください。

    - **Stack Name**: `fastapi-dynamodb-sample`
    - **AWS Region**: `ap-northeast-1`
    - **Confirm changes before deploy**: `y`
    - **Allow SAM CLI IAM role creation**: `y`
    - **Disable rollback**: `n`
    - **FastApiFunction has no authentication. Is this okay?**: `y`
    - **Save arguments to samconfig.toml**: `y`
    - **SAM configuration file**: `samconfig.toml`
    - **SAM configuration environment**: `default`
    - **Create managed ECR repositories for all functions?**: `y`

3. 2回目以降は設定が `samconfig.toml` に保存されるため、次のコマンドだけで反映できます。

    ```bash
    sam build
    sam deploy
    ```

4. デプロイ完了後、出力される API Gateway エンドポイント (`ApiEndpoint`) にアクセスすることで FastAPI アプリを利用できます。

### DynamoDB テーブルについて

- アプリケーションは環境変数 `ITEMS_TABLE_NAME` を参照し、未設定時は `items` を使用します（ローカル開発向け）。
- SAM テンプレートでは `fastapi-dynamodb-sample-items` テーブルを作成し、その名称を `ITEMS_TABLE_NAME` として Lambda に渡しています。

既存テーブルを利用する場合は、`template.yaml` のテーブル定義を削除/変更するか、デプロイ時に `ITEMS_TABLE_NAME` を別値に上書きしてください。

SAM Local で DynamoDB Local を利用する場合は、SAM CLI の環境変数ファイル（例: `sam local start-api --env-vars env.json`）に `DYNAMODB_ENDPOINT_URL` を指定してください。

### ローカル検証

Lambda 実行環境での挙動を手元で確認する場合は次のコマンドを利用します。

```bash
sam build
sam local start-api
```

起動後、`http://127.0.0.1:3000/items` のようにアクセスできます。

