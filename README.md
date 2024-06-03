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
