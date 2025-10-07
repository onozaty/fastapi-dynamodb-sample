# fastapi-dynamodb-sample

FastAPI + DynamoDB のサンプルプロジェクト

## セットアップ

依存関係のインストール:

```bash
uv sync
```

## 開発サーバー

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

### AWS CLIでの操作例

```bash
# 環境変数でダミー認証情報を設定
export AWS_ACCESS_KEY_ID=dummy
export AWS_SECRET_ACCESS_KEY=dummy

# テーブル一覧
aws dynamodb list-tables \
  --endpoint-url http://dynamodb-local:8000 \
  --region us-east-1

# テーブル定義の確認
aws dynamodb describe-table \
  --table-name items \
  --endpoint-url http://dynamodb-local:8000 \
  --region us-east-1

# テーブルの削除
aws dynamodb delete-table \
  --table-name items \
  --endpoint-url http://dynamodb-local:8000 \
  --region us-east-1
```