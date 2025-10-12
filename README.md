# fastapi-dynamodb-sample

FastAPI + DynamoDB のサンプルプロジェクトです。

## 必要な環境

このプロジェクトは [Dev Container](https://containers.dev/) 環境で動作します。  
VS Code の Dev Containers 拡張機能を使用すると、以下が自動的にセットアップされます。

- Python 3.13
- uv
- AWS CLI
- AWS SAM CLI
- Docker CLI
- DynamoDB Local (自動起動)

**必要なもの:**
- Docker ([Docker Desktop](https://www.docker.com/products/docker-desktop/) など)
- [VS Code](https://code.visualstudio.com/)
- [Dev Containers 拡張機能](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

## ローカル開発環境のセットアップ

### 1. 依存関係のインストール

```bash
uv sync
```

### 2. DynamoDB Localの起動とテーブル作成

Dev Container環境ではDynamoDB Localが自動的に起動します (`http://dynamodb-local:8000`)。

テーブルを作成:

```bash
bash ./dynamodb/create-tables-local.sh
```

### 3. 開発サーバーの起動

```bash
uv run fastapi dev
```

起動後、 http://127.0.0.1:8000/docs にアクセスするとAPI仕様を確認できます。

## 開発ツール

### テスト

```bash
uv run pytest
```

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

## DynamoDB Localについて

開発環境ではDynamoDB Localが起動しています:

- **エンドポイント**: `http://dynamodb-local:8000`
- **リージョン**: `ap-northeast-1` (設定値、実際のリージョンではありません)
- **認証情報**: ダミー値 (`dummy`) で動作します

### テーブルの作成

```bash
bash ./dynamodb/create-tables-local.sh
```

このスクリプトは `dynamodb/table-definitions/` ディレクトリ内のJSON定義ファイルを読み込み、テーブルを作成します。

### AWS CLIでの操作

DynamoDB Localに対してAWS CLIでテーブル操作を行う例:

```bash
# テーブル一覧を確認
aws dynamodb list-tables \
  --endpoint-url http://dynamodb-local:8000 \
  --region ap-northeast-1

# テーブル定義を確認
aws dynamodb describe-table \
  --table-name items \
  --endpoint-url http://dynamodb-local:8000 \
  --region ap-northeast-1

# テーブルを削除
aws dynamodb delete-table \
  --table-name items \
  --endpoint-url http://dynamodb-local:8000 \
  --region ap-northeast-1
```

**注意**: DynamoDB Localへのアクセスには認証情報が不要ですが、AWS CLIの仕様上、環境変数に何らかの値を設定する必要があります。

```bash
export AWS_ACCESS_KEY_ID=dummy
export AWS_SECRET_ACCESS_KEY=dummy
```

## AWSへのデプロイ (AWS SAM)

このプロジェクトは、AWS SAM を使用してコンテナイメージとして AWS Lambda にデプロイできます。  
SAM CLI が、コンテナイメージのビルド・ECR へのプッシュ・API Gateway/Lambda/DynamoDB テーブルの作成を一括で行います。

### 前提条件

AWS認証情報が設定されていることを確認してください。  
設定方法は [AWS CLI の設定](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) を参照してください。

### デプロイ手順

#### 1. ビルド

```bash
sam build
```

#### 2. 初回デプロイ (ガイド付き)

初回デプロイ時は `--guided` オプションを使用して、対話形式で設定を行います:

```bash
sam deploy --guided
```

設定例:

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

設定は `samconfig.toml` に保存されます。

#### 3. 2回目以降のデプロイ

設定が保存されているため、以下のコマンドだけでデプロイできます。

```bash
sam build
sam deploy
```

#### 4. デプロイ完了後

デプロイ完了後、出力される `ApiEndpoint` の値がAPI Gateway のエンドポイントURLです。  
例: `https://xxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/`

このURLに `/items/` などのパスを追加してアクセスすることで、FastAPI アプリを利用できます。

**API仕様の確認:**  
エンドポイントURLに `/docs` を追加すると、FastAPIの自動生成ドキュメント(Swagger UI)にアクセスできます。  
例: `https://xxxxxxxxxx.execute-api.ap-northeast-1.amazonaws.com/docs`

### DynamoDB テーブルの設定

- ローカル開発環境では、環境変数 `DYNAMODB_ITEMS_TABLE_NAME` が未設定の場合、デフォルトで `items` テーブル名を使用します
- AWS環境では、SAM テンプレートが `fastapi-dynamodb-sample-items` という名前でテーブルを作成し、その名前を環境変数 `DYNAMODB_ITEMS_TABLE_NAME` として Lambda 関数に渡します
