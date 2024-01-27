# Python taban imajını kullan
FROM python:3.8

# Çalışma dizini olarak /app'i belirle
WORKDIR /app

# Gerekli dosyaları kopyala
COPY ./requirements.txt /app/requirements.txt
COPY ./app.py /app/app.py

# Bağımlılıkları yükle
RUN pip install --no-cache-dir -r requirements.txt

# Uygulamayı çalıştır
CMD ["python", "app.py"]