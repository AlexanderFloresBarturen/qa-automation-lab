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
* python-jose
* JWT
* python-multipart
* Docker
* Docker Compose
* Git

---

## Estado actual

### Gestión de Usuarios

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

* Requeire autenticación
* Un usuario solo puede consultar su propio perfil
* Retorna 403 cuando intenta acceder al perfil de otro usuario
* Los usuarios inactivos no pueden autenticarse

##### Eliminar Usuario

```http
DELETE /users/{user_id}
```

Características:

* Requeire autenticación
* Soft Delete
* No elimina físicamente el registro
* Cambia el campo `is_active` a `False`
* Retorna HTTP 204

##### Actualizar Usuario

```http
PUT /users/{user_id}
```

Características

* Requeire autenticación
* Actualiza nombre, email y edad
* Mantiene el mismo ID
* Retorna 409 cuando el email ya está siendo utilizado por otro usuario activo
* No crea registros nuevos durante la actualización

##### Actualizar Usuario Parcialmente
```http
PATCH /users/{user_id}
```

Características:

* Requeire autenticación
* Permite actualizar uno o más campos del usuario
* Los campos son opcionales
* No permite payload vacío
* No permite valores null
* Mantiene el mismo ID
* Retorna 409 cuando el email ya está siendo utilizado por otro usuario activo
* Permite reutilizar emails pertenecientes a usuarios eliminados lógicamente
* Actualiza únicamente los campos enviados

##### Login

```http
POST /users/login
```

Características:

* Autenticación mediante JWT
* Utiliza OAuth2 Password Flow
* Verifica contraseñas mediante bcrypt
* Retorna Access Token
* Retorna 401 para credenciales inválidas
* Retorna 423 para cuentas bloqueadas

##### Solicitar Recuperación de Contraseña

```http
POST /users/forgot-password
```

Características:

* Genera token de recuperación
* Invalida tokens anteriores del usuario
* Los tokens expiran en 15 minutos
* Retorna HTTP 200 incluso si el email no existe
* Evita email enumeration

##### Restableces Contraseña

```http
POST /users/reset-password
```

Características:

* Requiere token válido
* Verifica expiración del token
* Verifica que el token no haya sido utilizado
* Actualiza el password_hash
* Invalida el token utilizado
* Reinicia el contador de intentos fallidos
* Desbloquea la cuenta

##### Listar usuarios

```http
POST /users/reset-password
```

Características:

* Requiere rol admin
* Retorna únicamente usuario activos
* Utiliza autorización basada en RBAC
* Retorna 403 para usuarios sin privilegios administrativos
* Retorna 401 para usuarios no autenticados

##### Perfil Actual

```http
GET /users/test/me
```

Características:

* Requiere autenticación
* Obtiene el usuario asociado al JWT
* No requiere conocer el ID del usuario

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

### Contraseñas

* Mínimo 8 caracteres.
* Al menos una mayúscula.
* Al menos una minúscula.
* Al menos un número.
* Al menos un carácter especial.

### Autenticación

* Las contraseñas nunca se almacenan en texto plano.
* Las contraseñas se almacenan utilizando bcrypt.
* Los usuarios deben autenticarse mediente JWT.
* Los JWT incluyen fecha de expiración.
* Los endpoints protegidos requieren Bearer Token.
* Los usuarios inactivos no pueden autenticarse.

### Roles

* Todo usuario registrado recibe automáticamente el rol user.
* Los administradores se asignan manualmente.
* Los recursos administrativos requieren permisos de administrador.
* La autorización se implementa mediante la dependencia `require_admin()`

### Autorización

La aplicación implementa dos niveles de control de acceso.

#### Basado en Propietario (Ownership)

Un usuario únicamente puede:

* Consultar su propio perfil
* Actualizar su propio perfil
* Eliminar su propia cuenta

Intentar acceder a recursos de otros usuarios retorna:

```text
403 Forbidden
```

#### Basado en Roles (RBAC)

Algunos recursos requieren privilegios administrativos. Ejemplo:

```http
GET /users
```

Solo usuarios con rol `admin` pueden acceder a ellos.

### Bloqueo de Cuenta

* Después de 5 intentos fallidos consecutivos la cuenta se bloquea
* El bloqueo dura 15 minutos.
* Durante el bloqueo el login retorna HTTP 423.
* Cuando el bloqueo expira el contador de intentos fallidos se reinicia automáticamente.
* Un login exitoso reinicia el contador de intentos fallidos.

### Recuperación de Contraseñas

* Los tokens de recuperación son de un solo uso.
* Los tokens expiran después de 15 minutos.
* Un usuario solo puede tener un token activo.
* Solicitar un nuevo token invalida los anteriores.
* El cambio de contraseña invalida el token utilizado.
* El cambio de contraseña desbloquea la cuenta.

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

| Campo                  | Tipo         |
| ---------------------- | ------------ |
| id                     | Integer      |
| role_id                | Integer (FK) |
| name                   | String       |
| email                  | String       |
| age                    | Integer      |
| is_active              | Boolean      |
| password_hash          | String       |
| failed_login_attempts  | Integer      |
| locked_until           | DateTime     |

### Tablas Roles

| Campo         | Tipo        |
| ------------- | ----------- |
| id            | Integer     |
| name          | String      |

Roles inciales:

1. admin
2. user

### Tabla PasswordResetTokens

| Campo         | Tipo         |
| ------------- | ------------ |
| id            | Integer      |
| user_id       | Integer (FK) |
| token         | String       |
| used          | Boolean      |
| created_at    | DateTime     |
| expires_at    | DateTime     |

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

## Configuración Centralizada

### Objetivo

La aplicación utiliza una configuración centralizada para evitar la duplicación de parámetros entre:

* FastAPI
* Alembic
* Pytest

Toda la configuración del proyecto se encuentra en:

```text
app/core/settings.py
```

Esto permite mantener una única fuente de verdad para la configuración del sistema.

### Configuración Gestionada

Actualmente `Settings` centraliza:

#### Base de datos

* Development Database
* Test Database
* Current Database

#### JWT

* Secret Key
* Algorithm
* Token Expiration

#### Seguridad

* Maximum Login Attempts
* Account Lock Duration
* Password Reset Token Expiration

### Cambio de Entorno

La clase `Settings` encapsula el cambio entre la base de desarrollo y la de pruebas.

```python
settings.use_development_database()

settings.use_test_database()
```

El resto de la aplicación nunca necesita conocecer cuál es la base activa. Siempre utiliza:

```python
settings.DATABASE_URL
```

### Estado Actual

Además de la URL activa, `Settings` mantiene el entorno actualmente seleccionado.

```python
settings.CURRENT_DATABASE
```

Valores disponibles:

1. development
2. test

Esto permite conocer en cualquier momento qué base está utilizando la aplicación.

También dispone de propiedades auxiliares:

```python
settings.is_development_database

settings.is_test_database
```

que facilitan realizar comprobaciones sin comparar cadenas de texto.

### Integración con Alembic

Alembic ya no obtiene la URL desde `alembic.ini`.

Durante la inicialización ejecuta:

```python
config.set_main_option(
     "sqlalchemy.url",
     settings.DATABASE_URL
)
```

Estos hace que las migraciones utilicen siempre la base de datos actualmente activa.

### Automatización de Testing

Antes de ejecutar la suite de pruebas, Pytest cambia automáticamente el entorno a testing.

Flujo:

```text
Inicio Pytest
        │
        ▼
settings.use_test_database()
        │
        ▼
DATABASE_URL → users_test
        │
        ▼
Alembic upgrade head
        │
        ▼
Inicio de pruebas
```

Al finalizar la ejecucion:

```text
Fin de pruebas
        │
        ▼
settings.use_development_database()
```

De esta forma:

* Las migraciones siempre se ejecutan sobre users_test.
* La base de datos de desarrollo nunca se modifica durante las pruebas.
* El desarrollador no necesita ejecutar manualmente `alembic ugrade head` antes de lanzar la suite.

### ¿Por qué sigue existiendo `test_engine`?

Aunque la aplicación utiliza una configuración centralizada, durante las pruebas FastAPI reemplaza la dependencia `get_db()` mediante `dependency_overrides`.

La infraestructura queda así:

```text
                    Settings
                       │
          ┌────────────┴────────────┐
          │                         │
          ▼                         ▼
   connection.py              alembic/env.py
          │                         │
          ▼                         ▼
   users (desarrollo)      users / users_test
                                   │
                                   ▼
                           pytest_sessionstart()
                                   │
                                   ▼
                        settings.use_test_database()
                                   │
                                   ▼
                           alembic upgrade head
                                   │
                                   ▼
                             test_engine
                                   │
                                   ▼
                      dependency_overrides(get_db)
                                   │
                                   ▼
                              users_test
```

`test_engine` continúa existinedo porque el `engine` de la aplicación se crea durante la importación del módulo (`connection.py`). En ese momento todavía no se ha ejecutado `pytest_sessionstart()`. En lugar de recrear el `engine` principal, las pruebas utilizan un `test_engine` independiente y redirigen todas las dependencias de base de datos hacia el mediente `dependency_overrides`.

Este enfoque mantiene completamente aisladas als bases de desarrollo y de pruebas, evita efectos secundario sobre el `engine` principal y simplifica la infraestructura de testing.

### Beneficios

* Una única fuente de configuración (`Settings`).
* Eliminación de URLs duplicadas en distintos módulos.
* FastAPI, Alembic y Pytest comparten la misma configuración.
* Las migraciones de testing de ejecutan automáticamente.
* El entorno de desarrollo permanece aislado del entorno de pruebas.
* La arquitectura queda preparada para migrar fácilmente a variables de entorno (`.env`) mediante `pydantic-settings` en el futuro.

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
* loged_user
* get_token
* user_reset_password_payload
* admin_user

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

#### POST /users/login

* Login exitoso
* Usuario inexistente
* Contraseña incorrecta
* Incremento de intentos fallidos
* Bloqueo tras 5 intentos fallidos
* Usuario bloqueado
* Reinicio de contador tras login exitoso
* Reinicio automático tras expiración del bloqueo

#### POST /users/forgot-password

* Usuario existente
* Usuario inexistente
* Invalidación de tokens anteriores

#### POST /users/reset-password

* Token válido
* Token inválido
* Token usado
* Token expirado
* Contraseña inválida
* Actualización de hash
* Desbloqueo de cuenta
* Flujo completo de recuperación de contraseña

#### GET /users

* Acceso exitoso para administrador
* Acceso denegado para usuario normal
* Acceso sin token
* Acceso con token inválido

#### POST /users/test/me

* Token válido
* Token inválido
* Sin token

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

### Autorización

#### Endpoints Protegidos

* Usuario consulta su propio perfil
* Usuario intenta consultar otro perfil
* Usuario elimina su propio perfil
* Usuario intenta eliminar otro perfil
* Usuario modifica su propio perfil
* Usuario intenta modificar otro perfil
* Token inválido
* Sin token

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
pytest --html=reports/report.html --self-contained-html
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

### SQLAlchemy

* Relationships
* Foreign Keys
* Identity map
* Session Refresh
* Session Expunge

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

### Seguridad

* Hashing de contraseñas
* bcrypt
* JWT
* OAuth2
* Access Tokens
* Bearer Authentication
* Expiración de Tokens
* Autenticación
* Autorización
* RBAC (Role Based Access Control)
* Bloqueo de cuentas

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
│   ├── core/
│   │   └── settings.py
│   ├── database/
│   │   ├── connection.py
│   │   └── dependencies.py
│   ├── models/
│   │   ├── role_model.py
│   │   ├── token_model.py
│   │   └── user_model.py
│   ├── routes/
│   │   └── users.py
│   ├── schemas/
│   │   └── user.py
│   ├── security/
│   │   ├── dependencies.py
│   │   ├── jwt.py
│   │   └── password.py
│   ├── services/
│   │   └── email_service.py
│   ├── utils/
│   │   └── password_validator.py
│   └── main.py
│
├── docs/
│   ├── alembic.md
│   ├── docker.md
│   └── testing.md
│
├── tests/
│   ├── integration/
│   │   └── test_password_recovery_flow.py
│   ├── conftest.py
│   ├── helpers.py
│   ├── test_create_user.py
│   ├── test_database.py
│   ├── test_delete_user.py
│   ├── test_get_user.py
│   ├── test_get_users.py
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
* [x] Reglas de contraseñas
* [x] Testing de validación de contraseñas
* [x] Testing de persistencia de hashes
* [x] Login
* [x] Testing de login
* [x] JWT Access Token
* [x] Endpoint protegido
* [x] Testing de autenticación

#### Sprint 3.2

* [x] Expiración de tokens
* [x] Dependencia get_current_user
* [x] Protección de endpoints
* [x] Reglas de autenticación
* [x] Testing avanzado
* [x] Sistema de roles
* [x] Tabla de roles
* [x] Foreign Keys
* [x] Relaciones SQLAlchemy
* [x] Dependencia require_admin
* [x] RBAC aplicado a endpoints reales
* [x] Endpoint administrativo
* [x] Testing de roles

#### Sprint 3.3

* [x] Bloqueo de cuenta
* [x] Tokens de recuperación
* [x] Recuperación de contraseña
* [x] Testing de autenticación

### Sprint 4 - Automatización Avanzada

#### 4.1

* [x] Mocking
* [x] Test Doubles
* [x] Spy y Stub

#### 4.2

* [x] Monkeypatch
* [x] Testing de servicios externos

#### 4.3

* [x] Pruebas de integración avanzadas

#### 4.4

* [x] Reportes HTML avanzados
* [x] Métricas de cobertura

#### 4.5

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
* Los tokens de recuperación deben ser de un solo uso.
* Los tests pueden manipular fechas directamente para validar expiraciones sin esperar tiempo real.