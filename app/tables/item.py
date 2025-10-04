from pynamodb.attributes import NumberAttribute, UnicodeAttribute
from pynamodb.models import Model

from app.settings import settings


class ItemTable(Model):
    """DynamoDB Item table using PynamoDB ORM."""

    class Meta:  # type: ignore[misc]
        table_name = "items"
        region = settings.aws_region
        # DynamoDB LocalやmotoのendpointURL指定
        if settings.dynamodb_endpoint_url:
            host = settings.dynamodb_endpoint_url

    # Primary key
    id = UnicodeAttribute(hash_key=True)

    # Attributes
    name = UnicodeAttribute()
    description = UnicodeAttribute(null=True)
    price = NumberAttribute()
