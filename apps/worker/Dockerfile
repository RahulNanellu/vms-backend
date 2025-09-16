FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY worker.py .
COPY jobs.py ./apps/worker/jobs.py
ENV PYTHONUNBUFFERED=1
CMD ["rq", "worker", "-u", "redis://redis:6379/0", "ptt_high", "ptt_norm", "ptt_low"]
