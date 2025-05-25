########################   builder stage   ########################
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create virtual-env & install requirements
WORKDIR /install
COPY requirements.txt .
RUN python -m venv /venv \
 && /venv/bin/pip install --upgrade pip \
 && /venv/bin/pip install --no-cache-dir -r requirements.txt


########################   runtime stage   ########################
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/venv/bin:$PATH"

WORKDIR /app
COPY --from=builder /venv /venv
COPY . .

EXPOSE 8050

CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:server"]