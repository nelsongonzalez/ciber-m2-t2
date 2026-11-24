# Actividad A

Descarga un contenedor de Apache desde DockerHub y haz las siguientes acciones:

## Arranca el contenedor

```bash
docker run -d \
  --name apache-server \
  -p 127.0.0.1:8080:80 \
  httpd:2.4
```

![Index.html por defecto](./screenshots/Screenshot%202026-11-24%20at%2012.13.42 AM.png)

## Modifica el HTML del index.html

El nuevo HTML es el archivo `public-html/index.html`.

## Haz un commit de los cambios y 'tagealo'

`git commit -m "Archivo index.html para Apache Web Server"`

## Arranca el nuevo contenedor y comprueba los cambios

```bash
docker run -d \
  --name apache-server \
  -p 127.0.0.1:8080:80 \
  -v "$PWD/public-html:/usr/local/apache2/htdocs:ro" \
  httpd:2.4
```

![Index.html por defecto](./screenshots/Screenshot%202026-11-24%20at%2012.28.38 AM.png)

# Actividad B

Crea una aplicación en Python que haga las funciones de calculadora.

Crea un fichero Dockerfile y haz lo siguiente:

- Utiliza una imagen alpine (en la versión que creas)
- Añade el repositorio de tu calculadora en Python a la imagen de Docker que crearás con el Dockerfile.
- Pásale variables de entorno a tu calculadora y añade dichas variables a través del Dockerfile

## Genera la imagen con tu proyecto en el interior

```bash
docker build -t sum-calculator .
```

## Levanta el contenedor

```bash
docker run --rm sum-calculator
docker run --rm -e NUM_A=12 -e NUM_B=30 sum-calculator
docker run --rm -e NUM_A=0.1 -e NUM_B=0.2 sum-calculator
```

![Creación y ejecución de la imagen](./screenshots/Screenshot%202026-11-24%20at%201.01.34 AM.png)

# Actividad C

Utilizando Docker-Compose haz lo siguiente:
- Despliega 3 contenedores
- 2 de los 3 contenedores deben tener visibilidad entre ellos
- El otro contenedor debe verse con el equipo anfitrión

```bash
docker compose up -d
docker compose ps
# retornará "servicio denegado" porque aún nos e ha configurado el servicio
docker exec sonarqube wget -qO- http://127.0.0.1:9000/api/system/status
docker exec sonarqube-db psql -U sonar -d sonar -c "SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public';"
curl -fsSi http://127.0.0.1:8081
docker compose down
```

### Qué hace cada servicio

1. `sonarqube-db` (`postgres:16.3-alpine`)
   - Ejecuta la base de datos PostgreSQL que almacena la configuración, proyectos, métricas y resultados de análisis de SonarQube (en la base de datos `sonar` con el volumen persistente `sonarqube_db_data`).
   - Incluye un `healthcheck` con `pg_isready` para avisar a Docker en cuanto PostgreSQL está listo para aceptar conexiones.
   - Está conectado únicamente a `red_interna` (`internal: true`) y **no expone puertos al equipo anfitrión**.

2. `sonarqube` (`sonarqube:lts-community`)
   - Ejecuta la plataforma de análisis estático de código y seguridad (SAST) SonarQube Community Edition.
   - Se conecta a PostgreSQL mediante JDBC usando el nombre del servicio en la red interna (`SONAR_JDBC_URL: jdbc:postgresql://sonarqube-db:5432/sonar`).
   - Al igual que `sonarqube-db`, está únicamente en `red_interna` (`internal: true`) y sin puertos publicados hacia el anfitrión, garantizando que ambos contenedores tengan visibilidad entre sí pero queden aislados del exterior y del tercer contenedor.

3. `web-anfitrion` (`httpd:2.4`)
   - Ejecuta un servidor web Apache que sirve el contenido estático local de [index.html](file:///Users/nelson/Workspace/ciberseguridad/ciber-m2-t2/public-html/index.html) en modo solo lectura (`:ro`).
   - Está conectado a una red independiente (`red_anfitrion`) y publica su puerto `80` en `127.0.0.1:8081` del equipo anfitrión (además de declarar `host.docker.internal:host-gateway`), de modo que se comunica con el equipo anfitrión pero no tiene acceso a `red_interna`.
