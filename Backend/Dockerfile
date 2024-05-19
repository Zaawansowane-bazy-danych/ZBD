FROM python:latest

WORKDIR /app    

COPY . /app


RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8000

CMD ["python", "start.py"]