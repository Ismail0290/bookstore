FROM python:3.13-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY req.txt /code/

RUN pip install --no-cache-dir -r req.txt

COPY . /code/

CMD ["gunicorn","bookstore.wsgi:application", "--bind", "0.0.0.0:8000"]