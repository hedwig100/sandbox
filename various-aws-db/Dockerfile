FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir "boto3==1.34.*" "pydantic==2.*"

COPY app.py dynamo.py ./

ENV PORT=8080
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1

CMD ["python", "app.py"]
