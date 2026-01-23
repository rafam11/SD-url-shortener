FROM sd-url-shortener-base:latest

WORKDIR /app

RUN apt-get update \
    && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

COPY /kgs/src /app/src/

ENV PYTHONPATH=/app/src

EXPOSE 8001

CMD ["python", "-m", "uvicorn", "kgs.main:app", "--host", "0.0.0.0", "--port", "8001"]