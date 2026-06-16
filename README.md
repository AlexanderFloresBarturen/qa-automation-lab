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
* SQLite
* pytest-cov
* pytest-html
* Docker
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

SQLite

### Tabla Users

| Campo     | Tipo    |
| --------- | ------- |
| id        | Integer |
| name      | String  |
| email     | String  |
| age       | Integer |
| is_active | Boolean |

### Base de Datos de Testing

Las prueba automatizadas no utilizan la base de datos de desarrollo `(users.db)`.
Durante la ejecución de los test se utiliza una base de datos aislada:

```text
test.db
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
* clean_database
* override_get_db

### Cobertura Actual

#### POST /users

* Registro exitoso
* Nombre demasiado corto
* Email inválido
* Edad menor a 18
* Payload vacío
* Campos obligatorios ausentes
* Email duplicado

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

#### Persistencia SQLite

* Usuario guardado correctamente en la base de datos
* Actualización reflejada correctamente en la base de datos
* Actualización parcial reflejada correctamente en la base de datos
* Soft Delete reflejado correctamente en la base de datos
* Verificación de que UPDATE no crea registros adicionales
* Verificación de que PATCH no crea registros adicionales

### Aislamiento de Pruebas

Cada prueba se ejecuta sobre una base de datos limpia mediante fixtures automáticas.

Objetivos:

* Evitar dependencias entre tests.
* Garantizar resultados reproducibles.
* Evitar contaminación de datos entre ejecuciones.
* Permitir ejecutar cualquier test de forma individual.

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
* Validación directa de persistencia
* Validación de UPDATE sin inserción de registros
* Validación de Soft Delete desde la BD
* Verificación de UPDATE vs INSERT
* Verificación de PATCH vs INSERT
* Base de datos aislada para testing
* Separación entre entorno de desarrollo y pruebas
* Limpieza automática de datos
* Ciclo de vida de Session, Engine y Dependency Injection

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
├── app/
│   ├── main.py
│   ├── schemas.py
│   ├── models.py
│   ├── database.py
│   ├── dependencies.py
│   └── routes/
│       └── users.py
│
├── tests/
│   ├── conftest.py
│   ├── test_create_user.py
│   ├── test_database.py
│   ├── test_delete_user.py
│   ├── test_get_user.py
│   ├── test_patch_user.py
│   └── test_update_user.py
│
├── requirements.txt
└── README.md
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

### Sprint 2.5 - Infraestructura de Testing

* [ ] Crear VM Ubuntu dedicada para servicios
* [ ] Instalar Docker Engine en Ubuntu
* [ ] Instalar Docker Compose en Ubuntu
* [ ] Desplegar PostgreSQL mediante Docker Compose
* [ ] Crear base de datos de producción (`users`)
* [ ] Crear base de datos de pruebas (`users_test`)
* [ ] Migrar SQLAlchemy de SQLite a PostgreSQL
* [ ] Adaptar fixtures de testing para PostgreSQL
* [ ] Implementar limpieza mediante rollback transaccional
* [ ] Actualizar documentación de infraestructura

### Sprint 2.6 - Gestión de Esquema

* [ ] Introducción a Alembic
* [ ] Primera migración de esquema
* [ ] Versionado de cambios de base de datos
* [ ] Integración Alembic + SQLAlchemy

### Sprint 3 - Autenticación

* [ ] Login
* [ ] Hashing de contraseñas
* [ ] JWT Access Token
* [ ] Endpoint protegido
* [ ] Bloqueo de cuenta
* [ ] Recuperación de contraseña
* [ ] Reglas de autenticación
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