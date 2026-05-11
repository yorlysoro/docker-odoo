# Documentacion de Ultimos cambios realizados

## 09/05/2026

- fix(odoo_docker) Se arregla error 502 para http a la hora de quere acceder de forma manual al sistema Se agrega en el archivo docker_compose.app.yml la variable de entorno LONGPOLLING_PORT Se agrega en el .resources/db.Dockerfile el comando EXPOSE 5432 para exponer el puerto de la base de datos postgresql
