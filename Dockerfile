FROM python:3.5
WORKDIR /app
COPY backend /app/roadAlert/
COPY manage.py requirements.txt /app/
RUN pip install -r requirements.txt
EXPOSE 8000
