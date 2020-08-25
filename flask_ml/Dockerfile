FROM python:3.7.6-buster
WORKDIR /flask_ml
COPY . /flask_ml
RUN pip install -U -r requirements.txt
EXPOSE 8080
CMD ["python", "ml_app.py"]
