> **Documento:** Roadmap  
> **Proyecto:** QA Automation Lab  
> **Última actualización:** Sprint 4  
> **Estado:** Vigente

# Roadmap

## Objetivo

Este documento describe la evolución del proyecto a través de los distintos sprints, mostrando las funcionalidades implementadas, las mejoras arquitectónicas incorporadas y los principales aprendizajes obtenidos durante el desarrollo.

El laboratorio evoluciona de forma incremental, incorporando nuevas capacidades en cada sprint con el objetivo de simular el crecimiento de una aplicación backend real y su infraestructura de QA Automation.

---

## Resumen de Sprints

|  Sprint  | Estado | Objetivo Principal           |
| :------: | :----: | ---------------------------- |
| Sprint 0 |    ✅   | Infraestructura inicial      |
| Sprint 1 |    ✅   | Introducción al Testing      |
| Sprint 2 |    ✅   | CRUD completo                |
| Sprint 3 |    ✅   | Seguridad y Autenticación    |
| Sprint 4 |    ✅   | QA Automation Avanzado       |
| Sprint 5 |   🚧   | Integración Continua (CI/CD) |

---

## Sprint 0 - Infraestructura Inicial

### Objetivos

* Crear la estructura base del proyecto.
* Implementar la API con FastAPI.
* Configurar PostgreSQL.
* Integrar SQLAlchemy.
* Incorporar Alembic para el versionado del esquema.
* Preparar la infraestructura mediante Docker.

### Implementaciones

* API REST inicial.
* Modelos SQLAlchemy.
* Base de datos PostgreSQL.
* Migraciones con Alembic.
* Contenedor Docker para PostgreSQL.

### Resultado

Se estableció la infraestructura base sobre la cual evolucionaría el laboratorio durante los siguientes sprints.

---

## Sprint 1 - Introducción al Testing

### Objetivos

* Incorporar Pytest.
* Diseñar la infraestructura de testing.
* Crear fixtures reutilizables.
* Separar el entorno de pruebas del entorno de desarrollo.

### Implementaciones

* Configuración inicial de Pytest.
* Fixtures comunes.
* Base de datos de testing.
* Cliente HTTP para pruebas.
* Primeros tests automatizados.

### Resultado

El proyecto adquirió una infraestructura básica para automatizar pruebas de forma reproducible.

---

## Sprint 2 - CRUD Completo

### Objetivos

* Implementar todas las operaciones CRUD.
* Consolidar la API REST.
* Mejorar las validaciones.

### Implementaciones

* Crear usuario.
* Obtener usuario.
* Listar usuarios.
* Actualizar usuario.
* Actualización parcial.
* Soft Delete.
* Validaciones mediante Pydantic.

### Resultado

La API alcanzó un estado funcional estable con soporte completo para la gestión de usuarios.

---

## Sprint 3 - Seguridad y Autenticación

### Objetivos

* Incorporar autenticación mediante JWT.
* Implementar autorización basada en roles (RBAC).
* Añadir recuperación de contraseña.
* Mejorar la seguridad de las cuentas.

### Implementaciones

* Login con JWT.
* Hashing de contraseñas.
* Bloqueo temporal por intentos fallidos.
* Roles (`USER` y `ADMIN`).
* Recuperación de contraseña mediante tokens.
* Servicio de correo desacoplado.
* Control de acceso mediante dependencias de FastAPI.

### Resultado

El laboratorio evolucionó desde una API CRUD a una aplicación con mecanismos de autenticación y autorización similares a los utilizados en aplicaciones reales.

---

## Sprint 4 - QA Automation Avanzado

### Objetivos

* Ampliar la infraestructura de testing.
* Incorporar técnicas avanzadas de automatización.
* Automatizar la preparación del entorno de pruebas.
* Mejorar la documentación técnica.

### Implementaciones

#### Automatización

* Mocking.
* Spy.
* Stub.
* Monkeypatch.
* Testing de servicios externos.
* Pruebas de integración.
* Flujos End-to-End.

#### Calidad

* Reportes HTML.
* Cobertura de código (98%).
* Eliminación de código muerto.
* Refactorización de endpoints.

#### Infraestructura

* Configuración centralizada mediante `Settings`.
* Cambio dinámico entre desarrollo y testing.
* Migraciones automáticas durante la ejecución de Pytest.
* Sincronización entre `users` y `users_test`.

#### Documentación

* README completamente reorganizado.
* Documentación de arquitectura.
* Documentación de testing.
* Documentación de Alembic.
* Documentación de Docker.
* Documentación del modelo de datos.
* Documentación funcional de la API.

### Resultado

El laboratorio alcanzó una arquitectura modular, una infraestructura de testing madura y una documentación técnica completa, acercándose al nivel de un proyecto backend profesional.

---

## Sprint 5 - Integración Continua (Planificado)

### Objetivos previstos

* GitHub Actions.
* Integración Continua (CI).
* Ejecución automática de pruebas.
* Publicación de reportes.
* Linters.
* Formateadores automáticos.
* Análisis estático.
* Quality Gates.

### Resultado esperado

Automatizar completamente el pipeline de calidad para que cada cambio sea validado antes de integrarse al proyecto.

---

## Evolución Arquitectónica

La arquitectura del proyecto evolucionó progresivamente durante el desarrollo.

```text
Sprint 0
Infraestructura Base
        │
        ▼
Sprint 1
Testing Automatizado
        │
        ▼
Sprint 2
API REST Completa
        │
        ▼
Sprint 3
Seguridad y RBAC
        │
        ▼
Sprint 4
QA Automation Avanzado
        │
        ▼
Sprint 5
CI/CD
```

Cada sprint incorporó nuevas capacidades sin perder la simplicidad de las etapas anteriores, permitiendo que la arquitectura creciera de manera incremental.

---

## Lecciones Aprendidas

El desarrollo del laboratorio permitió aplicar y consolidar conocimientos en distintas áreas del desarrollo backend y la automatización de pruebas.

Entre los principales aprendizajes destacan:

* Diseño de APIs REST.
* Modelado de bases de datos relacionales.
* SQLAlchemy y Alembic.
* Autenticación mediante JWT.
* Control de acceso basado en roles.
* Diseño de infraestructuras de testing.
* Mocking, Spy, Stub y Monkeypatch.
* Pruebas de integración y End-to-End.
* Gestión de cobertura y reportes.
* Organización y documentación de proyectos técnicos.

---

## Visión a Futuro

El laboratorio continuará evolucionando incorporando prácticas utilizadas habitualmente en proyectos profesionales de ingeniería de software y QA Automation.

Las próximas etapas estarán orientadas a fortalecer la automatización, la integración continua, la calidad del código y la escalabilidad de la arquitectura.

## Hitos de Proyecto

- ✅ Primera API REST funcional.
- ✅ Primera migración con Alembic.
- ✅ Primera suite automatizada con Pytest.
- ✅ Implementación de JWT.
- ✅ Implementación de RBAC.
- ✅ Recuperación de contraseña.
- ✅ Mocking y Monkeypatch.
- ✅ 98 % de cobertura.
- ✅ Migraciones automáticas en testing.
- ✅ Documentación técnica completa.