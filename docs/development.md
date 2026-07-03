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
Ruff (Lint)
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
   Pytest
      │
      ▼
GitHub Actions
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

```python
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

#### Configuración Actual

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

**Estado:** Pendiente

Se incorporará como formateador oficial del proyecto

---

### isort

**Estado:** Pendiente

Se utilizará para mantener un orden consistente de las importaciones

---

### MyPy

**Estado:** Pendiente

Permitirá incorporar comprobación estática de tipos al proyecto.

---

### GitHub Actions

**Estado:** Pendiente

Automatizará la ejecución del pipeline de calidad en cada Push y Pull Request.

---

## Pipeline de Calidad

Una vez completado el Sprint 5, el pipeline verificará automáticamente:

* Análisis estático.
* Formato del código.
* Organización de importaciones.
* Comprobación de tipos.
* Ejecución de la suite de pruebas.
* Cobertura de código.

El objetivo es impedir cambios que incumplan los estándates de calidad sean integrados al proyecto.

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

Es documento evolucionará conforme avance el Sprint 5.

Las próximas incorporaciones previstas incluyen:

* Configuración de Ruff.
* Integración de Black.
* Configuración de isort.
* Integración de MyPy.
* GitHub Actions.
* Pre-commit Hooks.
* Publicación de reportes.
* Badges de calidad.

---

## Conclusiones

El Sprint 5 representa un cambio de enfoque dentro del laboratorio.

Mientras los sprints anteriores estuvieron orientados a desarrollar funcionalidades e infraestructura de testing, este sprint se centra en profesionalizar el proceso de desarrollo mediante herramientas de análisis estático, automatización y calidad continua.

El objetivo final es disponer de un pipeline capaz de validar automáticamente la calidad del proyecto antes de su integración, siguiendo prácticas habituales en proyectos profesionales de desarrollo backend y QA Automation.
