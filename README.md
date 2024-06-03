# ZBD
Zaawansowane Bazy Danych


Wdrożenie bazy danych SurrealDB na fly.io przeprowadza się w następujący sposób. \
W pierwszej kolejności należy zainstalować klienta fly.io flyctl (https://fly.io/docs/hands-on/install-flyctl/)  \
Następnie należy założyć nowy katalog z plikami dotyczącymi wdrożenia:

```console
mkdir surrealdb && cd surrealdb
```

Zawartość pliku Dockerfile:

```console
FROM surrealdb/surrealdb:latest
EXPOSE 8080
CMD ["start", "--bind", "0.0.0.0:8080", "file://data/srdb.db"]
```

Następnie należy wygenerować plik fly.toml i podczas generacji podać unikalną nazwę naszej bazy (przykładowo moja-baza), oraz wygenerować nowy wolumen:

```console
fly launch --no-deploy
fly volumes create data --region <region> --size 1
```

Zawartość pliku fly.toml powinna wyglądać następująco:

```console
app = 'moja-baza'
primary_region = 'waw'

[build]

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0
  processes = ['app']

[[vm]]
  memory = '1gb'
  cpu_kind = 'shared'
  cpus = 1

[mounts]
source="data"
destination="/data"
```

Należy podać dane do uwierzytelniania jako sekrety:

```console
fly secrets set SURREAL_USER="..."
fly secrets set SURREAL_PASS="..."
```

Gdy wszystko już jest gotowe, następująca komenda umożliwi wdrożenie bazy SurrealDB na serwer fly.io:

```console
fly deploy
```

Po wdrożeniu możemy zobaczyć stan naszej bazy pod adresem https://fly.io/apps/moja-baza \
Komunikacja z bazą danych odbywa się poprzez zapytania HTTP pod adres https://moja-baza.fly.dev \
Dokumentacja do komunikacji znajduje się pod adresem https://surrealdb.com/docs/surrealdb/integration/http \
Aby skutecznie wysyłać zapytania do bazy danych, należy w zapytaniu podać dane do uwierzytelniania (te, które ustaliliśmy jako sekrety przed wdrożeniem) oraz dla headerów 'ns' i 'db' ustalić i podać (dowolne) nazwy namespace i database, z których chcemy korzystać podczas pracy z aplikacją, którą budujemy. \

Więcej szczegółów na temat wdrożenia SurrealDB w fly.io można znaleźć pod adresem https://surrealdb.com/docs/surrealdb/deployment/fly

## Wdrożenie Frontendu i Backendu

Po postawieniu bazy danych możemy przejsc do postawienia aplikacji, którą możemy postawić lokalnie lub na azure

### Postawienie lokalnie

Żeby lokalnie uruchomic aplikacje będziemy potrzebować Dockera zaintsalowanego na naszym komputerze natsepnie trzeba uruchomic nastepujace komendy budujace nam obrazy:

```console
docker build --build-arg REACT_APP_API_URL=%backend-url% -t frontend Frontend/tournament/.
docker build --build-arg SURREALDB_URL=%https://moja-baza.fly.dev% --build-arg SUERREALDB_LOGIN=%SURREAL_USER% --build-arg SUERREALDB_PASSWORD=%SURREAL_PASS% --build-arg SUERREALDB_NS=%Twój-namespace% --build-arg SUERREALDB_DB=%Twój-database% -t backend Backend/.
```

Oczywiście zmienne przy budowaniu obrazów nalezy dodać własne zmienne.
Po czym:

```console
docker run -p 3000:3000 --name frontend frontend
docker run -p 8000:8000 --name backend backend
```
