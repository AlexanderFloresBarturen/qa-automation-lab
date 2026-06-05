# QA Automation Lab

Proyecto práctico de entrenamiento en QA Automation utilizando Python.

## Objetivos

- Aprender diseño de casos de prueba
- Practicar API Testing
- Automatizar pruebas con Pytest
- Aplicar buenas prácticas de QA

---

## Tecnologías

- Python
- FastAPI
- Pytest
- SQLAlchemy
- SQLite
- Docker
- Git

---

## Estado actual

### Sprint 1 - Gestión de Usuarios

#### Implementado

- Endpoint raíz (`GET /`)
- Endpoint de creación de usuarios (`POST /users`)
- Validaciones con Pydantic:
  - Nombre entre 2 y 50 caracteres
  - Email válido
  - Edad entre 18 y 65 años

#### Testing

- Fixture de Pytest para TestClient
- Primeros tests automatizados:
  - Registro exitoso
  - Nombre demasiado corto

---

## Estructura del proyecto

```text
qa-automation-lab/
│
├── app/
│   ├── main.py
│   ├── schemas.py
│   ├── models.py
│   ├── database.py
│   └── routes/
│       └── users.py
│
├── tests/
│   ├── conftest.py
│   └── test_create_user.py
│
├── requirements.txt
└── README.md
```

---

## Roadmap

### Sprint 1
- [x] API básica
- [x] Validaciones de entrada
- [ ] Persistencia SQLite
- [ ] GET User
- [ ] DELETE User

### Sprint 2
- [ ] Login
- [ ] Bloqueo de cuenta
- [ ] Reglas de autenticación

### Sprint 3
- [ ] Productos
- [ ] Inventario

### Sprint 4
- [ ] Carrito de compras
- [ ] Cupones de descuento

### Sprint 5
- [ ] Automatización avanzada
- [ ] Fixtures avanzadas
- [ ] Parametrización
- [ ] Reportes

### Sprint 6
- [ ] Integración continua
- [ ] GitHub Actions

---

## Lecciones aprendidas

- FastAPI devuelve HTTP 422 para errores de validación de Pydantic.
- TestClient permite probar APIs sin levantar Uvicorn.
- Las fixtures de Pytest ayudan a reutilizar recursos entre pruebas.
- `python -m pytest` puede evitar problemas de resolución de entornos en Windows.

