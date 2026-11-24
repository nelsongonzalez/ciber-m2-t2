# Descarga un contenedor de Apache desde DockerHub y haz las siguientes acciones:

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
