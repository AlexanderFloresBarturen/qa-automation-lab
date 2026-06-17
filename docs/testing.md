# Testing y Base de Datos de Pruebas

## Objetivo

Garantizar que las pruebas automatizadas:

* Sean reproducibles.
* No modifiquen datos reales.
* Sean independientes entre sí.
* Puedan ejecutarse en cualquier momento.
* Mantengan una base de datos limpia después de cada test.

---

## Arquitectura de Testing

```text
Pytest
│
├── Fixture db
│
├── Fixture client
│
└── FastAPI
     │
     └── Dependency Override
          │
          ▼
     users_test
```

Todos los tests utilizan la base de datos:

```text
users_test
```

Nunca:

```text
users
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

Separar ambas bases evita que las pruebas modifiquen datos de desarrollo.

---

## Dependency Override

FastAPI permite reemplazar dependencias durante los tests.

Aplicación:

```python
def get_db():
    ...
```

Testing:

```python
app.dependency_overrides[get_db] = override_get_db
```

Gracias a esto:

```text
Endpoints
↓
users_test
```

en lugar de:

```text
Endpoints
↓
users
```

---

## Fixture db

### Implementación

```python
@pytest.fixture
def db():
    connection = test_engine.connect()

    transaction = connection.begin()

    db = TestingSessionLocal(bind=connection)

    yield db

    db.close()

    transaction.rollback()

    connection.close()
```

---

## Flujo de Ejecución

### Inicio

Se abre una conexión:

```python
connection = test_engine.connect()
```

---

### Transacción

Se crea una transacción:

```python
transaction = connection.begin()
```

Todas las operaciones del test ocurren dentro de ella.

---

### Sesión

La sesión se vincula explícitamente a la conexión:

```python
db = TestingSessionLocal(bind=connection)
```

Esto obliga a que todos los commits realizados por los endpoints queden contenidos dentro de la misma transacción.

---

### Finalización

Al terminar el test:

```python
transaction.rollback()
```

revierte todos los cambios realizados.

---

## ¿Por qué funciona?

Aunque un endpoint ejecute:

```python
db.commit()
```

la sesión está asociada a una transacción externa.

Por tanto:

```text
commit
≠ persistencia definitiva
```

Todo permanece dentro de la transacción abierta por el fixture.

Al ejecutar:

```python
transaction.rollback()
```

los cambios desaparecen.

---

## Aislamiento entre Tests

Cada test recibe:

```text
Nueva conexión
Nueva transacción
Nueva sesión
```

por lo que:

```text
Test A
```

no afecta a:

```text
Test B
```

---

## Fixture client

### Implementación

```python
@pytest.fixture
def client(db):

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
```

---

## Objetivo

Forzar que los endpoints utilicen la sesión creada por el fixture:

```python
db
```

en lugar de crear una nueva.

Esto permite que:

```text
Pytest
↓
FastAPI
↓
SQLAlchemy
```

compartan exactamente la misma transacción.

---

## ¿Por qué no crear una nueva sesión?

Esto sería incorrecto:

```python
def override_get_db():
    db = TestingSessionLocal()
    yield db
```

porque:

```text
Nueva sesión
↓
Nueva conexión
↓
Nueva transacción
```

El rollback del fixture principal no podría revertir esos cambios.

---

## Fixture Factory

Algunos fixtures generan datos dinámicamente.

Ejemplo:

```python
@pytest.fixture
def user_payload():
    def _user_payload(
        name="Pepe",
        age=49
    ):
        ...
    return _user_payload
```

Uso:

```python
payload = user_payload(
    name="Alex",
    age=25
)
```

---

## Fixture de Entidad Creada

Ejemplo:

```python
@pytest.fixture
def created_user(client, valid_user_payload):
    response = client.post(
        "/users",
        json=valid_user_payload
    )

    assert response.status_code == 201

    return response.json()
```

Permite reutilizar usuarios ya creados.

---

## Ventajas del Enfoque

### Gestión del Esquema

Los tests no crean ni eliminan tablas.

El esquema de la base de datos de testing es gestionado exclusivamente mediante Alembic:

```bash
alembic upgrade head
```

esto garantiza que la estructura utiizada durante las pruebas sea idéntica a la utilizada en desarrollo.

---

### Aislamiento

Cada prueba comienza con:

```text
Tabla vacía
```

y termina dejando:

```text
Tabla vacía
```

mediante rollback.

---

### Reproducibilidad

El resultado de una prueba no depende de ejecuciones anteriores.

---

### Simplicidad

No es necesario ejecutar:

```python
DELETE FROM users
```

antes o después de cada prueba.

---

## Flujo Completo

```text
Inicio test
│
├── Nueva conexión
│
├── Nueva transacción
│
├── Nueva sesión
│
├── Endpoint ejecuta commits
│
├── Test finaliza
│
├── Rollback
│
└── Conexión cerrada
```

Resultado:

```text
Base de datos limpia
```

para el siguiente test.

---

## Buenas Prácticas

### Utilizar siempre users_test

Nunca ejecutar pruebas sobre:

```text
users
```

---

### Compartir la misma sesión

Los endpoints deben utilizar:

```python
yield db
```

desde el fixture.

---

### Mantener rollback automático

Evita limpiezas manuales.

---

### Crear datos únicamente dentro del test

No depender de registros preexistentes.

---

## Lecciones Aprendidas

* FastAPI permite reemplazar dependencias mediante `dependency_overrides`.
* Una transacción externa puede contener los commits de los endpoints.
* `rollback()` elimina todos los cambios realizados durante una prueba.
* Cada test debe ser independiente de los demás.
* El aislamiento mediante transacciones es más eficiente que borrar registros manualmente.
* Compartir la misma sesión entre Pytest y FastAPI es fundamental para que el rollback funcione correctamente.
