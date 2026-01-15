# Etapa 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar paquetes Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias de Python en una venv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Etapa 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias en runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copiar venv de la etapa anterior
COPY --from=builder /opt/venv /opt/venv

# Copiar código de la aplicación
COPY . .

# Configurar PATH
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Crear directorios necesarios
RUN mkdir -p /app/data /app/uploads

# Exponer puerto (ajusta según necesites)
EXPOSE 8080

# Volúmenes para persistencia
VOLUME ["/app/data", "/app/uploads"]

# Comando por defecto - mantener contenedor activo
CMD ["tail", "-f", "/dev/null"]
