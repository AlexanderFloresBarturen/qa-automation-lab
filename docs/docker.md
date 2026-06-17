# Docker y PostgreSQL

## Objetivo

Desplegar PostgreSQL en una máquina virtual Ubuntu utilizando Docker y Docker Compose, manteniendo el servicio accesible únicamente a través de una interfaz de red Host-Only.

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

## Lecciones Aprendidas

* Docker permite desplegar PostgreSQL sin instalarlo directamente en Ubuntu.
* Docker Compose simplifica la gestión del contenedor.
* Una interfaz Host-Only proporciona aislamiento de red adecuado para laboratorios.
* Mantener bases de datos separadas para desarrollo y testing reduce riesgos.
* PostgreSQL en Docker se aproxima más a un entorno real que SQLite.
