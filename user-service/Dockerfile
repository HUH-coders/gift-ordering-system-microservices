# Dockerfile
FROM python:3.9
WORKDIR /run
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5001"]