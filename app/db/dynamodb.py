from app.tables.item import ItemTable


def ensure_all_tables_exist() -> None:
    """Ensure all DynamoDB tables exist, create if not."""

    # TODO: 運用環境で使う場合には、Tableの作成は別途行った方が良い
    if not ItemTable.exists():
        ItemTable.create_table(
            read_capacity_units=1,
            write_capacity_units=1,
            wait=True,
        )
