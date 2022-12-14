# Store-API
Flask API for Store Management


## Diectory stracture

    ├───.env.example
    ├───.flaskenv
    ├───.gitignore
    ├───app.py
    ├───blocklist.py
    ├───db.py
    ├───Dockerfile
    ├───LICENSE
    ├───README.md
    ├───requirements.txt
    ├───run.py
    ├───run.sh
    ├───schemas.py
    ├───tasks.py
    │
    ├───migrations
    │   ├───alembic.ini
    │   ├───env.py
    │   ├───README
    │   ├───script.py.mako
    │   │
    │   └───versions
    │           ├───75f43c6e0acc_.py
    │
    ├───models
    │       ├───item.py
    │       ├───item_tag.py
    │       ├───store.py
    │       ├───tag.py
    │       ├───user.py
    │       ├───__init__.py
    │
    └───resources
            ├───item.py
            ├───store.py
            ├───tag.py
            ├───user.py

## Run Locally


Clone the project

```bash
  git clone https://github.com/sidd6p/Store-API.git
```

Go to the Store-API directory
```bash
  cd Store-API
```

Install dependencies

```bash
  pip install -r requirements.txt
```

run the project

```bash
  flask run
```



## Feature

- User 
    - Registration
    - Login
    - Logout
- Store
    - Create
    - Delete
- Item
    - Create
    - Update
    - Delete
- Tag
    - Create
    - Delete
    - Link
    - Unlink




## API-Collection
[![Run in Insomnia}](https://insomnia.rest/images/run.svg)](https://insomnia.rest/run/?label=Store-API&uri=store-api)


## Tech & Tool

- __Language__: [Python](https://www.python.org/)

- __Frame-WorK__: [Flask](https://flask.palletsprojects.com/en/2.2.x/)

- __IDE__: [VS Code](https://code.visualstudio.com/)

- __API Architecture__: [RestAPI](https://restfulapi.net/)

- __API Client__: [Insomnia](https://insomnia.rest/) 

- __Documentation__: [Swagger](https://swagger.io/)
