FROM python:3-slim
WORKDIR /project/horarios
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python3", "./horarios.py"]
