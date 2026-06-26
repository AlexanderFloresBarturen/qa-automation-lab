> **Documento:** Modelo de Datos  
> **Proyecto:** QA Automation Lab  
> **Última actualización:** Sprint 4  
> **Estado:** Vigente

# Modelo de Datos

## Objetivo

Este documento describe el modelo de datos utilizado por el proyecto, las relaciones entre entidades y las principales restricciones definidas en la base de datos.

Su objetivo es proporcionar una visión conceptual del esquema persistente sin entrar en detalles de implementación específicos de SQLAlchemy o Alembic.

---

## Diagrama Entidad–Relación

```text
           Role
             │
         1 ──┴── N
             │
           User
             │
         1 ──┴── N
             │
      PasswordResetToken
```

---

## Entidades

### Role

Representa los distintos perfiles de autorización disponibles en la aplicación.

#### Campos

| Campo | Tipo    | Descripción    |
| ----- | ------- | -------------- |
| id    | Integer | Clave primaria |
| name  | String  | Nombre del rol |

#### Relaciones

* Un rol puede estar asociado a múltiples usuarios.

---

### User

Representa los usuarios registrados en el sistema.

#### Campos

| Campo                 | Tipo     | Descripción                |
| --------------------- | -------- | -------------------------- |
| id                    | Integer  | Clave primaria             |
| name                  | String   | Nombre del usuario         |
| email                 | String   | Correo electrónico (único) |
| password_hash         | String   | Contraseña cifrada         |
| age                   | Integer  | Edad                       |
| role_id               | Integer  | Rol asignado               |
| failed_login_attempts | Integer  | Intentos fallidos          |
| locked_until          | DateTime | Fin del bloqueo temporal   |
| is_active             | Boolean  | Estado lógico del usuario  |

#### Relaciones

* Pertenece a un único rol.
* Puede tener múltiples tokens de recuperación.

---

### PasswordResetToken

Almacena los tokens utilizados durante el proceso de recuperación de contraseña.

#### Campos

| Campo      | Tipo     | Descripción                         |
| ---------- | -------- | ----------------------------------- |
| id         | Integer  | Clave primaria                      |
| user_id    | Integer  | Usuario propietario                 |
| token      | String   | Token de recuperación               |
| used       | Boolean  | Indica si el token ya fue utilizado |
| created_at | DateTime | Fecha de creación                   |
| expires_at | DateTime | Fecha de expiración                 |

#### Relaciones

* Cada token pertenece a un único usuario.

---

### Relaciones

| Relación                  | Cardinalidad |
| ------------------------- | ------------ |
| Role → User               | `1:N`        |
| User → PasswordResetToken | `1:N`        |

---

## Restricciones

### Integridad

* `role_id` referencia la tabla `roles`.
* `user_id` referencia la tabla `users`.
* Los tokens se eliminan automáticamente cuando el usuario es eliminado físicamente (`ON DELETE CASCADE`).

---

### Restricciones de Unicidad

| Campo | Restricción |
| ----- | ----------- |
| email | UNIQUE      |
| token | UNIQUE      |

---

### Restricciones Lógicas

El modelo incorpora restricciones de negocio adicionales:

* El email debe ser único.
* Solo existe un token de recuperación activo por usuario.
* Un token únicamente puede utilizarse una vez.
* Los usuarios eliminados lógicamente permanecen almacenados mediante `is_active`.

---

## Decisiones de Diseño

El modelo de datos fue diseñado siguiendo criterios de normalización y separación de responsabilidades.

Las decisiones arquitectónicas que motivaron la creación de entidades independientes (`Role`, `PasswordResetToken`) se describen con mayor detalle en [Arquitectura](/docs/architecture.md).

---

## Evolución del Modelo

La estructura de la base de datos evoluciona mediante migraciones versionadas utilizando Alembic.

Cada modificación del esquema genera una nueva migración, garantizando que todos los entornos compartan la misma estructura.

Los detalles del proceso de versionado se documentan en [Alembic](/docs/alembic.md).

| Entidad            | Estado |
| ------------------ | ------ |
| Role               |    ✅   |
| User               |    ✅   |
| PasswordResetToken |    ✅   |
