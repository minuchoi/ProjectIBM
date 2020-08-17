FROM python:3.8
LABEL maintainer "Minu Choi <7176choi@gmail.com>"

COPY requirements.txt /
RUN pip3 install -r /requirements.txt
COPY ./ ./

EXPOSE 80

CMD ["python", "app.py"]


