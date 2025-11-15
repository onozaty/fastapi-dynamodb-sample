import time
import uuid
from typing import Awaitable, Callable

import structlog
from fastapi import FastAPI, Request, Response

from app.logger import get_logger, setup_logging
from app.routers import items

# ログ設定を初期化
setup_logging()

logger = get_logger()

app = FastAPI()

app.include_router(items.router)


@app.middleware("http")
async def log_requests(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """リクエスト/レスポンスをログに記録するミドルウェア。"""
    # LambdaのリクエストIDを取得（Lambda Web Adapterが設定するヘッダーから）
    request_id = request.headers.get("x-amzn-request-id")
    if not request_id:
        # ローカル環境: 新規UUIDを生成
        request_id = str(uuid.uuid4())

    # structlogのコンテキストにリクエストIDを設定
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(request_id=request_id)

    start_time = time.time()

    # パス+クエリパラメータを取得
    full_path = request.url.path
    if request.url.query:
        full_path += f"?{request.url.query}"

    # リクエスト情報をログ出力
    logger.info(f"Request started: {request.method} {full_path}")

    try:
        response = await call_next(request)

        # 処理時間を計算
        process_time = time.time() - start_time
        duration_ms = round(process_time * 1000)

        # レスポンス情報をログ出力
        logger.info(
            f"Request completed: {request.method} {full_path} - "
            f"{response.status_code} ({duration_ms}ms)"
        )

        return response

    except Exception as e:
        # エラー発生時の処理時間を計算
        process_time = time.time() - start_time
        duration_ms = round(process_time * 1000)

        # エラー情報をログ出力
        logger.error(
            f"Request failed: {request.method} {full_path} - "
            f"{type(e).__name__}: {str(e)} ({duration_ms}ms)",
            exc_info=True,
        )

        # 例外を再スロー
        raise
