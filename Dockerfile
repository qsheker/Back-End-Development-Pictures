FROM python:3.11-slim
WORKDIR /opt/app-root/src
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
USER 1001
EXPOSE 3000
CMD ["gunicorn", "--bind", "0.0.0.0:3000", "--workers", "1", "--threads", "4", "app:app"]
