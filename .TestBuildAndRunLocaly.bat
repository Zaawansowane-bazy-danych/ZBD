docker rm -f backend
docker rmi -f backend
docker build -t backend Backend/.
docker run -e SURREALDB_URL=https://tournamentdb-deployment.fly.dev/sql -e SUERREALDB_LOGIN=tournamentadmin -e SUERREALDB_PASSWORD=RubiksCube420 -e SUERREALDB_NS=tournament -e SUERREALDB_DB=tournament -p 8000:8000 --name backend backend