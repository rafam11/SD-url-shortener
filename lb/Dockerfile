FROM sd-url-shortener-base:latest

WORKDIR /app

COPY /lb/src /app/src/

ENV PYTHONPATH=/app/src

EXPOSE 8080

CMD ["python", "-m", "uvicorn", "load_balancer.main:app", "--host", "0.0.0.0", "--port", "8080"]
