FROM python:3-slim
WORKDIR /project/users
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python3", "./users.py"]
