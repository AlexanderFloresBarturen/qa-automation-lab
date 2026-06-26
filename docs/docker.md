> **Documento:** Docker  
> **Proyecto:** QA Automation Lab  
> **Última actualización:** Sprint 4  
> **Estado:** Vigente

# Docker

## Objetivo

Este documento describe la infraestructura Docker utilizada por el proyecto y proporciona los pasos necesarios para preparar el entorno de desarrollo.

Además de explicar la arquitectura utilizada, incluye la instalación, configuración y administración del contenedor PostgreSQL empleado por el laboratorio.

---

## ¿Por qué utilizar Docker?

El proyecto utiliza Docker para desacoplar la infraestructura del sistema operativo del desarrollador y garantizar que cualquier persona pueda levantar el mismo entorno de desarrollo independientemente de su plataforma.

Docker elimina diferencias de configuración entre equipos y simplifica la preparación del laboratorio, especialmente durante las primeras etapas del proyecto.

---

## Arquitectura

```text
Windows
│
├── FastAPI
├── Pytest
└── Cliente PostgreSQL
     │
     ▼
Ubuntu VM
│
└── Docker
     │
     └── PostgreSQL
```

La comunicación entre Windows y Ubuntu se realiza mediante una interfaz Host-Only de VirtualBox.

---

## Flujo General

El entorno de desarrollo sigue el siguiente flujo:

```text
Docker Compose
      │
      ▼
PostgreSQL
      │
      ▼
Alembic
      │
      ▼
FastAPI
      │
      ▼
Pytest
```

Docker proporciona únicamente la infraestructura necesaria para ejecutar el resto de componentes del laboratorio.

---

## Requisitos

### Ubuntu

Verificar versión:

```bash
lsb_release -a
```

Verificar recursos:

```bash
free -h
df -h
```

---

## Instalación de Docker

Actualizar repositorios:

```bash
sudo apt update
```

Instalar Docker:

```bash
sudo apt install docker.io -y
```

Verificar instalación:

```bash
docker --version
```

Iniciar servicio:

```bash
sudo systemctl enable docker
sudo systemctl start docker
```

Agregar usuario al grupo docker:

```bash
sudo usermod -aG docker $USER
```

Cerrar sesión y volver a ingresar.

Verificar:

```bash
docker ps
```

---

## Instalación de Docker Compose

Instalar plugin oficial:

```bash
sudo apt install docker-compose-v2 -y
```

Verificar:

```bash
docker compose version
```

---

## Configuración de Red

Se agregó una segunda interfaz de red a la máquina virtual:

```text
Adaptador Host-Only
```

Dirección utilizada:

```text
192.168.56.2
```

PostgreSQL fue configurado para escuchar únicamente en esta interfaz.

Beneficios:

* No se expone PostgreSQL a Internet.
* Acceso únicamente desde el host.
* Entorno aislado para laboratorio.

---

## Estructura del Proyecto

```text
postgres/
│
├── docker-compose.yml
└── data/
```

---

## docker-compose.yml

Ejemplo utilizado:

```yaml
services:
  postgres:
    image: postgres:17
    container_name: postgres-lab

    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: users

    ports:
      - "192.168.56.2:5432:5432"

    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## Inicio del Contenedor

Levantar servicio:

```bash
docker compose up -d
```

Verificar:

```bash
docker ps
```

Detener:

```bash
docker compose down
```

---

## Bases de Datos

### Desarrollo

```text
users
```

### Testing

```text
users_test
```

---

## Usuarios

### Administrador

```text
postgres
```

---

## Conexión desde Windows

Cadena de conexión de desarrollo:

```text
postgresql+psycopg://postgres:postgres@192.168.56.2:5432/users
```

Cadena de conexión de testing:

```text
postgresql+psycopg://postgres:postgres@192.168.56.2:5432/users_test
```

---

## Comandos Útiles

Ver contenedores:

```bash
docker ps
```

Ver logs:

```bash
docker logs postgres-lab
```

Entrar al contenedor:

```bash
docker exec -it postgres-lab bash
```

Abrir PostgreSQL:

```bash
docker exec -it postgres-lab psql -U postgres
```

Listar bases de datos:

```sql
\l
```

Listar tablas:

```sql
\dt
```

Descripción de una tabla:

```sql
\d users
```

Salir:

```sql
\q
```

---

## Buenas Prácticas

* No modificar la configuración manualmente dentro del contenedor.
* Gestionar el esquema mediante Alembic.
* Mantener la configuración centralizada mediante Settings.
* Versionar docker-compose.yml.
* No almacenar datos persistentes fuera de los volúmenes Docker.

---

## Evolución Futura

* Contenerización completa de FastAPI.
* Docker Compose con todos los servicios.
* Variables mediante .env.
* Integración con GitHub Actions.
* Ejecución de pruebas dentro de contenedores.

---

## Conclusiones

Docker proporciona una infraestructura reproducible y desacoplada del sistema operativo del desarrollador.

La combinación de Docker, Alembic y la configuración centralizada mediante Settings permite preparar un entorno de desarrollo consistente, facilitando tanto el desarrollo diario como la ejecución de pruebas automatizadas.