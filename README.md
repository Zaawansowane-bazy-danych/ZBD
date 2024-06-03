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

Następnie należy wygenerować plik fly.toml i podczas generacji podać unikalną nazwę naszej bazy (przykładowo tournamentdb-deployment), oraz wygenerować nowy wolumen:

```console
fly launch --no-deploy
fly volumes create data --region <region> --size 1
```

Zawartość pliku fly.toml powinna wyglądać następująco:

```console
app = 'tournamentdb-deployment'
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

Należy podać dane do uwierzytelniania:

```console
fly secrets set SURREAL_USER="..."
fly secrets set SURREAL_PASS="..."
```

Gdy wszystko już jest gotowe, następująca komenda umożliwi wdrożenie bazy SurrealDB na serwer fly.io:

```console
fly deploy
```
