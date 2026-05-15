FROM python:3.8
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
# Run as root (no USER directive)
EXPOSE 5000
CMD ["python", "payment_handler.py"]
