FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY PageLoad.py urllist.json ./
CMD ["python", "PageLoad.py"]