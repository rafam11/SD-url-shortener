FROM sd-url-shortener-base:latest

WORKDIR /app

COPY ./api/src /app/src
COPY ./api/tests /app/tests

ENV PYTHONPATH=/app/src

RUN pytest \
    --cov=app \
    --cov-report=term-missing \
    --cov-report=xml

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]