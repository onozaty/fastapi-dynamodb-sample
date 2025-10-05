from app.tables.item import ItemTable


def ensure_all_tables_exist() -> None:
    """全てのDynamoDBテーブルが存在することを確認し、存在しない場合は作成する。"""

    # TODO: 運用環境で使う場合には、Tableの作成は別途行った方が良い
    if not ItemTable.exists():
        ItemTable.create_table(
            read_capacity_units=1,
            write_capacity_units=1,
            wait=True,
        )
