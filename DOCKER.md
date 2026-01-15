# 🐳 Guía de Docker para Syncord

Este documento explica cómo usar Docker para ejecutar Syncord de forma aislada en tu sistema.

## 📋 Requisitos

- Docker instalado ([descargar aquí](https://www.docker.com/products/docker-desktop))
- Docker Compose (incluido en Docker Desktop)

## 🚀 Ejecución Rápida

### Con Docker Compose (Recomendado)

```bash
# Construir y levantar el contenedor
docker-compose up -d

# Ver logs
docker-compose logs -f syncord

# Detener el contenedor
docker-compose down
```

### Con Docker directamente

```bash
# Construir la imagen
docker build -t syncord:latest .

# Ejecutar el contenedor
docker run -d \
  --name syncord-app \
  -v syncord-data:/app/data \
  -v syncord-uploads:/app/uploads \
  -p 8080:8080 \
  syncord:latest

# Ver logs
docker logs -f syncord-app

# Detener el contenedor
docker stop syncord-app
docker rm syncord-app
```

## 📁 Volúmenes y Persistencia

El `docker-compose.yml` crea dos volúmenes para mantener los datos persistentes:

- **`syncord-data`**: Almacena la base de datos y configuración
- **`syncord-uploads`**: Almacena archivos subidos/descargados

Para acceder a estos volúmenes:

```bash
# Listar volúmenes
docker volume ls

# Inspeccionar un volumen
docker volume inspect syncord-data

# Eliminar volúmenes (cuidado, se pierden los datos)
docker volume rm syncord-data syncord-uploads
```

## ⚙️ Configuración

### Variables de Entorno

Puedes agregar variables de entorno en `docker-compose.yml`:

```yaml
environment:
  - DISCORD_TOKEN=tu_token_aqui
  - ENCRYPTION_KEY=tu_clave_aqui
  - GUILD_ID=tu_guild_id_aqui
```

### Archivo de Configuración

Para usar `setup.yaml`, descomenta y ajusta el volumen en `docker-compose.yml`:

```yaml
volumes:
  - ./setup.yaml:/app/setup.yaml
```

## 🔧 Comandos Útiles

### Ejecutar comandos dentro del contenedor

```bash
# Acceder a la shell del contenedor
docker-compose exec syncord bash

# Ejecutar un comando específico
docker-compose exec syncord python main.py --help
```

### Ver estado y recursos

```bash
# Ver procesos en ejecución
docker-compose ps

# Ver consumo de recursos
docker stats syncord-app
```

### Reconstruir la imagen

```bash
# Forzar reconstrucción (útil después de cambios)
docker-compose build --no-cache
docker-compose up -d
```

## 📊 Monitoreo

### Logs

```bash
# Ver todos los logs
docker-compose logs syncord

# Últimas 100 líneas
docker-compose logs --tail=100 syncord

# En tiempo real
docker-compose logs -f syncord

# Con timestamps
docker-compose logs -f --timestamps syncord
```

### Estadísticas en Vivo

```bash
docker stats syncord-app
```

## 🛑 Limpieza

```bash
# Detener todos los servicios
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v

# Eliminar imagen
docker rmi syncord:latest

# Limpieza completa (⚠️ elimina TODO de Docker)
docker system prune -a
```

## 🔐 Seguridad

- El Dockerfile usa una **multi-stage build** para reducir el tamaño de la imagen
- Los datos están aislados en volúmenes Docker
- Las dependencias se validan contra `requirements.txt`

## 📦 Distribución

Para compartir tu aplicación:

```bash
# Guardar imagen como archivo
docker save syncord:latest | gzip > syncord-latest.tar.gz

# Cargar imagen desde archivo
docker load < syncord-latest.tar.gz

# Subir a Docker Hub (necesitas cuenta)
docker tag syncord:latest tu_usuario/syncord:latest
docker push tu_usuario/syncord:latest
```

## 🐛 Solución de Problemas

### El contenedor se detiene inmediatamente

```bash
# Ver el error
docker-compose logs syncord
```

### Puerto 8080 ya está en uso

Cambia el puerto en `docker-compose.yml`:
```yaml
ports:
  - "8081:8080"  # Cambiar a otro puerto
```

### Permisos denegados

```bash
# En Linux, ejecutar con sudo o agregar usuario a grupo docker
sudo usermod -aG docker $USER
```

### Espacio en disco

```bash
# Ver uso de Docker
docker system df

# Limpiar imágenes/contenedores no usados
docker system prune
```

## 📚 Referencias

- [Documentación oficial de Docker](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Best Practices for Python Docker](https://docs.docker.com/language/python/build-images/)
