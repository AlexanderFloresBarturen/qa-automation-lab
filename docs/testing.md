> **Documento:** Testing  
> **Proyecto:** QA Automation Lab  
> **Última actualización:** Sprint 5  
> **Estado:** Vigente

# Testing

## Objetivo

Este documento describe la estrategia de testing utilizada en el proyecto, la infraestructura que soporta la ejecución de las pruebas y las principales decisiones tomadas para garantizar que la suite sea reproducible, aislada y mantenible.

El objetivo no es únicamente validar el correcto funcionamiento de la aplicación, sino construir una infraestructura de pruebas similar a la utilizada en proyectos profesionales de desarrollo backend y QA Automation.

---

## Filosofía de Testing

La estrategia de testing del proyecto se basa en cinco principios fundamentales:

* Independencia entre pruebas.
* Reproducibilidad.
* Aislamiento completo del entorno de desarrollo.
* Automatización del entorno de pruebas.
* Reutilización mediante fixtures y utilidades comunes.

Cada prueba debe poder ejecutarse de manera individual o como parte de la suite completa, obteniendo siempre el mismo resultado.

---

## Infraestructura de Testing

La ejecución de las pruebas utiliza una infraestructura independiente de la aplicación en desarrollo.

```text
pytest
    │
    ▼
Fixtures
    │
    ▼
Dependency Overrides
    │
    ▼
test_engine
    │
    ▼
users_test
```

Esta arquitectura permite reutilizar exactamente la misma aplicación FastAPI, sustituyendo únicamente la infraestructura necesaria para conectar con la base de datos de testing.

---

## Aislamiento del Entorno

Uno de los principales objetivos del laboratorio es garantizar que las pruebas nunca modifiquen la base de datos de desarrollo.

Para conseguirlo se implementaron varios mecanismos complementarios:

* Base de datos independiente (`users_test`).
* `test_engine` exclusivo para testing.
* `dependency_overrides` para sustituir `get_db()`.
* Rollback automático mediante transacciones.
* Creación automática de la base de datos de testing cuando no existe.
* Migraciones automáticas antes de ejecutar la suite.

Como resultado, todas las pruebas utilizan un entorno completamente aislado y reproducible.

---

## Preparación Automática del Entorno

La infraestructura de testing prepara automáticamente el entorno antes de ejecutar la primera prueba.

El proceso realiza las siguientes tareas:

1. Selecciona la configuración correspondiente al entorno de testing.
2. Comprueba si existe la base de datos `users_test`.
3. Crea la base de datos si aún no existe.
4. Aplica todas las migraciones disponibles mediante Alembic.
5. Inicia la ejecución de la suite.

Gracias a este proceso, un desarrollador únicamente necesita disponer de un servidor PostgreSQL operativo para ejecutar las pruebas.

---

## Organización de las Pruebas

La suite de pruebas sigue la misma organización por dominios utilizada por la aplicación.

Cada conjunto de pruebas se agrupa según la responsabilidad funcional que valida, facilitando la navegación por el proyecto y manteniendo una correspondencia directa con la estructura de los routers.

La estructura prevista es la siguiente:

```text
tests/
│
├── auth/
│   ├── test_login.py
│   ├── test_register.py
│   └── test_password_recovery.py
│
├── profile/
│   ├── test_get_profile.py
│   ├── test_update_profile.py
│   ├── test_patch_profile.py
│   └── test_delete_profile.py
│
├── users/
│   ├── test_get_users.py
│   ├── test_get_user.py
│   ├── test_create_user.py
│   ├── test_update_user.py
│   ├── test_patch_user.py
│   └── test_delete_user.py
│
├── conftest.py
├── database.py
├── helpers.py
└── test_database.py
```

Esta organización permite mantener una correspondencia clara entre la estructura de la API, los routers y la suite de pruebas, facilitando el mantenimiento y la evolución del proyecto.

---

## Fixtures

La infraestructura de testing se apoya en fixtures reutilizables que eliminan duplicación de código y facilitan la preparación del entorno de pruebas.

Entre las principales fixtures se encuentran:

| Fixture        | Responsabilidad                            |
| -------------- | ------------------------------------------ |
| `db`           | Sesión de base de datos para testing.      |
| `client`       | Cliente HTTP de FastAPI.                   |
| `created_user` | Usuario registrado previamente.            |
| `logged_user`  | Usuario autenticado.                       |
| `admin_user`   | Usuario autenticado con rol administrador. |
| `user_payload` | Generación dinámica de datos de prueba.    |

Este enfoque permite mantener los tests pequeños, independientes y fáciles de mantener.

---

## Tipos de Pruebas

Actualmente el laboratorio incorpora distintos niveles de pruebas automatizadas.

| Tipo        | Objetivo                                                                       |
| ----------- | ------------------------------------------------------------------------------ |
| Unitarias   | Validar funciones o comportamientos individuales.                              |
| Funcionales | Verificar el comportamiento de un endpoint específico.                         |
| Integración | Validar el funcionamiento conjunto de varios componentes.                      |
| End-to-End  | Comprobar flujos completos desde la petición inicial hasta el resultado final. |

La combinación de estos niveles permite aumentar la confianza en el comportamiento de la aplicación sin depender exclusivamente de un único tipo de prueba.

---

## Mocking

El proyecto utiliza Mock para sustituir dependencias externas cuya ejecución real no resulta necesaria durante las pruebas.

Actualmente esta técnica se aplica principalmente sobre el servicio de envío de correos electrónicos.

### Beneficios

* Evita depender de servicios externos.
* Reduce el tiempo de ejecución de la suite.
* Permite verificar llamadas y parámetros.
* Facilita el aislamiento de la lógica bajo prueba.

---

## Spy

Los Spy permiten ejecutar el comportamiento real de una función mientras registran las llamadas realizadas durante la prueba.

Se utilizan cuando resulta necesario comprobar la interacción entre componentes sin modificar su comportamiento.

---

## Stub

Los Stub sustituyen implementaciones reales por respuestas controladas.

Se utilizan para simplificar escenarios específicos y garantizar resultados deterministas durante las pruebas.

---

## Monkeypatch

Monkeypatch permite modificar temporalmente atributos, funciones o variables durante la ejecución de un test.

En este proyecto se utiliza para sustituir dependencias de forma controlada sin modificar permanentemente la implementación original.

Su principal ventaja es permitir simular distintos escenarios manteniendo completamente aislado el código de producción.

---

## Cobertura de Código

El proyecto utiliza Coverage.py para medir el porcentaje de código ejecutado por la suite de pruebas.

La cobertura no se utiliza únicamente como una métrica cuantitativa.

También sirve para:

* Detectar código muerto.
* Identificar rutas no ejercitadas.
* Descubrir casos de prueba faltantes.
* Guiar refactorizaciones.

Durante el Sprint 4 la revisión de cobertura permitió eliminar ramas de código que nunca podían ejecutarse, simplificando la implementación de varios endpoints.

---

## Reportes HTML

La suite genera reportes HTML para facilitar el análisis de la ejecución de las pruebas.

Estos reportes incluyen:

* Resultado individual de cada test.
* Tiempo de ejecución.
* Resumen general de la suite.
* Estado de éxito o fallo.

Este tipo de reportes resulta especialmente útil durante procesos de integración continua.

---

## Buenas Prácticas

Durante el desarrollo del laboratorio se adoptaron las siguientes prácticas:

* Cada test valida un único comportamiento.
* Los tests son independientes entre sí.
* No existe dependencia del orden de ejecución.
* Se utilizan fixtures para evitar duplicación.
* Las dependencias externas se aíslan mediante Mock cuando es necesario.
* Las pruebas de integración validan flujos completos del sistema.
* La base de datos de desarrollo nunca es utilizada durante la ejecución de la suite.
* La organización de la suite debe reflejar la organización de los dominios de la aplicación.

---

## Conclusiones

La infraestructura de testing evolucionó progresivamente junto con el proyecto.

Lo que comenzó como una pequeña colección de pruebas unitarias terminó convirtiéndose en una suite automatizada que incorpora aislamiento completo del entorno, pruebas de integración, mocking, monkeypatch, cobertura de código y generación de reportes.

Esta evolución permitió que el laboratorio no solo validara el funcionamiento de la aplicación, sino que también sirviera como un entorno para practicar técnicas de QA Automation utilizadas habitualmente en proyectos profesionales.
