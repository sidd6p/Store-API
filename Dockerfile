FROM python
EXPOSE 5000
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["flask", "run", "--host", "0.0.0.0"]

