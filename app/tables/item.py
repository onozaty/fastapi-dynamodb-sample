from pynamodb.attributes import NumberAttribute, UnicodeAttribute
from pynamodb.models import Model

from app.settings import settings


class ItemTable(Model):
    """PynamoDB ORMを使用したDynamoDB Itemテーブル。"""

    class Meta:  # type: ignore[misc]
        table_name = settings.items_table_name
        if settings.aws_region:
            region = settings.aws_region
        if settings.dynamodb_endpoint_url:
            host = settings.dynamodb_endpoint_url
        if settings.aws_access_key_id:
            aws_access_key_id = settings.aws_access_key_id
        if settings.aws_secret_access_key:
            aws_secret_access_key = settings.aws_secret_access_key

    # プライマリキー
    id = UnicodeAttribute(hash_key=True)

    # 属性
    name = UnicodeAttribute()
    description = UnicodeAttribute(null=True)
    price = NumberAttribute()
