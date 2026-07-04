>**Documento:** Desarrollo  
>**Proyecto:** QA Automation Lab  
>**Última actualización:** Sprint 5  
>**Estado:** En desarrollo

# Desarrollo

## Objetivo

Este documento describe el flujo de desarrollo adoptado por el proyecto, las herramientas utilizadas para garantizar la calidad del código y las decisiones tomadas durante la construcción del pipeline de desarrollo.

A diferencia de `testing.md`, que documenta la estrategia de pruebas, este documentos se centra en las prácticas de ingeniería que permiten mantener un código consistente, legible y preparado para su integración continua.

---

## Filosofía

A partir del Sprint 5, el proyecto adopta un enfoque basado en ingeniería de software, donde la calidad del código se valida de forma automática antes de su integración.

Cada herramienta incorporada debe cumplir al menos uno de los siguientes objetivos:

* Detectar errores antes de la ejecución.
* Mejorar la legibilidad del código.
* Automatizar tareas repetitivas.
* Facilitar el mantenimiento del proyecto.
* Integrarse con el pipeline de CI.

Las herramientas se incorporan progesivamente, comprendiendo primero el problema que resuelven antes de integrarlas al laboratorio.

---

## Flujo de Desarrollo

El objetivo final del Sprint 5 es construir el siguiente flujo de trabajo:

```text
Editar Código
      │
      ▼
Ruff (Lint / Análisis estático)
      │
      ▼
Black (Formato)
      │
      ▼
isort (Imports)
      │
      ▼
MyPy (Tipos)
      │
      ▼
   Commit
      │
      ▼
    Push
      │
      ▼
GitHub Actions
      │
      ▼
  PostgreSQL
      │
      ▼
   Alembic
      │
      ▼
   Pytest
      │
      ▼
Pull Request
      │
      ▼
    Merge
```

Cada etapa valida un aspecto distinto de la calidad del proyecto antes de permitir que los cambios sean integrados.

---

## Principios de Calidad

El laboratorio adopta los siguientes principios durante del desarrollo:

* El código debe ser legible.
* La calidad debe validarse automáticamente.
* Las herramientas deben complementar al desarrollador, no sustituirlo.
* La configuración debe mantenerse centralizada.
* Los errores debe detectarse lo antes posible dentro del ciclo de desarrollo.

Estos principios guían la incorporación de todas las herramientas utilizadas durante el Sprint 5.

---

## Configuración Centralizada

Una de las primeras decisiones arquitectónicas del Sprint consiste en centralizar la configuración de las herramientas de calidad utilizando `pyproject.toml`.

Esta decisión evita la proliferación de archivos de configuración independientes y sigue el estándar adoptado por gran parte del ecosistema Python moderno.

El objetivo es disponer de un único punto de configuración para herramientas como:

* Ruff
* Black
* isort
* MyPy
* Pytest (cuando resulte apropiado)
* Otras herramientas compatibles con `pyproject.toml`

---

## Herramientas

Las herramientas incorporadas durante este Sprint se documentan en las siguientes secciones.

### Ruff

**Estado:** ✅ Implementado

#### Objetivo

Realizar análisis estático del código para detectar errores comunes antes de ejecutar la suite de pruebas, permitiendo identificar problemas de calidad antes de que el código llegue al pipeline de CI.

#### Comando

```bash
ruff check .
```

#### Configuración Adoptada

Ruff se configura mediante `pyproject.toml`, siguiendo la estrategia de centralizar la configuración de todas las herramientas de calidad del proyecto en un único archivo.

Durante el Sprint 5 se decidió comenzar con una configuración mínima y fácil de evolucionar:

* Reglas habilitadas:

  * E: errores básicos de estilo.
  * F: errores detectados por `Pyflakes` (variables sin usar, imports innecesarios, nombres no definidos, etc.).
* Longitud máxima de línea adaptada al proyecto.
* Uso de `per-file-ignores` únicamente cuando existe una justificación técnica.

#### Decisiones de Ingeniería

Durante la integración de Ruff se adoptaron las siguientes decisiones:

* Incorporar únicamente las familias de reglas E y F como punto de partida, ampliando la configuración únicamente cuando el proyecto lo requiera.
* Priorizar reglas que detecten errores reales sobre reglas puramente estéticas.
* Mantener una configuración sencilla, explícita y fácilmente mantenible.
* Evitar copiar configuraciones genéricas sin comprender el propósito de cada opción.

#### Excepciones Justificadas

El proyecto evita deshabilitar reglas de análisis estático de forma global. Sin embargo, existen casos particulares, como `alembic/env.py`, donde se realizan importaciones únicamente para registrar los modelos SQLAlchemy en `Base.metadata`. 

En estos casos se utiliza `per-file-ignores` para documentar explícitamente la excepción, en lugar de modificar el diseño del código para satisfacer al analizador estático.

#### Lecciones Aprendidas

La incorporación de Ruff permitió establecer varias prácticas que se mantendrán durante el resto del proyecto:

* Analizar los resultados antes de corregirlos.
* Clasificar los hallazgos por tipo de problema.
* Preferir excepciones específicas antes de deshabilitar reglas de forma global.
* Adaptar la configuración de la herramienta a las necesidades del proyecto, en lugar de mofidificar el código únicamente para eliminar advertencias.
* Comprender cada regla antes de habilitarla o deshabilitarla.

#### Configuración

```toml
# Configuración general
[tool.ruff]
line-length = 200  # Verifica que el largo de la línea no sea mayor a 200 caracteres

# Configuración analizador estático 
[tool.ruff.lint]
select = ["E", "F"]  # Activa las reglas E (estilo) y F (Pyflakes)

[tool.ruff.lint.per-file-ignores]
"alembic/env.py" = ["E402", "F401"]  # En el archivo env.py ignora únicamente las reglas E402 y F401
```

---

### Black

**Estado:** ✅ Implementado

#### Objetivo

Mantener un estilo de código uniforme en todo el proyecto mediante un formateador automático, eliminando diferencias de formato entre desarrolladores y reduciendo el ruido durante las revisiones de código.

#### Comando

```bash
# Muestra los problemas de formato
black --check .

# Corrije los errores
black .
```

#### Decisiones adoptadas

* Configuración centralizada mediante `pyproject.toml`.
* Misma longitud máxima de línea utilizada por Ruff (`200` caracteres) para evitar conflictos entre herramientas.
* Uso de Python 3.12 como versión objetivo (`target-version = ["py312"]`).
* Aplicación del formato sobre todo el repositorio antes de continuar con el resto del pipeline de calidad.

#### Configuración

```toml
[tool.black]
line-length = 200
target-version = ["py312"]  # Indica que el proyecto se ejecuta sobre Python 3.12.x"
```

#### Observaciones

Black modifica únicamente el formato del código fuente. No detecta errores, no reorganiza imports y no realiza comprobaciones de tipos.

Los avisos mostrados posteriormente por Pylance pertenecen al análisis de tipos y serán tratados durante la integración de MyPy.

---

### isort

**Estado:** ✅ Implementado

#### Objetivo

Mantener una organización consistente de las importaciones del proyecto mediante una clasificación automática por categorías y orden alfabético.

#### Comando

```bash
# Muestra los problemas de formato
isort --check-only --diff .

# Corrije los errores
isort .
```

#### Decisiones adoptadas

* Configuración centralizada mediante `pyproject.toml`.
* Compatibilidad con Black mediante `profile = "black"`.
* Misma longitud máxima de línea utilizada por Ruff y Black (`200` caracteres).
* Aplicación sobre todo el repositorio para unificar el estilo de las importaciones.

#### Configuración

```toml
[tool.isort]
profile = "black"  # Organiza los imports de manera compatible con Black
line_length = 200
```

#### Observaciones

isort reorganiza únicamente las importaciones.

No modifica la lógica del programa, no detecta errores y no realiza comprobaciones de tipos.

Su función consiste exclusivamente en mantener una estructura consistente de los imports, facilitando la lectura y reduciendo diferencias de estilo entre desarrolladores.

---

### MyPy

**Estado:** ✅ Completado

#### Objetivo

Realizar análisis estático de tipos para detectar errores potenciales antes de la ejecución del programa.

#### Decisiones adoptadas

* Configuración centralizada mediante `pyproject.toml`.
* Integración gradual después de Ruff, Black e isort.
* Corrección de errores reales de tipado en lugar de ocultarlos mediante `type: ignore`.
* Migración de los modelos al Typed ORM de SQLAlchemy 2 para obtener compatibilidad completa con MyPy.

#### Configuración

```toml
[tool.mypy]
python_version = "3.12"

warn_return_any = true  # Avisa si una función devuelve Any
warn_unused_configs = true  # Evita errores en el archivo de configuración

disallow_untyped_defs = false  # Exige que todas las funciones estén tipadas
check_untyped_defs = true  # Analiza la función aunque no tenga anotaciones

ignore_missing_imports = true  # Evita analizar errores de terceros (imports)
```

#### Observaciones

La migración al Typed ORM permitió que MyPy infiriera correctamente los tipos de los modelos SQLAlchemy, eliminando los falsos positivos asociados al uso de `Column(...)` del estilo declarativo clásico.

---

### GitHub Actions

**Estado:** ✅ Implementado

#### Objetivo

Automatizar la validación del proyecto en un entorno limpio para garantizar que cada cambio pueda construirse, migrar la base de datos y ejecutar correctamente toda la suite de pruebas.

#### Pipeline

```text
Checkout
    │
    ▼
Setup Python
    │
    ▼
Install dependencies
    │
    ▼
PostgreSQL
    │
    ▼
Verify PostgreSQL
    │
    ▼
   Ruff
    │
    ▼
   Black
    │
    ▼
   isort
    │
    ▼
   MyPy
    │
    ▼
  Alembic
    │
    ▼
  Pytest
```

#### Decisiones adoptadas

* Construcción incremental del workflow, incorporando una etapa cada vez.
* Uso de PostgreSQL como servicio dentro de GitHub Actions.
* Ejecución automática de Alembic antes de la suite de pruebas.
* Uso de GitHub Secrets para almacenar información sensible.
* Externalización de la configuración mediante `.env`.
* Validación completa del proyecto antes de permitir su integración.

#### Beneficios

* Verificación automática del proyecto desde un entorno limpio.
* Detección temprana de errores de integración.
* Reproducibilidad del proceso de construcción.
* Pipeline alineado con prácticas habituales de integración continua.

---

## Comparativa de Herramientas del Pipeline

| Herramienta | Análisis estático | Formato | Organización de imports | Análisis de tipos |
|-------------|:-----------------:|:-------:|:-----------------------:|:-----------------:|
| Ruff | ✅ | ❌ | ❌* | ❌ |
| Black | ❌ | ✅ | ❌ | ❌ |
| isort | ❌ | ❌ | ✅ | ❌ |
| MyPy | ❌ | ❌ | ❌ | ✅ |

\* Ruff incorpora compatibilidad con la organización de imports mediante reglas inspiradas en isort. En este laboratorio se utiliza la herramienta **isort** de forma independiente con fines didácticos y para conocer el flujo tradicional utilizado en numerosos proyectos Python.

>**Nota:**  
>Actualmente las cuatro herramientas se ejecutan satisfactoriamente sobre todo el proyecto.

### Pipeline de Calidad

```text
Edición del código
        │
        ▼
Ruff
(Análisis estático)
        │
        ▼
Black
(Formato)
        │
        ▼
isort
(Organización de imports)
        │
        ▼
MyPy
(Análisis de tipos)
        │
        ▼
Pytest
(Pruebas)
```

Cada herramienta aborda una dimensión distinta de la calidad del código. Esta separación de responsabilidades permite construir un pipeline modular donde cada etapa complementa a las anteriores sin duplicar funciones.

---

## SQLAlchemy Typed ORM

Durante la integración de MyPy se migraron todos los modelos al estilo moderno de SQLAlchemy 2.

### Antes

```python
id = Column(Integer, primary_key=True)

name = Column(String)

role = relationship(...)
```

### Después

```python
id: Mapped[int] = mapped_column(primary_key=True)

name: Mapped[str] = mapped_column(String)

role: Mapped["RoleModel"] = relationship(...)
```

### Beneficios

* Compatibilidad completa con MyPy.
* Mejor autocompletado en el IDE.
* Inferencia correcta de tipos.
* Código alineado con las recomendaciones actuales de SQLAlchemy 2.

---

## Configuración mediante Variables de Entorno

Durante el Sprint 5 se decidió externalizar la configuración del proyecto utilizando variables de entorno.

La configuración local se almacena en un archivo `.env`, mientras que el repositorio incluye un archivo `.env.example` como plantilla para nuevos desarrolladores.

En GitHub Actions las variables sensibles se almacenan mediante **GitHub Secrets**, evitando incorporar credenciales dentro del repositorio.

Esta estrategia permite ejecutar el mismo código en distintos entornos (desarrollo, pruebas e integración continua) modificando únicamente la configuración y no la implementación.

---

## Buenas Prácticas

Durante el desarrollo se siguen las siguientes recomendaciones:

* Comprender el propósito de cada herramienta antes de integrarla.
* Evitar configuraciones copiadas sin criterio.
* Incorporar nuevas herramientas únicamente cuando aporten valor al proyecto.
* Mantener una configuración centralizada y fácilmente mantenible.
* Automatizar siempre que sea posible las tareas repetitivas.

---

## Evolución

Durante el Sprint 5 se incorporaron progresivamente las siguientes herramientas al pipeline de desarrollo:

* Ruff
* Black
* isort
* MyPy
* SQLAlchemy Typed ORM
* Configuración mediante variables de entorno (`.env`)
* GitHub Actions
* Integración automática con PostgreSQL
* Ejecución automática de Alembic
* Ejecución automática de Pytest

Las siguientes mejoras previstas para futuros sprints incluyen:

* Pre-commit Hooks.
* Reportes de cobertura.
* Badges de calidad.
* Matrices de versiones de Python.

---

## Conclusiones

El Sprint 5 representa un cambio de enfoque dentro del laboratorio.

Mientras los sprints anteriores estuvieron orientados a desarrollar funcionalidades e infraestructura de testing, este sprint se centra en profesionalizar el proceso de desarrollo mediante herramientas de análisis estático, automatización y calidad continua.

El objetivo final es disponer de un pipeline capaz de validar automáticamente la calidad del proyecto antes de su integración, siguiendo prácticas habituales en proyectos profesionales de desarrollo backend y QA Automation.
