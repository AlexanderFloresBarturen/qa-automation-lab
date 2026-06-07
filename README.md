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

---

## Reglas de Negocio

### Usuarios

* El nombre debe contener entre 2 y 50 caracteres.
* El email debe tener formato válido.
* La edad debe estar entre 18 y 65 años.
* No pueden existir dos usuarios activos con el mismo email.
* Un usuario eliminado lógicamente puede reutilizar su email.
* Los usuarios inactivos no pueden ser consultados mediante la API.

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

---

## Testing

### Fixtures

* client
* valid_user_payload
* created_user

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

### Pytest

* Fixtures
* Reutilización de setup
* Datos dinámicos
* Aislamiento de pruebas

### Bases de Datos

* Persistencia
* Integridad de datos
* Soft Delete

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
│   ├── test_get_user.py
│   └── test_delete_user.py
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
* [x] DELETE User (Soft Delete)
* [x] Validaciones de entrada
* [x] Fixtures reutilizables

### Sprint 2 - Gestión de Usuarios Avanzada

* [ ] PUT User
* [ ] Reutilización de email tras Soft Delete
* [ ] Validaciones avanzadas
* [ ] Persistencia validada desde tests

### Sprint 3 - Autenticación

* [ ] Login
* [ ] Bloqueo de cuenta
* [ ] Recuperación de contraseña
* [ ] Reglas de autenticación

### Sprint 4 - Automatización Avanzada

* [ ] Mocking
* [ ] Parametrización
* [ ] Fixtures avanzadas
* [ ] Base de datos de pruebas
* [ ] Cobertura de código

### Sprint 5 - Integración Continua

* [ ] GitHub Actions
* [ ] Ejecución automática de tests
* [ ] Reportes HTML

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
