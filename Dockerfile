FROM python:3.8

WORKDIR /code
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app /code/app
# EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]