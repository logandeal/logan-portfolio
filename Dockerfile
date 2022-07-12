FROM quay.io/centos/centos:stream8

RUN dnf install -y python3.9

WORKDIR /logan-portfolio

COPY . .

RUN pip3 install -r requirements.txt

CMD ["flask", "run", "--host=0.0.0.0"]

EXPOSE 5000