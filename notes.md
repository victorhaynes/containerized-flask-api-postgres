1) Create venv
```
$ python3 -m venv <name>
$ source <name>/bin/activate
```

2) create app.py
3) write basic API
4) install packages
5) pip freeze requirements
6) Dockerfile
7) Docker Compose YML file
8) `$ docker compose up -d <name_of_db_service>` to build database container
9) Check if database is running (i.e. postgres) `$ docker exec -it <name_of_db_service> psql -U postgres`
10) Build python app/api container `$ docker compose up --build <name_of_api_service>`