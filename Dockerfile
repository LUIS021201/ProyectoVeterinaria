FROM python:3.9

WORKDIR /app

RUN pip3 install --upgrade pip

COPY . .

RUN pip3 --no-cache install -r requirements.txt

EXPOSE 5000

CMD ["python3","app.py"]
