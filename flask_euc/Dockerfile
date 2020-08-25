FROM python:3.7.6-buster
WORKDIR /flask_euc
COPY . /flask_euc
RUN pip install -U -r requirements.txt
EXPOSE 80:80
CMD ["python","euc_app.py"]
