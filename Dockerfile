FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY requirements.txt .

#COPY ./model /model/

COPY ./app.py .

RUN pip install -r requirements.txt

EXPOSE 8008

CMD ["python", "app.py"]