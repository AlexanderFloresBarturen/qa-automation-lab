> **Documento:** Arquitectura del Sistema  
> **Proyecto:** QA Automation Lab  
> **Última actualización:** Sprint 4  
> **Estado:** Vigente

# Arquitectura

## Objetivo

Este documento describe la arquitectura interna del proyecto, las principales decisiones de diseño y la forma en que interactán sus distintos componentes.

Su propósito es explicar **por qué** el sistema fue construido de esta manera, más que describir únicamente la estructura de carpetas.

---

## Principios de Diseño

El proyecto fue construido siguiendo los siguientes principios:

* Separación clara de responsabilidades.
* Componentes desacoplados.
* Configuración centralizada.
* Testing reproducible.
* Evolución controlada del esquema mediante migraciones.
* Arquitectura orientada a facilitar la automatización de pruebas.

---

## Arquitectura General

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

Cada capa posee una responsabilidad específica y evita depender directamente de capas superiores.

---

## Organización del Proyecto

```text
app/ 
│ 
├── core/ 
├── database/ 
├── models/ 
├── routes/ 
├── schemas/ 
├── security/ 
├── services/ 
└── utils/
```

Cada módulo agrupa una única responsabilidad dentro de la aplicación.

---

## Configuración Centralizada

Toda la configuración del proyecto se encuentra encapsulada en:

```text
app/core/settings.py
```

La clase `Settings` centraliza:

* Base de datos de desarrollo.
* Base de datos de testing.
* Configuración JWT.
* Parámetros de autenticación.
* Recuperación de contraseña.
* Entorno actualmente activo.

Esto evita duplicar configuraciones entre la aplicación, Alembic y Pytest.

---

## Gestión de Entornos

La aplicación distingue dos entornos de base de datos:

```text
Development
   │ 
   ▼ 
users

Testing
   │ 
   ▼ 
users_test
```

El cambio entre ambos entornos se realiza mediante:

```python
settings.use_development_database()

settings.use_test_database()
```

permitiendo compartir una única configuración entre todos los componentes del sistema.

---

## Capas de la Aplicación

### Routes

Los endpoints únicamente reciben la petición HTTP y coordinan el flujo de ejecución.

No contienen lógica de infraestructura ajena a la petición.

---

### Services 

Los servicios encapsulan funcionalidades reutilizables.

Ejemplo:

* Email Service

Esto facilita el uso de Mock, Spy y Monkeypatch durante las pruebas.

---

### Models

Representan las entidades persistentes mediante SQLAlchemy.

Cada modelo mantiene la definición del esquema y sus relaciones.

---

### Schemas

Define el contrato de entrada y salida de la API utilizando Pydantic.

Separar modelos y esquemas evita acoplar la persistencia con la interfaz HTTP.

---

### Security

Centraliza toda la lógica relacionado con:

* JWT
* Password hashing
* Dependencias de autenticación
* Control de acceso

---

### Database

Gestiona:

* Engine
* Sesiones
* Dependencias
* Conexiones

---

### Utils 

Agrupa utilidades reutilizables que no pertenecen a una capa específica.

---

## Flujo General de una Petición

```text
Cliente
   │ 
   ▼ 
FastAPI
   │ 
   ▼ 
Route
   │ 
   ▼ 
Service (cuando aplica)
   │ 
   ▼ 
Database
   │ 
   ▼ 
PostgreSQL
```

---

## Flujos Principales

Los siguientes diagramas muestran los principales flujos funcionales del sistema y cómo interactúan sus distintos componentes.

No representan la implementación detallada de cada endpoint, sino la secuencia general seguida por la aplicación para resolver los casos de uso más importantes.

---

### Flujo de Autenticación

El proceso de autenticación valida las credenciales del usuario y genera un JWT que será utilizado para autenticar las solicitudes posteriores.

```text
Cliente
    │
    ▼
POST /users/login
    │
    ▼
Buscar usuario
    │
    ▼
¿Cuenta activa?
    │
    ▼
¿Cuenta bloqueada?
    │
    ▼
Validar contraseña
    │
    ▼
Generar JWT
    │
    ▼
Respuesta
```

Este flujo también gestiona el incremento del contador de intentos fallidos, el bloqueo temporal de cuentas y el reinicio del contador cuando la autenticación se realiza correctamente.

---

### Flujo de Autorización (RBAC)

Una vez autenticado, cada endpoint protegido verifica tanto la identidad del usuario como los permisos necesarios para ejecutar la operación solicitada.

```text
Cliente
    │
    ▼
JWT
    │
    ▼
Validar Token
    │
    ▼
Obtener Usuario
    │
    ▼
Verificar Rol
    │
    ▼
¿Tiene permisos?
    │
 ┌──┴────────┐
 │           │
 ▼           ▼
Sí           No
 │           │
 ▼           ▼
Endpoint  403 Forbidden
```

Esta separación permite distinguir claramente entre autenticación (quién es el usuario) y autorización (qué acciones puede realizar).

---

### Flujo de Recuperación de Contraseña

La recuperación de contraseña fue diseñada para garantizar que únicamente exista un token válido por usuario y que cada token pueda utilizarse una única vez.

```text
Cliente
    │
    ▼
Forgot Password
    │
    ▼
Buscar Usuario
    │
    ▼
Invalidar Token Anterior
    │
    ▼
Generar Nuevo Token
    │
    ▼
Guardar Token
    │
    ▼
Email Service
    │
    ▼
Reset Password
    │
    ▼
Validar Token
    │
    ▼
Actualizar Contraseña
    │
    ▼
Invalidar Token
```

El proceso contempla la expiración de tokens, la invalidación automática de solicitudes anteriores y el desbloqueo de cuentas cuando el cambio de contraseña se completa correctamente.

---

### Flujo de Infraestructura de Testing

La infraestructura de testing reutiliza exactamente la misma aplicación que el entorno de desarrollo, sustituyendo únicamente la infraestructura necesaria para mantener un entorno completamente aislado.

```text
pytest
    │
    ▼
pytest_sessionstart
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
Dependency Overrides
    │
    ▼
test_engine
    │
    ▼
Endpoints
```

Gracias a este flujo, las pruebas automatizadas ejecutan el mismo código de producción utilizando una base de datos independiente, garantizando el aislamiento de los datos y la reproducibilidad de la suite de pruebas.

---

### Relación entre los Flujos

Los cuatro procesos anteriores representan el funcionamiento general de la aplicación.

```text
Cliente
    │
    ▼
Autenticación
    │
    ▼
Autorización (RBAC)
    │
    ▼
Endpoints
    │
    ├──────────────┐
    │              │
    ▼              ▼
Operaciones    Recuperación
Normales       de Contraseña

        Testing
            ▲
            │
   Ejecuta todos los flujos
   sobre un entorno aislado
```

Esta organización permite mantener separadas las responsabilidades de autenticación, autorización, recuperación de credenciales e infraestructura de pruebas, facilitando tanto el mantenimiento como la automatización del proyecto.


---

## ¿Por qué centralizar la configuración?

### Problema

A medida que el proyecto fue creciendo, distintos componentes comenzaron a necesitar información compartida.

Entre ellos:

* FastAPI
* Alembic
* Pytest
* JWT
* Recuperación de contraseñas

Mantener configuraciones independientes para cada uno aumentaba el riesgo de inconsistencias y dificultaba el mantenimiento del proyecto.

--- 

### Decisión

Se decidió centralizar toda la configuración en una única clase:

```text
Settings
```

de forma que cualquier componente del sistema obtenga su configuración desde una única fuente de verdad.

---

### Resultado

Actualmente la configuración es compartida por:

```text
             Settings 
                │ 
    ┌───────────┼───────────┐ 
    │           │           │ 
    ▼           ▼           ▼ 
 FastAPI     Alembic      Pytest
```

Este enfoque reduce la duplicación de código, simplifica el mantenimiento y facilita la incorporación de nuevos entornos de ejecución en el futuro.

---

## ¿Por qué utilizar Dependency Overrides?

### Problema

La aplicación utiliza una sesión de base de datos obtenida mediante la dependencia `get_db()`.

Durante las pruebas automatizadas era necesario evitar que los endpoints utilizaran la base de datos de desarrollo.

---

### Decisión

FastAPI permite reemplazar dependencias mediante `dependency_overrides`.

Durante los tests, `get_db()` es sustituido por una implementación que utiliza una sesión asociada exclusivamente a la base de datos de testing.

De esta manera, toda la aplicación continúa utilizando exactamente el mismo código, mientras que únicamente cambia el origen de la sesión.

---

### Beneficios

* No fue necesario modificar los endpoints para soportar testing.
* El código de producción permanece idéntico durante las pruebas.
* Los tests utilizan una infraestructura completamente aislada.
* La aplicación continúa dependiendo únicamente de `get_db()`, sin conocer si se encuentra ejecutándose en desarrollo o testing.

---

## ¿Por qué existe un `test_engine` independiente?

### Problema

El `engine` principal de SQLAlchemy se crea durante la inicialización de la aplicación utilizando la base de datos de desarrollo.

Reutilizar ese mismo `engine` durante las pruebas aumentaría el riesgo de ejecutar operaciones sobre datos reales.

---

### Decisión

La infraestructura de testing crea un `test_engine` independiente y que está conectado exclusivamente a la base de datos `users_test`.

Este `engine` es utilizado únicamente mediante `dependency_overrides`, sin modificar la configuración de la aplicación.

---

### Beneficios

* Separación completa entre desarrollo y testing.
* Eliminación del riesgo de modificar datos de desarrollo durante las pruebas.
* Mayor estabilidad y reproducibilidad de la suite de tests.
* Posibilidad de ejecutar pruebas repetidamente sin afectar el entorno principal.

---

## ¿Por qué separar Routes y Services?

### Problema

Cuando los endpoints contienen toda la lógica de negocio, terminan acumulando responsabilidades que dificultan el mantenimiento y las pruebas.

Además, funcionalidades reutilizables como el envío de correos electrónicos quedan acopladas a un único endpoint.

### Decisión

Los endpoints se limitan a coordinar la petición HTTP, mientras que la lógica reutilizable se encapsula en servicios independientes.

Actualmente esta separación se utiliza, por ejemplo, en el servicio de envío de correos electrónicos.

### Beneficios

* Mayor reutilización de código.
* Menor acoplamiento entre componentes.
* Posibilidad de aplicar Mock, Spy y Monkeypatch sobre los servicios.
* Facilita incorporar nuevos servicios sin modificar la estructura general de la aplicación.

---

## ¿Por qué implementar RBAC mediante una tabla `roles`?

### Problema

Una alternativa sencilla consiste en almacenar el rol del usuario como una cadena de texto.

Sin embargo, este enfoque dificulta mantener la integridad de los datos y limita la posibilidad de ampliar el sistema con nuevos roles.

---

### Decisión

Los roles fueron modelados como una entidad independiente relacionada con los usuarios mediante SQLAlchemy.

Este diseño representa de forma más fiel un sistema de autorización basado en roles (RBAC).

---

### Beneficios

* Integridad referencial.
* Escalabilidad para incorporar nuevos roles.
* Modelo de datos más cercano a aplicaciones reales.
* Relaciones administradas directamente por el ORM.

---

## ¿Por qué utilizar Soft Delete?

### Problema

Eliminar registros físicamente provoca la pérdida permanente de información y dificulta realizar auditorías o recuperar datos eliminados por error.

---

### Decisión

Los usuarios se marcan como inactivos mediante el campo `is_active`, evitando eliminar el registro de la base de datos.

Todos los endpoints filtran únicamente los usuarios activos.

---

### Beneficios

* Conservación del historial.
* Posibilidad de restaurar registros.
* Mayor seguridad frente a eliminaciones accidentales.
* Estrategia utilizada habitualmente en aplicaciones empresariales.

---

## ¿Por qué crear una tabla `password_reset_tokens`?

### Problema

Guardar un único token directamente en la tabla `users` limita la información disponible sobre el proceso de recuperación y dificulta controlar el estado de cada solicitud.

---

### Decisión

Se creó una entidad independiente para almacenar los tokens de recuperación, incluyendo su propietario, fecha de creación, expiración y estado de uso.

Cada nueva solicitud invalida automáticamente el token anterior.

---

### Beneficios

* Modelo de datos normalizado.
* Mayor flexibilidad para futuras ampliaciones.
* Gestión independiente del ciclo de vida de cada token.
* Mejor alineación con implementaciones utilizadas en aplicaciones reales.

---

## ¿Por qué utilizar Alembic?

### Problema

Modificar el esquema de la base de datos manualmente dificulta reproducir los cambios entre distintos entornos y aumenta el riesgo de inconsistencias.

---

### Decisión

Todas las modificaciones del esquema se gestionan mediante migraciones versionadas utilizando Alembic.

La aplicación y la infraestructura de testing utilizan las mismas migraciones, garantizando que ambos entornos compartan exactamente la misma estructura.

---

### Beneficios

* Versionado del esquema.
* Sincronización entre desarrollo y testing.
* Historial completo de cambios.
* Automatización de la inicialización de la base de datos de pruebas.

---

## Evolución de la Arquitectura

La arquitectura del proyecto no fue diseñada completamente desde el inicio. Evolucionó de forma incremental conforme aparecieron nuevos requisitos funcionales y de testing. Esta evolución permitió introducir mejoras de diseño cuando realmente fueron necesarias, manteniendo el proyecto simple durante las primeras etapas y aumentando progresivamente su nivel de modularidad, automatización y mantenibilidad.
