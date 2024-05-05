FROM python:3.9
RUN mkdir /fastapi_app
WORKDIR /fastapi_app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
CMD gunicorn main_:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
#CMD["python", "parser.py"]