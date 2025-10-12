from pynamodb.attributes import NumberAttribute, UnicodeAttribute
from pynamodb.models import Model

from app.settings import settings


class ItemTable(Model):
    """PynamoDB ORMを使用したDynamoDB Itemテーブル。"""

    class Meta:  # type: ignore[misc]
        table_name = settings.dynamodb_items_table_name
        if settings.dynamodb_region:
            region = settings.dynamodb_region
        if settings.dynamodb_endpoint_url:
            host = settings.dynamodb_endpoint_url
        if settings.dynamodb_aws_access_key_id:
            aws_access_key_id = settings.dynamodb_aws_access_key_id
        if settings.dynamodb_aws_secret_access_key:
            aws_secret_access_key = settings.dynamodb_aws_secret_access_key

    # プライマリキー
    id = UnicodeAttribute(hash_key=True)

    # 属性
    name = UnicodeAttribute()
    description = UnicodeAttribute(null=True)
    price = NumberAttribute()
