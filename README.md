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
