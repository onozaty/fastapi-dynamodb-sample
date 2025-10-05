from pynamodb.attributes import NumberAttribute, UnicodeAttribute
from pynamodb.models import Model

from app.settings import settings


class ItemTable(Model):
    """PynamoDB ORMを使用したDynamoDB Itemテーブル。"""

    class Meta:  # type: ignore[misc]
        table_name = "items"
        region = settings.aws_region
        # DynamoDB LocalやmotoのendpointURL指定
        if settings.dynamodb_endpoint_url:
            host = settings.dynamodb_endpoint_url

    # プライマリキー
    id = UnicodeAttribute(hash_key=True)

    # 属性
    name = UnicodeAttribute()
    description = UnicodeAttribute(null=True)
    price = NumberAttribute()
