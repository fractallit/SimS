FROM python:3.14

COPY requirements.txt .

RUN apt-get update && apt-get install -y ffmpeg

RUN pip install --upgrade setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /src

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--threads", "2", "app:app"]
