> **Documento:** API  
> **Proyecto:** QA Automation Lab  
> **Última actualización:** Sprint 5  
> **Estado:** Vigente

# API

## Objetivo

Este documento describe la estructura funcional de la API REST del proyecto, los recursos disponibles, las convenciones utilizadas y las principales decisiones de diseño adoptadas durante su desarrollo.

La API sigue una organización basada en dominios funcionales, separando claramente las responsabilidades relacionadas con autenticación, perfil del usuario y administración de usuarios.

---

## Principios de Diseño

La API fue diseñada siguiendo los siguientes principios:

* Organización por dominios funcionales.
* Separación entre autenticación y administración.
* Uso de recursos REST.
* Validaciones mediante Pydantic.
* Autenticación basada en JWT.
* Autorización mediante RBAC.
* Soft Delete para usuarios.
* Respuestas tipadas mediante modelos Pydantic.

---

## Organización de la API

Actualmente la API se divide en tres dominios principales.

```text
Authentication
│
├── Login
├── Register
├── Forgot Password
└── Reset Password

Profile
│
├── Obtener perfil
├── Actualizar perfil
├── Actualización parcial
└── Eliminar cuenta

Users
│
└── Administración de usuarios
```

Cada dominio representa una responsabilidad distinta dentro del sistema.

---

## Authentication

Responsable de la autenticación de usuarios y de todas las operaciones relacionadas con la identidad de una cuenta.

### Endpoints

| Método | Endpoint | Descripción | Autenticación |
|---------|----------|-------------|----------------|
| POST | /auth/login | Iniciar sesión | No |
| POST | /auth/register | Registrar una nueva cuenta | No |
| POST | /auth/forgot-password | Solicitar recuperación de contraseña | No |
| POST | /auth/reset-password | Restablecer contraseña | No |

---

## Profile

Responsable de la gestión del usuario autenticado.

Todos estos endpoints obtienen el usuario directamente desde el JWT, por lo que no requieren un identificador en la URL.

### Endpoints

| Método | Endpoint | Descripción | Autenticación |
|---------|----------|-------------|----------------|
| GET | /profile | Obtener perfil | Sí |
| PUT | /profile | Actualizar completamente el perfil | Sí |
| PATCH | /profile | Actualización parcial del perfil | Sí |
| DELETE | /profile | Eliminar la cuenta (Soft Delete) | Sí |

---

## Users

Responsable de la administración de usuarios del sistema.

Todos los endpoints de este dominio requieren permisos de administrador.

Actualmente se encuentra en evolución.

### Endpoints

| Método | Endpoint | Descripción | Rol requerido |
|---------|----------|-------------|----------------|
| GET | /users | Listar usuarios | ADMIN |

### Evolución prevista

El dominio incorporará progresivamente:

| Método | Endpoint |
|---------|----------|
| GET | /users/{id} |
| POST | /users |
| PUT | /users/{id} |
| PATCH | /users/{id} |
| DELETE | /users/{id} |

---

## Autenticación

La API utiliza JSON Web Tokens (JWT).

Después de un inicio de sesión exitoso, el cliente debe incluir el token en el encabezado Authorization.

```http
Authorization: Bearer <token>
```

Los endpoints protegidos utilizan dependencias de FastAPI para obtener el usuario autenticado.

---

## Autorización

El proyecto implementa autorización basada en roles (RBAC).

Actualmente existen los siguientes roles:

| Rol | Descripción |
|------|-------------|
| USER | Usuario estándar |
| ADMIN | Administrador del sistema |

Los permisos se aplican mediante dependencias reutilizables.

```text
get_current_user
require_admin
```

---

## Validaciones

Las solicitudes utilizan modelos Pydantic para validar automáticamente:

* Tipos de datos.
* Longitudes mínimas y máximas.
* Formato del correo electrónico.
* Restricciones numéricas.
* Complejidad de contraseña.

Las validaciones se ejecutan antes de que la lógica del endpoint sea procesada.

---

## Soft Delete

La eliminación de usuarios se implementa mediante Soft Delete.

En lugar de eliminar físicamente un registro, el sistema marca al usuario como inactivo.

Esto permite:

* preservar la integridad referencial
* mantener trazabilidad
* evitar pérdidas accidentales de información.

---

## Convenciones REST

La API sigue las siguientes convenciones:

* GET para consultas.
* POST para creación de recursos.
* PUT para reemplazo completo.
* PATCH para modificaciones parciales.
* DELETE para eliminación lógica.

Los recursos se nombran utilizando sustantivos en plural cuando representan colecciones.

---

## Decisiones Arquitectónicas

Durante la evolución del proyecto se adoptó la separación de la API en tres dominios independientes.

### Authentication

Gestiona la identidad del usuario.

### Profile

Gestiona exclusivamente la cuenta del usuario autenticado.

Al eliminar el identificador del usuario en estos endpoints se reduce la superficie para ataques de tipo IDOR y se simplifica la lógica de autorización.

### Users

Gestiona la administración de usuarios por parte de administradores.

Esta separación permite mantener responsabilidades claras y facilita la evolución independiente de cada dominio.

---

## Evolución Futura

Las siguientes funcionalidades se incorporarán en futuras iteraciones:

* CRUD administrativo completo.
* Revocación de tokens.
* Refresh Tokens.
* Verificación de correo electrónico.
* Cambio de contraseña.
* Multi-Factor Authentication (MFA).
* Versionado de la API.
* Documentación OpenAPI enriquecida.

---

## Conclusiones

La organización por dominios permite mantener una API más clara, escalable y alineada con las responsabilidades del negocio.

La separación entre Authentication, Profile y Users facilita la evolución del sistema, reduce el acoplamiento entre funcionalidades y mejora tanto la mantenibilidad como la seguridad de la aplicación.