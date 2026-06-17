# Alembic y Gestión de Esquema

## Objetivo

Gestionar la evolución del esquema de base de datos mediante migraciones versionadas.

Alembic permite:

* Versionar cambios de estructura.
* Mantener historial de modificaciones.
* Aplicar cambios de forma controlada.
* Revertir cambios cuando sea necesario.
* Sincronizar entornos de desarrollo y testing.

---

## ¿Por qué Alembic?

Inicialmente el proyecto utilizaba:

```python
Base.metadata.create_all(bind=engine)
```

Este mecanismo permite crear tablas nuevas, pero no gestiona cambios posteriores sobre tablas existentes.

Ejemplo:

```python
phone = Column(String)
```

Agregar esta columna al modelo no modifica automáticamente una tabla ya existente en PostgreSQL.

Para resolver este problema se introdujo Alembic.

---

## Conceptos Fundamentales

### Modelo SQLAlchemy

Define la estructura deseada:

```python
class UserModel(Base):
    ...
```

---

### Migración

Representa un cambio concreto sobre el esquema.

Ejemplo:

```python
op.add_column(...)
```

---

### Revision

Archivo que contiene una migración.

Ejemplo:

```text
42asca24sa_initial_schema.py
```

---

### Upgrade

Aplica cambios al esquema.

```bash
alembic upgrade head
```

---

### Downgrade

Revierte cambios aplicados.

```bash
alembic downgrade -1
```

---

### Head

Última versión disponible del esquema.

```bash
alembic current
```

---

### Baseline Migration

Proceso utilizado cuando una base de datos ya existe antes de introducir Alembic.

Permite registrar el estado actual como punto de partida del historial.

---

## Instalación

Instalar Alembic:

```bash
pip install alembic
```

Verificar:

```bash
alembic --help
```

---

## Inicialización

Crear estructura de Alembic:

```bash
alembic init alembic
```

Resultado:

```text
alembic/
├── versions/
├── env.py
└── script.py.mako

alembic.ini
```

---

## Configuración

### alembic.ini

Configurar cadena de conexión:

```ini
sqlalchemy.url = postgresql+psycopg://postgres:postgres@192.168.56.2:5432/users
```

---

### env.py

Importar metadata de SQLAlchemy:

```python
from app.database import Base
from app.models import UserModel

target_metadata = Base.metadata
```

Importar los modelos es obligatorio para que SQLAlchemy los registre dentro de:

```python
Base.metadata
```

---

## Primera Migración

Generar migración automática:

```bash
alembic revision --autogenerate -m "initial schema"
```

Archivo generado:

```text
alembic/versions/
└── 42asca24sa_initial_schema.py
```

En este proyecto la migración resultó vacía:

```python
def upgrade():
    pass

def downgrade():
    pass
```

porque la estructura ya existía en PostgreSQL.

---

## Baseline

La base de datos fue creada previamente mediante:

```python
Base.metadata.create_all()
```

Por tanto Alembic no conocía el historial.

Se registró el estado actual mediante:

```bash
alembic stamp head
```

Este comando:

* No modifica tablas.
* No ejecuta migraciones.
* Crea la tabla `alembic_version`.
* Registra la versión actual del esquema.

---

## Tabla alembic_version

Alembic utiliza:

```text
alembic_version
```

para almacenar la versión actual aplicada a la base de datos.

Ejemplo:

| version_num |
| ----------- |
| 42asca24sa  |

---

## Primera Migración Real

Se agregó la columna:

```python
phone = Column(String, nullable=True)
```

al modelo:

```python
UserModel
```

Generación automática:

```bash
alembic revision --autogenerate -m "add phone to users"
```

Resultado:

```python
def upgrade():
    op.add_column(
        "users",
        sa.Column("phone", sa.String(), nullable=True)
    )
```

```python
def downgrade():
    op.drop_column(
        "users",
        "phone"
    )
```

---

## Aplicación de Migraciones

Aplicar última versión:

```bash
alembic upgrade head
```

Verificar versión actual:

```bash
alembic current
```

Mostrar historial:

```bash
alembic history
```

---

## Flujo de Trabajo

### Modificar modelo

```python
phone = Column(String)
```

### Generar migración

```bash
alembic revision --autogenerate -m "descripcion"
```

### Revisar migración

Inspeccionar manualmente:

```python
upgrade()
downgrade()
```

### Aplicar migración

```bash
alembic upgrade head
```

### Verificar PostgreSQL

```sql
\d users
```

---

## Buenas Prácticas

### Revisar siempre las migraciones

Nunca ejecutar:

```bash
alembic upgrade head
```

sin revisar previamente:

```python
upgrade()
downgrade()
```

---

### Mantener downgrade funcional

Toda migración debe poder revertirse.

---

### Una única fuente de verdad

Una vez adoptado Alembic, la gestión del esquema debe realizarse mediante migraciones.

Evitar depender de:

```python
Base.metadata.create_all()
```

como mecanismo principal de evolución del esquema.

---

## Comandos Más Utilizados

Generar migración:

```bash
alembic revision --autogenerate -m "mensaje"
```

Aplicar migraciones:

```bash
alembic upgrade head
```

Retroceder una versión:

```bash
alembic downgrade -1
```

Ver versión actual:

```bash
alembic current
```

Ver historial:

```bash
alembic history
```

Registrar baseline:

```bash
alembic stamp head
```

---

## Lecciones Aprendidas

* Alembic es el sistema oficial de migraciones para SQLAlchemy.
* `create_all()` no gestiona cambios sobre tablas existentes.
* Una migración debe revisarse antes de ejecutarse.
* `revision` genera migraciones; `upgrade` las ejecuta.
* `stamp` permite adoptar Alembic en una base de datos ya existente.
* Alembic mantiene el estado mediante la tabla `alembic_version`.
* Los cambios de esquema deben ser reversibles mediante `downgrade`.
