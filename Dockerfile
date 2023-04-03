FROM python:3.9
WORKDIR /Desktop/AiCore/DCP/data_collection/rugby_boots/scraper.py
COPY requirements.txt .
COPY . /scraper.py
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "scraper.py"]

