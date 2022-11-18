FROM python
EXPOSE 5000
WORKDIR /app
COPY requirements.text .
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]

