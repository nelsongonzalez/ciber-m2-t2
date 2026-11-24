FROM alpine:3.21

RUN apk add --no-cache python3 \
    && adduser -D appuser

WORKDIR /app

COPY calculator/calculator.py /app/calculator.py

ENV NUM_A=0 \
    NUM_B=0

USER appuser

ENTRYPOINT ["python3", "/app/calculator.py"]
