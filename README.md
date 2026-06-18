# QA Automation Lab

Proyecto práctico de entrenamiento en QA Automation utilizando Python, enfocado en pruebas de APIs, automatización backend y buenas prácticas utilizadas en entornos profesionales.

---

## Objetivos

* Aprender diseño de casos de prueba
* Practicar API Testing
* Automatizar pruebas con Pytest
* Aplicar buenas prácticas de QA
* Comprender contratos de APIs REST
* Aprender testing de persistencia y bases de datos
* Preparar una base sólida para posiciones de QA Automation Engineer

---

## Tecnologías

* Python
* FastAPI
* Pytest
* SQLAlchemy
* PostgreSQL
* Alembic
* pytest-cov
* pytest-html
* Passlib
* bcrypt
* Docker
* Docker Compose
* Git

---

## Estado actual

### Sprint 1 - Gestión de Usuarios

#### Backend Implementado

##### Endpoint raíz

```http
GET /
```

Respuesta:

```json
{
    "message": "QA Automation Lab API"
}
```

##### Crear Usuario

```http
POST /users
```

Validaciones implementadas:

* Nombre obligatorio
* Nombre entre 2 y 50 caracteres
* Email obligatorio
* Email con formato válido
* Edad obligatoria
* Edad entre 18 y 65 años
* No se permiten emails duplicados para usuarios activos

##### Consultar Usuario

```http
GET /users/{user_id}
```

Características:

* Devuelve usuarios activos
* Retorna 404 cuando el usuario no existe
* Retorna 404 cuando el usuario fue eliminado lógicamente

##### Eliminar Usuario

```http
DELETE /users/{user_id}
```

Características:

* Soft Delete
* No elimina físicamente el registro
* Cambia el campo `is_active` a `False`
* Retorna HTTP 204

##### Actualizar Usuario

```http
PUT /users/{user_id}
```

Características

* Actualiza nombre, email y edad
* Mantiene el mismo ID
* Retorna 404 cuando el usuario no existe o fue eliminado lógicamente
* Retorna 409 cuando el email ya está siendo utilizado por otro usuario activo
* No crea registros nuevos durante la actualización

##### Actualizar Usuario Parcialmente
```http
PATCH /users/{user_id}
```

Características:

* Permite actualizar uno o más campos del usuario
* Los campos son opcionales
* No permite payload vacío
* No permite valores null
* Mantiene el mismo ID
* Retorna 404 cuando el usuario no existe o fue eliminado lógicamente
* Retorna 409 cuando el email ya está siendo utilizado por otro usuario activo
* Permite reutilizar emails pertenecientes a usuarios eliminados lógicamente
* Actualiza únicamente los campos enviados

---

## Reglas de Negocio

### Usuarios

* El nombre debe contener entre 2 y 50 caracteres.
* El email debe tener formato válido.
* La edad debe estar entre 18 y 65 años.
* No pueden existir dos usuarios activos con el mismo email.
* Un usuario eliminado lógicamente puede reutilizar su email.
* Los usuarios inactivos no pueden ser consultados mediante la API.
* Los campos enviados mediante PATCH no pueden tener valor null.
* Un PATCH debe contener al menos un campo para actualizar.
* PATCH actualiza únicamente los campos enviados por el cliente.

---

## Persistencia

### Base de Datos

PostgreSQL

### Infraestructura

La base de datos se ejecuta dentro de un contenedor Docker alojado en una VM Ubuntu. La conectividad se realiza mediante una interfaz de red Host-Only para aislar el servicio del resto de la red.

Arquitectura:

```text
Windows
│
├── FastAPI
├── Pytest
└── PostgreSQL Client
     │
     ▼
Ubuntu VM
│
└── Docker
     │
     └── PostgreSQL
```

### Tabla Users

| Campo         | Tipo    |
| ------------- | ------- |
| id            | Integer |
| name          | String  |
| email         | String  |
| age           | Integer |
| is_active     | Boolean |
| password_hash | String  |

### Base de Datos de Testing

Las prueba automatizadas no utilizan la base de datos de desarrollo `users`.
Durante la ejecución de los test se utiliza una base de datos aislada:

```text
users_test
```

Mediante `Dependency Overrides` de FastAPI:

```python
app.dependency_overrides[get_db] = override_get_db
```

#### Beneficios
* Los test no modifican datos de desarrollo.
* Las pruebas son reproducibles.
* La persisetencia puede validarse sin afecar el entorno de trabajo.
* Se facilita la ekecución de pruebas automatizadas en CI/CD.

### Gestión de Esquema

El versionado de la base de datos se realiza mediante Alembic.

Comandos principales:

```bash
alembic current
alembic history
alembic revision --autogenerate -m "mensaje"
alembic upgrade head
alembic downgrade -1
```

Las migraciones se almacenan en:

```text
alembic/
└── versions/
```

---

## Testing

### Fixtures

* client
* db
* valid_user_payload
* valid_update_payload
* created_user
* user_payload
* patch_user
* setup_test_database

### Cobertura Actual

#### POST /users

* Registro exitoso
* Nombre demasiado corto
* Email inválido
* Edad vacío
* Payload vacío
* Contraseña sin minúscula
* Contraseña sin mayúscula
* Contraseña sin número
* Contraseña sin
* Contraseña longitud mínima

#### GET /users/{id}

* Usuario existente
* Usuario inexistente
* Parámetro inválido

#### DELETE /users/{id}

* Eliminación exitosa
* Usuario inexistente
* Eliminación doble

#### PUT /users/{id}

* Actualización exitosa
* Usuario inexistente
* Usuario eliminado
* Email duplicado

#### PATCH /users/{id}

* Actualizar únicamente name
* Actualizar únicamente email
* Actualizar únicamente age
* Actualizar name y email
* Actualizar name y age
* Actualizar email y age
* Actualizar todos los campos
* Usuario inexistente
* Usuario eliminado
* Email duplicado
* Reutilización de email tras Soft Delete
* Payload vacío
* Name inválido
* Email inválido
* Age inválido
* Name null
* Email null
* Age null

#### Persistencia PostgreSQL

* Usuario guardado correctamente en la base de datos
* Actualización reflejada correctamente en la base de datos
* Actualización parcial reflejada correctamente en la base de datos
* Soft Delete reflejado correctamente en la base de datos
* Verificación de que UPDATE no crea registros adicionales
* Verificación de que PATCH no crea registros adicionales
* La contraseña nunca se alamacena en texto plano
* bcrypt genere un hash válido
* `verify_password()` valide correctamente el hash almacenado

### Aislamiento de Pruebas

Los test utilizan transacciones SQL para garantizar aislamiento completo entre ejecuciones.

Cada prueba:

1. Abre una conexión a PostgreSQL.
2. Inicia una transacción.
3. Ejecuta la prueba.
4. Revierte todos los cambios mediante rollback.

Ejemplo simplificado:

```python
connection = test_engine.connect()

transaction = connection.begin()

db = TestingSessionLocal(bind=connection)

yield db

transaction.rollback()
```

#### Beneficios

* No es necesario eliminar registros manuales.
* Las pruebas son independientes entre sí.
* La base de datos permanece limpia después de cada test.
* Reduce el tiempo de ejecución de la suite.

### Cobertura de Código

La cobertura se mide utilizando `pytest-cov`

Ejecutar:

```python
pytest --cov=app
```

Mostrar líneas no cubiertas

```python
pytest --cov=app --cov-report=term-missing
```

Generar reporte HTML

```python
pytest --cov=app --cov-report=html
```

El reporte se genera en:

```text
htmlcov/index.html
```

Objetivos:

* Detectar ramas de código no ejecutadas.
* Identificar validaciones sin pruebas.
* Detectar código muerto.
* Medir cobertura de lógica de negocio.

### Reportes HTML

Los resultados de ejecución pueden exportarse a HTML utilizando `pytest-html`

Generar reporte:

```python
pytest --html=report.html --self-contained-html
```

Archivo generado:

```text
report.html
```

Beneficios:

* Evidencia de ejecución.
* Historial de resultados.
* Compartir resultados con desarrolladores o líderes técnicos.
* Integración futura con CI/CD

---

## Conceptos QA Aprendidos

### Diseño de Pruebas

* Casos positivos
* Casos negativos
* Partición de equivalencia
* Boundary Value Analysis (BVA)

### API Testing

* Status Codes
* Contratos de respuesta
* Validación de estructura JSON
* Validación de tipos de datos
* Validación de persistencia
* Pruebas CRUD
* Pruebas de integración de endpoints
* Pruebas de actualización parcial (PATCH)
* Validación de reglas de negocio
* Dependency Injection
* Verificación de cobertura
* Validación de reglas de negocio mediante cobertura

### Pytest

* Fixtures
* Reutilización de setup
* Datos dinámicos
* Parametrización
* Helpers reutilizables
* Dependency Overrides
* Fixture autouse
* Aislamiento de pruebas
* Cobertura de código
* Reportes HTML

### Bases de Datos

* Persistencia
* Integridad de datos
* Soft Delete
* PostgreSQL
* SQLAlchemy ORM
* Dependency Overrides
* Base de datos aislada para testing
* Rollback transaccional
* Validación directa de persistencia
* Validación de UPDATE sin inserción de registros
* Validación de Soft Delete desde la BD
* Verificación de UPDATE vs INSERT
* Verificación de PATCH vs INSERT

### Gestión de Esquema

* Alembic
* Baseline Migration
* Revision
* Upgrade
* Downgrade
* Autogenerate
* alembic_version
* Versionado de esquema
* Migraciones reversibles

---

## Test Doubles

### Test Double

Término general para cualquier objeto que reemplaza una dependencia real durante una prueba.

### Stub

Devuelve respuestas predefinidas.

### Mock

Simula dependencias y permite verificar interacciones.

Ejemplo:

```python
mock_send_email.assert_called_once()
```

### Fake

Implementación simplificada de un componente real.

Ejemplo:

* Base de datos en memoria
* Repositorio temporal en memoria

### Dummy

Objeto utilizado únicamente para satisfacer dependencias.

### Spy

Permite observar cómo fue utilizado un objeto durante una prueba.

---

## Estructura del Proyecto

```text
qa-automation-lab/
│
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── ...
│
├── app/
│   ├── main.py
│   ├── schemas.py
│   ├── models.py
│   ├── database.py
│   ├── dependencies.py
│   └── routes/
│       └── users.py
│
├── app/
│   └── security.py
│
├── tests/
│   ├── conftest.py
│   ├── helpers.py
│   ├── test_create_user.py
│   ├── test_database.py
│   ├── test_delete_user.py
│   ├── test_get_user.py
│   ├── test_patch_user.py
│   └── test_update_user.py
│
├── README.md
├── alembic.ini
└── requirements.txt
```

---

## Roadmap

### Sprint 1 - Gestión de Usuarios

* [x] API básica
* [x] Persistencia SQLite
* [x] POST User
* [x] GET User
* [x] PUT User
* [x] DELETE User (Soft Delete)
* [x] Reutilización de email tras Soft Delete
* [x] Validaciones de entrada
* [x] Fixtures reutilizables
* [x] Validación de persistencia desde tests
* [x] PATCH User

### Sprint 2 - Calidad de Automatización

* [x] Parametrización de pruebas
* [x] Base de datos de pruebas aisladas
* [x] Refactorización de fixtures
* [x] Helpers de validación de respuestas
* [x] Cobertura de código
* [x] Reportes HTML
* [x] Optimización de tiempos de ejecución

#### Sprint 2.1 - Infraestructura de Testing

* [x] Crear VM Ubuntu dedicada para servicios
* [x] Instalar Docker Engine en Ubuntu
* [x] Instalar Docker Compose en Ubuntu
* [x] Desplegar PostgreSQL mediante Docker Compose
* [x] PostgreSQL expuesto unicamente en Host-Only
* [x] Crear base de datos de desarrollo (`users`)
* [x] Crear base de datos de pruebas (`users_test`)
* [x] Migrar SQLAlchemy de SQLite a PostgreSQL
* [x] Adaptar fixtures de testing para PostgreSQL
* [x] Implementar limpieza mediante rollback transaccional
* [x] Aislamiento completo entre desarrollo y testing
* [x] Actualizar documentación de infraestructura

#### Sprint 2.2 - Gestión de Esquema

* [x] Introducción a Alembic
* [x] Inicialización de Alembic
* [x] Integración Alembic + SQLAlchemy
* [x] Creación de Baseline Migration
* [x] Primera migración de esquema
* [x] Versionado de cambios de base de datos
* [x] Uso de upgrade y downgrade
* [x] Uso de alembic_version

#### Sprint 2.3 - Alembic para Tests

* [x] Migrar users_test a Alembic
* [x] Eliminar create_all() de tests
* [x] Eliminar create_all() de main.py
* [x] Alembic como única fuente de verdad para la DB

### Sprint 3 - Autenticación

#### Sprint 3.1

* [x] Reemplazar phone por password_hash (nullable=True)
* [x] Generar migración con Alembic
* [x] Aplicar migración en users
* [x] Aplicar migración en users_test
* [x] Verificar esquema
* [x] Hashing con bcrypt
* [x] Testing de validación de contraseñas
* [x] Testing de persistencia de hashes
* [ ] Login
* [ ] JWT Access Token
* [ ] Endpoint protegido
* [ ] Testing de autenticación

#### Sprint 3.2

* [ ] Expiración de tokens
* [ ] Dependencia get_current_user
* [ ] Roles
* [ ] Reglas de autenticación
* [ ] Testing avanzado

#### Sprint 3.3

* [ ] Bloqueo de cuenta
* [ ] Recuperación de contraseña
* [ ] Tokens de recuperación
* [ ] Testing de autenticación

### Sprint 4 - Automatización Avanzada

* [ ] Mocking
* [ ] Test Doubles
* [ ] Spy y Stub
* [ ] Monkeypatch
* [ ] Testing de servicios externos
* [ ] Pruebas de integración avanzadas
* [ ] Reportes HTML avanzados
* [ ] Métricas de cobertura
* [ ] Inicialización automática mediante migraciones
* [ ] Sincronización users / users_test

### Sprint 5 - Integración Continua

* [ ] GitHub Actions
* [ ] Ejecución automática de tests
* [ ] Reportes HTML
* [ ] Ejecución de cobertura automática
* [ ] Pipeline con PostgreSQL
* [ ] Validación automática de Pull Requests
* [ ] Badge de cobertura
* [ ] Workflow de calidad

---

## Lecciones Aprendidas

* FastAPI devuelve HTTP 422 para errores de validación de Pydantic.
* TestClient permite probar APIs sin levantar Uvicorn.
* Las fixtures de Pytest ayudan a reutilizar recursos entre pruebas.
* `python -m pytest` puede evitar problemas de resolución de entornos en Windows.
* Los tests deben validar contratos de API, no solamente status codes.
* Un Soft Delete requiere validaciones distintas a un Hard Delete.
* Los datos de prueba deben ser únicos y reproducibles.
* Los fixtures pueden contener validaciones y lógica de preparación de datos.
* Los IDs inválidos deberían validarse explícitamente mediante restricciones de entrada.
* La calidad también se construye refinando requisitos, no solo encontrando bugs.
* Los tests de integración validan el flujo completo entre endpoints.
* Los tests de persistencia validan directamente el estado de la base de datos.
* Consultar la API y consultar la base de datos son estrategias complementarias de validación.
* PATCH y PUT resuelven problemas distintos.
* PATCH debe actualizar únicamente los campos enviados.
* Las reglas de validación pertenecen preferentemente a los schemas de Pydantic.
* `model_dump(exclude_unset=True)` permite identificar únicamente los campos enviados por el cliente.
* `setattr()` permite implementar actualizaciones dinámicas de modelos.
* La reutilización de emails después de un Soft Delete debe ser considerada explícitamente en las reglas de negocio.
* Los tests deben validar que una actualización modifica registros existentes y no genera registros nuevos.
* FastAPI permite reemplazar dependencias mediante `app.dependency_overrides`.
* Los tests deben ejecutarse sobre una base de datos independiente de producción.
* SQLAlchemy utiliza Session como unidad de trabajo para interactuar con la base de datos.
* `add()` registra cambios en la Session pero no los persiste.
* `commit()` confirma definitivamente los cambios en la base de datos.
* `refresh()` sincroniza el objeto Python con el estado persistido.
* Los tests no deben depender de valores específicos de IDs autoincrementales.
* La parametrización reduce duplicación y facilita la ampliación de escenarios de prueba.
* Los helpers permiten centralizar validaciones repetitivas y mejorar la mantenibilidad de la suite.
* La cobertura ayuda a identificar reglas de negocio que no están siendo ejecutadas por los tests.
* Una cobertura alta no garantiza ausencia de errores, pero reduce puntos ciegos.
* Los reportes HTML facilitan compartir resultados de ejecución.
* La cobertura puede revelar tests faltantes incluso cuando la suite parece completa.
* `pytest-cov` y `pytest-html` son herramientas complementarias para medir calidad y generar evidencia.
* SQLAlchemy permite migrar entre motores de bases de datos con cambios mínimos en la aplicación.
* Dependency Overrides permiten redirigir dependencias de FastAPI durante los tests.
* PostgreSQL es más adecuado que SQLite para simular entornos reales de producción.
* Los rollbacks transaccionales permiten mantener aislamiento completo entre pruebas.
* Una sesión SQLAlchemy puede asociarse a una conexión existente mediante bind=connection.
* El rollback debe ejecutarse sobre la misma transacción utilizada por los endpoints.
* Los tests de integración pueden compartir una sesión mediante Dependency Overrides sin perder aislamiento.