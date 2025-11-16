# https://docs.astral.sh/uv/guides/integration/aws-lambda/#deploying-a-docker-image

FROM ghcr.io/astral-sh/uv:0.9.2 AS uv

# First, bundle the dependencies into /var/task
FROM public.ecr.aws/docker/library/python:3.13-slim AS builder

# Enable bytecode compilation, to improve cold-start performance.
ENV UV_COMPILE_BYTECODE=1

# Disable installer metadata, to create a deterministic layer.
ENV UV_NO_INSTALLER_METADATA=1

# Enable copy mode to support bind mount caching.
ENV UV_LINK_MODE=copy

# Make uv available in the builder image.
COPY --from=uv /uv /usr/local/bin/uv

# Prepare dependency specifications.
WORKDIR /tmp/build
COPY pyproject.toml uv.lock ./

# Bundle the dependencies into /var/task via `uv pip install --target`.
# Omit any local packages (`--no-emit-workspace`) and development dependencies (`--no-dev`).
# This ensures that the Docker layer cache is only invalidated when the `pyproject.toml` or `uv.lock`
# files change, but remains robust to changes in the application code.
RUN uv export --frozen --no-emit-workspace --no-dev --no-editable -o requirements.txt && \
    uv pip install -r requirements.txt --target /var/task

FROM public.ecr.aws/docker/library/python:3.13-slim

# Copy AWS Lambda Web Adapter extension
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.9.1 /lambda-adapter /opt/extensions/lambda-adapter

# Copy the runtime dependencies from the builder stage.
COPY --from=builder /var/task /var/task

# Copy the application code.
COPY ./app /var/task/app

# Pre-compile application code to improve Lambda cold-start performance.
RUN python -m compileall -f -j 0 -q /var/task/app

# Set working directory
WORKDIR /var/task

# Add /var/task to Python path and add bin to PATH
ENV PYTHONPATH=/var/task
ENV PATH=/var/task/bin:$PATH

# Set the port for the web server
ENV PORT=8000

# Start uvicorn server
CMD exec uvicorn --host=0.0.0.0 --port=$PORT app.main:app
