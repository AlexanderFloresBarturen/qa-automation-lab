> **Documento:** Alembic  
> **Proyecto:** QA Automation Lab  
> **Última actualización:** Sprint 4  
> **Estado:** Vigente

# Gestión de Migraciones

## Objetivo

Este documento describe la estrategia utilizada para gestionar la evolución del esquema de la base de datos mediante Alembic.

El objetivo es garantizar que todos los entornos del proyecto compartan exactamente la misma estructura de base de datos y que las modificaciones del esquema puedan versionarse, reproducirse y automatizarse de forma segura.

---

## ¿Por qué utilizar Alembic?

Durante el desarrollo de una aplicación el modelo de datos evoluciona constantemente.

Modificar el esquema manualmente dificulta reproducir los cambios entre distintos entornos y aumenta el riesgo de inconsistencias.

Alembic permite:

* Versionar el esquema de la base de datos.
* Registrar la evolución del modelo de datos.
* Aplicar cambios de forma reproducible.
* Mantener sincronizados todos los entornos del proyecto.

---

## Flujo de Trabajo

La evolución del esquema sigue el siguiente proceso:

```text
Modificar modelos SQLAlchemy
            │
            ▼
Generar migración
            │
            ▼
Revisar migración
            │
            ▼
Aplicar migración
            │
            ▼
Actualizar esquema
```

Cada modificación del modelo debe quedar registrada mediante una nueva migración.

---

## Estructura

```text
alembic/
│
├── env.py
├── versions/
└── script.py.mako
```

### env.py

Configura el contexto de ejecución de Alembic.

En este proyecto obtiene la configuración directamente desde `Settings`, evitando duplicar la URL de conexión en múltiples lugares.

### versions/

Contiene el historial completo de migraciones versionadas.

Cada archivo representa un cambio específico sobre el esquema de la base de datos.

---

## Configuración Centralizada

Uno de los principales cambios introducidos durante el Sprint 4 fue eliminar la dependencia directa de `alembic.ini` como fuente de configuración.

Actualmente el flujo es:

```text
Settings
     │
     ▼
DATABASE_URL
     │
     ▼
env.py
     │
     ▼
Alembic
```

Gracias a este enfoque, Alembic utiliza automáticamente la configuración correspondiente al entorno activo.

---

## Desarrollo

Cuando se modifica un modelo SQLAlchemy, el flujo habitual consiste en:

1. Actualizar el modelo.
2. Generar una nueva migración.
3. Revisar el código generado.
4. Aplicar la migración sobre la base de datos de desarrollo.

Este proceso mantiene sincronizado el esquema de la base `users`.

---

## Testing

La base de datos de testing sigue un flujo diferente.

Durante la ejecución de la suite de pruebas ocurre automáticamente:

```text
pytest
    │
    ▼
pytest_sessionstart()
    │
    ▼
Settings
    │
    ▼
Seleccionar users_test
    │
    ▼
Alembic Upgrade Head
    │
    ▼
Inicio de la suite
```

De esta manera, la base `users_test` siempre comienza las pruebas utilizando la última versión disponible del esquema.

No es necesario ejecutar migraciones manualmente antes de lanzar la suite.

---

## Sincronización entre Entornos

La arquitectura garantiza que ambas bases de datos compartan exactamente las mismas migraciones.

```text
SQLAlchemy Models
        │
        ▼
Alembic Migration
  ┌─────┴──────────┐
  ▼                ▼
users         users_test
```

Esto elimina el riesgo de que desarrollo y testing evolucionen de forma independiente.

---

## Buenas Prácticas

Durante el desarrollo del laboratorio se siguen las siguientes recomendaciones:

* Cada cambio del esquema debe generar una migración independiente.
* Revisar siempre el código generado automáticamente por Alembic.
* No modificar manualmente la tabla `alembic_version`.
* Mantener las migraciones pequeñas y fáciles de revisar.
* Versionar todas las migraciones junto con el código fuente.

---

## Conclusiones

La incorporación de Alembic permitió que la evolución del esquema pasara a formar parte del propio ciclo de desarrollo del proyecto.

Gracias a la integración con `Settings` y la automatización realizada mediante Pytest, tanto la base de desarrollo como la base de testing permanecen sincronizadas utilizando exactamente el mismo historial de migraciones.

Esta estrategia elimina tareas manuales, reduce inconsistencias entre entornos y facilita la evolución del modelo de datos conforme el proyecto continúa creciendo.

## Comandos de uso Frecuente

```bash
# Crear migración
alembic revision --autogenerate -m "Descripción"

# Aplicar migraciones
alembic upgrade head

# Revertir una migración
alembic downgrade -1

# Mostrar historial
alembic history

# Mostrar versión actual
alembic current

# Registrar Baseline
alembic stamp head
```