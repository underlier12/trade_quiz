# FROM registry.access.redhat.com/ubi8/python-38
FROM python:3.9.6-buster

COPY . .

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN apt-get install -y tesseract-ocr tesseract-ocr-kor

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "flask" ]

CMD ["run", "--host", "0.0.0.0"]