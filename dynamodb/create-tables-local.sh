#!/bin/bash

# DynamoDB Localにテーブルを作成するスクリプト

# Bashで実行されているかチェック
if [ -z "$BASH_VERSION" ]; then
    echo "エラー: このスクリプトはBashで実行する必要があります。"
    echo "以下のコマンドで実行してください:"
    echo "  bash ./dynamodb/create-tables-local.sh"
    exit 1
fi

set -e

# DynamoDB Localのエンドポイント設定
ENDPOINT_URL="http://dynamodb-local:8000"
REGION="us-east-1"

# スクリプトのディレクトリを取得
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TABLE_DEFINITIONS_DIR="${SCRIPT_DIR}/table-definitions"

echo "DynamoDB Localにテーブルを作成します..."
echo "エンドポイント: ${ENDPOINT_URL}"
echo "リージョン: ${REGION}"
echo ""

# AWS認証情報の設定(DynamoDB Localではダミーでよい)
export AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID:-dummy}
export AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY:-dummy}

# テーブル定義ファイルを順に処理
for table_file in "${TABLE_DEFINITIONS_DIR}"/*.json; do
    if [ -f "$table_file" ]; then
        table_name=$(basename "$table_file" .json)
        echo "テーブル '${table_name}' を作成中..."

        # テーブルが既に存在するかチェック
        if aws dynamodb describe-table \
            --table-name "${table_name}" \
            --endpoint-url "${ENDPOINT_URL}" \
            --region "${REGION}" \
            --output json > /dev/null 2>&1; then
            echo "  ⚠️  テーブル '${table_name}' は既に存在します(スキップ)"
        else
            # テーブルを作成
            aws dynamodb create-table \
                --cli-input-json "file://${table_file}" \
                --endpoint-url "${ENDPOINT_URL}" \
                --region "${REGION}" \
                --output json > /dev/null
            echo "  ✅ テーブル '${table_name}' を作成しました"
        fi
    fi
done

echo ""
echo "完了！テーブル一覧:"

# jqが利用可能な場合はそれを使い、なければtable形式で表示
if command -v jq > /dev/null 2>&1; then
    aws dynamodb list-tables \
        --endpoint-url "${ENDPOINT_URL}" \
        --region "${REGION}" \
        --output json | jq -r '.TableNames[]'
else
    aws dynamodb list-tables \
        --endpoint-url "${ENDPOINT_URL}" \
        --region "${REGION}" \
        --output table
fi
