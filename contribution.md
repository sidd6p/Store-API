```
docker build -t flask_restapi:v1 .
```

```
docker run -dp 80:80 -w /app -v "$(pwd):/app" flask_restapi:v1 sh -c "flask run --host 0.0.0.0"
```
