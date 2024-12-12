FROM python:3.12.4

LABEL maintainer="razmaz112 retraz123@gmail.com"
LABEL description="Backend service for party manager project"

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "party_manager.wsgi:application"]