import logging

import structlog
from structlog.typing import EventDict, FilteringBoundLogger

from app.settings import settings


def _order_keys(
    logger: FilteringBoundLogger, method_name: str, event_dict: EventDict
) -> EventDict:
    """ログフィールドの順序を制御するプロセッサ。

    出力順序: timestamp -> level -> request_id -> event -> その他
    """
    ordered = {}

    # 優先順位に従ってキーを追加
    if "timestamp" in event_dict:
        ordered["timestamp"] = event_dict.pop("timestamp")
    if "level" in event_dict:
        ordered["level"] = event_dict.pop("level")
    if "request_id" in event_dict:
        ordered["request_id"] = event_dict.pop("request_id")
    if "event" in event_dict:
        ordered["event"] = event_dict.pop("event")

    # 残りのキーを追加
    ordered.update(event_dict)

    return ordered


def _custom_text_renderer(
    logger: FilteringBoundLogger, method_name: str, event_dict: EventDict
) -> str:
    """カスタムテキストレンダラー。

    フォーマット: timestamp [level] (request_id) event key1=value1 key2=value2
    """
    timestamp = event_dict.pop("timestamp", "")
    level = event_dict.pop("level", "")
    request_id = event_dict.pop("request_id", None)
    event = event_dict.pop("event", "")

    # 基本フォーマット
    parts = [timestamp, f"[{level:5}]"]

    # request_idがあれば追加
    if request_id:
        parts.append(f"({request_id})")

    # イベントメッセージ
    parts.append(event)

    # 残りのキーをkey=value形式で追加
    for key, value in event_dict.items():
        if key == "exception":
            # 例外は最後に改行して表示
            continue
        parts.append(f"{key}={value}")

    log_line = " ".join(parts)

    # 例外情報があれば追加
    if "exception" in event_dict:
        log_line += f"\n{event_dict['exception']}"

    return log_line


def setup_logging() -> None:
    """ログ設定を初期化する。

    - Uvicornのアクセスログを抑止
    - structlogの出力形式を設定(JSON or テキスト)
    - ログレベルをINFOに設定

    環境変数LOG_FORMATで出力形式を制御:
    - "text": 人間が読みやすいテキスト形式(ローカル開発用)
    - "json": JSON形式(デフォルト、本番環境用)
    """
    # Uvicornのアクセスログを抑止
    logging.getLogger("uvicorn.access").handlers.clear()

    # ログ形式に応じてレンダラーを選択
    if settings.log_format.lower() == "text":
        renderer = _custom_text_renderer
    else:
        renderer = structlog.processors.JSONRenderer()

    # structlogの設定
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.ExceptionRenderer(),
            _order_keys,
            renderer,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=False,
    )


def get_logger() -> FilteringBoundLogger:
    """設定済みのloggerインスタンスを取得する。

    Returns:
        FilteringBoundLogger: 構造化ログ用のloggerインスタンス
    """
    return structlog.get_logger()
