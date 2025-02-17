from python=3.12-slim

RUN pip install --upgrade pip setuptools wheel

RUN pip install -r requirements.txt

CMD ["python", "app.py"]