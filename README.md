# QA Automation Lab

Backend desarrollado con FastAPI diseñado como un laboratorio práctico para aprender QA Automation, pruebas automatizadas y buenas prácticas de desarrollo backend.

El proyecto evoluciona de forma incremental mediante sprints, incorporando progresivamente nuevas funcionalidades, mecanismos de seguridad, infraestructura de testing y mejoras de arquitectura, simulando la evolución de una aplicación real.

Su objetivo no es únicamente construir una API REST, sino servir como un entorno donde experimentar con técnicas de testing profesional, automatización y diseño de software mantenible.

---

## Objetivos del Proyecto

Este laboratorio fue creado con los siguientes objetivos:

* Desarrollar una API REST siguiendo buenas prácticas de arquitectura.
* Aprender y aplicar técnicas de QA Automation utilizando Pytest.
* Diseñar una infraestructura de testing aislada y reproducible.
* Implementar mecanismos reales de autenticación y autorización.
* Gestionar la evolución del esquema de la base de datos mediante Alembic.
* Automatizar el ciclo de pruebas e integración.
* Documentar las decisiones técnicas tomadas durante el desarrollo.
* Simular el ciclo de vida de un proyecto backend profesional.

Cada sprint incorpora nuevos conceptos tanto de desarrollo backend como de testing, permitiendo que el proyecto evolucione de forma similar a una aplicación utilizada en un entorno real.

---

## Características

### API REST

* CRUD completo de usuarios
* Validaciones mediante Pydantic
* Soft Delete
* Manejo consistente de códigos HTTP
* Documentación automática mediante Swagger/OpenAPI

### Persistencia

* PostgreSQL
* SQLAlchemy ORM
* Alembic para versionado del esquema
* Migraciones automáticas

### Seguridad

* Autenticación mediante JWT
* Hashing de contraseñas
* Control de acceso basado en roles (RBAC)
* Bloqueo temporal de cuentas
* Recuperación segura de contraseñas
* Tokens de recuperación de un solo uso

### Testing

* Pytest
* Fixtures reutilizables
* Dependency Overrides
* Base de datos independiente para testing
* Rollback automático por transacción
* Mocking
* Spy
* Stub
* Monkeypatch
* Pruebas unitarias
* Pruebas de integración
* Reportes HTML
* Cobertura de código

### Arquitectura

* Configuración centralizada mediante `Settings`
* Separación por capas
* Servicios desacoplados
* Gestión independiente de entornos de desarrollo y testing
* Migraciones sincronizadas entre bases de datos

---

## Tecnologías

### Backend

* Python
* FastAPI
* SQLAlchemy
* Pydantic

### Base de Datos

* PostgreSQL
* Alembic

### Testing

* Pytest
* unittest.mock
* pytest-mock
* pytest-html
* coverage

### Infraestructura

* Docker
* Docker Compose
* GitHub Actions

---

## Arquitectura

El proyecto sigue una arquitectura por capas con separación clara de responsabilidades.

```text
Cliente 
   │ 
   ▼ 
FastAPI 
   │ 
   ▼ 
Routes 
   │ 
   ▼ 
Services 
   │ 
   ▼ 
SQLAlchemy 
   │ 
   ▼ 
PostgreSQL
```

La configuración del proyecto se encuentra centralizada mediante la clase `Settings`, utilizada por la aplicación, Alembic y la infraestructura de testing.

Durante el Sprint 5 la configuración fue externalizada mediante variables de entorno (`.env`), permitiendo ejecutar el mismo código en distintos entornos (desarrollo, testing e integración continua) modificando únicamente la configuración.

La arquitectura completa, las decisiones de diseño y los principales flujos de la aplicación se documentan en: [Arquitectura](/docs/architecture.md)

---

## Calidad del Código

Este proyecto utiliza un pipeline de calidad compuesto por:

- ✅ Ruff
- ✅ Black
- ✅ isort
- ✅ MyPy
- ✅ Pytest

Todos los cambios deben superar satisfactoriamente estas herramientas antes de integrarse en el proyecto.

---

## Integración Continua

El proyecto incorpora un pipeline de Integración Continua mediante GitHub Actions.

En cada Push y Pull Request se ejecutan automáticamente las siguientes etapas:

```text
Ruff
   │ 
   ▼ 
Black
   │ 
   ▼ 
isort
   │ 
   ▼ 
MyPy
   │ 
   ▼ 
PostgreSQL
   │ 
   ▼ 
Alembic
   │ 
   ▼ 
Pytest
```

El objetivo es garantizar que el proyecto pueda construirse desde un entorno completamente limpio antes de integrar cualquier cambio.

---

## Estructura del Proyecto

```text
qa-automation-lab/ 
│ 
├── alembic/            # Migraciones 
├── app/                # Código de la aplicación 
├── docs/               # Documentación técnica 
├── tests/              # Suite de pruebas automatizadas 
│ 
├── README.md 
├── alembic.ini 
└── requirements.txt
```

---

## Primeros Pasos

### 1. Clonar el repositorio

```bash
git clone https://github.com/AlexanderFloresBarturen/qa-automation-lab.git

cd qa-automation-lab
```

### 2. Crear un entorno virtual

#### Windows

```powershell
python -m venv .venv

.venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

### 3. Configurar las variables de entorno

Crear un archivo `.env` a partir de `.env.example` y completar los valores correspondientes al entorno local.

```bash
cp .env.example .env
```

En Windows:

```powershell
copy .env.example .env
```

### 4. Instalar dependencias

```bash
pip install -r requirements
```

### 5. Levantar PostgreSQL

Consultar: [Docker](/docs/docker.md)

### 6. Inicializar la base de datos de desarrollo

Aplicar las migraciones sobre la base de datos de desarrollo:

```bash
alembic upgrade head
```

**Nota:** La base de datos de testing (`users_test`) se migra automáticamente al ejecutar la suite de pruebas mediante Pytest. No es necesario aplicar las migraciones manualmente para el entorno de testing.

### 7. Iniciar la aplicación

```bash
uvicorn app.main:app --reload
```

La documentación interactiva estará disponible en: `http://localhost:8000/docs`

### 8. Ejecutar la suite de pruebas

```bash
python -m pytest -v
```

---

## Documentación

La documentación técnica del proyecto se encuentra organizada por áreas con el objetivo de mantener el README como una visión general del laboratorio y delegar los detalles de implementación en documentos especializados.

| Documento | Descripción |
|-----------|-------------|
| [Arquitectura](/docs/architecture.md) | Arquitectura del sistema, organización por capas, decisiones de diseño y flujos principales.|
| [API](/docs/api.md) | Recursos expuestos, endpoints, reglas de negocio, control de acceso (RBAC) y comportamiento funcional de la API.|
| [Modelo de Datos](/docs/database.md) | Modelo relacional, entidades, relaciones, restricciones y estructura de la base de datos.|
| [Testing](/docs/testing.md) | Infraestructura de testing, fixtures, rollback, mocking, integración, cobertura y automatización. |
| [Alembic](/docs/alembic.md) | Gestión de migraciones, versionado del esquema y sincronización entre desarrollo y testing. |
| [Docker](/docs/docker.md) | Configuración del entorno mediante Docker y Docker Compose. |
| [Roadmap](/docs/roadmap.md) | Evolución del proyecto por sprints, funcionalidades implementadas y planificación de futuras etapas.|

---

## Roadmap

El proyecto evoluciona mediante sprints incrementales. Cada uno incorpora nuevos conceptos tanto de desarrollo backend como de QA Automation.

| Sprint  | Estado | Contenido principal |
|---------|--------|---------------------|
| Sprint 0 | ✅ | API base, PostgreSQL, SQLAlchemy, Alembic y Docker |
| Sprint 1 | ✅ | Pytest, fixtures, base de datos de testing y automatización básica |
| Sprint 2 | ✅ | CRUD completo y consolidación de la API |
| Sprint 3 | ✅ | Seguridad, JWT, RBAC, recuperación de contraseña y control de acceso |
| Sprint 4 | ✅ | Mocking, Monkeypatch, pruebas de integración, cobertura, reportes HTML y automatización de migraciones |
| Sprint 5 | ✅  | GitHub Actions, análisis estático, integración continua, migraciones automáticas y pipeline de calidad |

---

## Estado Actual

| Característica | Estado |
|----------------|--------|
| Desarrollo activo | ✅ |
| API REST | ✅ |
| PostgreSQL | ✅ |
| JWT Authentication | ✅ |
| RBAC | ✅ |
| Recuperación de contraseña | ✅ |
| Testing automatizado | ✅ |
| Pruebas de integración | ✅ |
| Mocking / Spy / Stub | ✅ |
| Monkeypatch | ✅ |
| Reportes HTML | ✅ |
| Cobertura de código | 98 % |
| Migraciones automáticas | ✅ |
| Configuración centralizada | ✅ |
| GitHub Actions | ✅ |
| Integración Continua | ✅ |
| Ruff | ✅ |
| Black | ✅ |
| isort | ✅ |
| MyPy | ✅ |

---

## Próximos Objetivos

Las siguientes etapas del laboratorio estarán orientadas a incorporar herramientas utilizadas habitualmente en proyectos profesionales de QA Automation y DevOps.

Entre los objetivos se encuentran:

* Hooks de Pre-commit.
* Publicación de reportes de cobertura.
* Badges de GitHub Actions y cobertura.
* Análisis de seguridad del código.
* Matriz de pruebas con múltiples versiones de Python.

---

## Licencia

Este proyecto se distribuye con fines educativos y de aprendizaje.