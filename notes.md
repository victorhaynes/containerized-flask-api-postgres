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

11a) 
11b) log into AWS `$ aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 144816010913.dkr.ecr.us-east-2.amazonaws.com`

12) tag
13) push

14) when creating ECS instance change the "db" service name in the DATABASE_URI environment variable to the host URL/RDS for the data base `i.e. db -> database-1.cyuqsci5tfzs.us-east-2.rds.amazonaws.com `

15) once service is created, view service, go to task, get public IP
16) update task JSON configuration form ARM architecture/apple M1 chip
17) update JSON configuration for whatever version of image that has been uploaded in "image" key

18 hit API at this IP address `3.135.200.4`


https://www.youtube.com/watch?v=QEaM4b3AliY
https://www.youtube.com/watch?v=8rj5LzMPvQw&t=209s
