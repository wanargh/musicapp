FROM python:3.7-alpine
    WORKDIR /music
    COPY . /music
    RUN pip install -U -r requirements.txt
    EXPOSE 8080
    CMD ["python", "musicapp.py"]
