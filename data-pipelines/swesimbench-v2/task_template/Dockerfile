FROM python:3.12-slim
RUN pip install --no-cache-dir --quiet urllib3 >/dev/null 2>&1 || true
WORKDIR /sim
COPY sim/ /sim/
# tests/ is mounted by the harness at verification time
