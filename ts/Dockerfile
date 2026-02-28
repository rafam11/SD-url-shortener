FROM sd-url-shortener-base:latest

WORKDIR /app

COPY /ts/src /app/src/

ENV PYTHONPATH=/app/src

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "token_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
