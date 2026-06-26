> **Documento:** API  
> **Proyecto:** QA Automation Lab  
> **Última actualización:** Sprint 4  
> **Estado:** Vigente

# API

## Objetivo

Este documento describe el comportamiento funcional de la API, los recursos disponibles, las reglas de negocio implementadas y los permisos necesarios para acceder a cada operación.

La documentación detallada del contrato HTTP (parámetros, esquemas y respuestas) se encuentra disponible automáticamente mediante Swagger/OpenAPI.

---

## Recursos Disponibles

Actualmente la API expone los siguientes recursos:

| Recurso           | Descripción                 |
| ----------------- | --------------------------- |
| Users             | Gestión de usuarios.        |
| Authentication    | Autenticación mediante JWT. |
| Password Recovery | Recuperación de contraseña. |

---

## Endpoints

### Gestión de Usuarios

| Método | Endpoint      | Descripción                                        |
| ------ | ------------- | -------------------------------------------------- |
| POST   | `/users`      | Registrar un nuevo usuario.                        |
| GET    | `/users`      | Obtener todos los usuarios (solo administradores). |
| GET    | `/users/{id}` | Obtener un usuario específico.                     |
| PUT    | `/users/{id}` | Reemplazar completamente un usuario.               |
| PATCH  | `/users/{id}` | Actualizar parcialmente un usuario.                |
| DELETE | `/users/{id}` | Eliminar lógicamente un usuario.                   |

---

### Autenticación

| Método | Endpoint       | Descripción                       |
| ------ | -------------- | --------------------------------- |
| POST   | `/users/login` | Autenticar usuario y generar JWT. |

---

### Recuperación de Contraseña

| Método | Endpoint                 | Descripción                                       |
| ------ | ------------------------ | ------------------------------------------------- |
| POST   | `/users/forgot-password` | Generar un token de recuperación.                 |
| POST   | `/users/reset-password`  | Cambiar la contraseña utilizando un token válido. |

---

## Reglas de Negocio

### Registro de Usuarios

Durante el registro se aplican las siguientes reglas:

* El correo electrónico debe ser único.
* La contraseña debe cumplir la política definida por la aplicación.
* La edad debe encontrarse dentro del rango permitido.
* El usuario se crea con el rol predeterminado (`USER`).
* El usuario se registra como activo.

---

### Autenticación

El proceso de autenticación implementa las siguientes reglas:

* Las credenciales deben ser válidas.
* Los usuarios inactivos no pueden autenticarse.
* Las cuentas bloqueadas rechazan el acceso.
* Cada intento fallido incrementa el contador de errores.
* Después de cinco intentos fallidos la cuenta queda bloqueada temporalmente.
* Un inicio de sesión exitoso reinicia el contador de intentos fallidos.
* La autenticación genera un JWT para las solicitudes posteriores.

---

### Recuperación de Contraseña

El proceso de recuperación implementa las siguientes reglas:

* Solo existe un token activo por usuario.
* Cada nueva solicitud invalida automáticamente el token anterior.
* Los tokens poseen fecha de expiración.
* Cada token puede utilizarse una única vez.
* Una recuperación de contraseña exitosa invalida el token utilizado.
* Al restablecer la contraseña también se desbloquea la cuenta del usuario.

---

### Eliminación de Usuarios

La eliminación utiliza la estrategia **Soft Delete**.

Como consecuencia:

* El registro permanece almacenado.
* El usuario deja de estar disponible para la aplicación.
* Los endpoints únicamente trabajan con usuarios activos.

---

## Control de Acceso (RBAC)

El acceso a los endpoints depende del rol autenticado.

| Endpoint                    | USER | ADMIN |
| --------------------------- | ---- | ----- |
| Crear usuario               |   ✅  |   ✅   |
| Obtener usuario propio      |   ✅  |   ✅   |
| Obtener listado de usuarios |   ❌  |   ✅   |
| Actualizar usuario propio   |   ✅  |   ✅   |
| Eliminar usuarios           |   ❌  |   ❌   |

La autenticación y la autorización se encuentran desacopladas.

La identidad del usuario se valida mediante JWT y posteriormente se verifican los permisos asociados a su rol.

**Nota:** En la versión actual del laboratorio, el rol ADMIN únicamente habilita el acceso al listado completo de usuarios. Las operaciones sobre recursos individuales (GET, PUT, PATCH y DELETE por identificador) continúan restringidas al propietario del recurso. La ampliación de privilegios administrativos podrá incorporarse en futuras versiones.

---

## Flujos Funcionales

### Registro

```text
Cliente
    │
    ▼
Validación
    │
    ▼
Crear Usuario
    │
    ▼
Persistencia
    │
    ▼
Respuesta
```

---

### Inicio de Sesión

```text
Cliente
    │
    ▼
Validar Credenciales
    │
    ▼
Generar JWT
    │
    ▼
Respuesta
```

---

### Recuperación de Contraseña

```text
Forgot Password
      │
      ▼
Generar Token
      │
      ▼
Reset Password
      │
      ▼
Actualizar Contraseña
```

Los detalles de implementación de estos flujos se describen en [Arquitectura](/docs/architecture.md).

---

## Códigos HTTP

La API utiliza códigos HTTP consistentes para representar el resultado de cada operación.

| Código | Significado                                       |
| ------ | ------------------------------------------------- |
| 200    | Operación completada correctamente.               |
| 201    | Recurso creado.                                   |
| 400    | Solicitud inválida o regla de negocio incumplida. |
| 401    | Credenciales inválidas.                           |
| 403    | Acceso prohibido.                                 |
| 404    | Recurso no encontrado.                            |
| 409    | Conflicto (por ejemplo, correo duplicado).        |
| 422    | Error de validación.                              |
| 423    | Cuenta bloqueada temporalmente.                   |

---

## Principios de Diseño

La API fue diseñada siguiendo los siguientes principios:

* Endpoints con responsabilidades claras.
* Separación entre autenticación y autorización.
* Validación mediante Pydantic.
* Manejo consistente de códigos HTTP.
* Aplicación de reglas de negocio en el backend.
* Documentación automática mediante Swagger/OpenAPI.

---

## Limitaciones Actuales

En la versión actual del laboratorio:

- No existe Refresh Token.
- No se implementa envío real de correos electrónicos.
- No existe paginación del listado de usuarios.
- No se dispone de auditoría de operaciones.

---

## Referencias

* [Arquitectura](/docs/architecture.md) describe las decisiones de diseño y los flujos internos.
* [Modelo de Datos](/docs/database.md) documenta el modelo de datos utilizado por la aplicación.
* [Testing](/docs/testing.md) explica la estrategia de pruebas aplicada a cada funcionalidad.
* [Alembic](/docs/alembic.md) describe la gestión de las migraciones del esquema.
