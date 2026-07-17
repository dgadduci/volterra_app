# Volterra Stock — Reglas del proyecto

## Objetivo

Volterra Stock es un sistema local para administrar el stock de productos del comercio Volterra.

Este proyecto también tiene como objetivo aprender ingeniería de software asistida por IA mediante:

- Specification-Driven Development, SDD;
- diseño incremental;
- documentación de decisiones;
- revisión mediante subagentes;
- validación automática mediante tests.

## Stack autorizado

- Python 3.14
- PostgreSQL
- SQLAlchemy 2.x
- Alembic
- psycopg 3
- pytest
- pytest-cov
- Ruff
- mypy
- python-dotenv

No agregar nuevas dependencias sin explicar:

1. qué problema concreto resuelven;
2. por qué las herramientas actuales no alcanzan;
3. qué costo de mantenimiento introducen;
4. cuál sería la alternativa más simple.

## Herramientas de desarrollo

La aplicación de Volterra Stock se desarrolla exclusivamente en Python.

OpenCode y Gentle AI pueden instalar archivos auxiliares escritos en TypeScript o
scripts Bash dentro de sus directorios de configuración. Esos archivos pertenecen a
las herramientas de desarrollo y no forman parte de la aplicación.

No se debe implementar lógica de negocio, persistencia ni interfaces de Volterra Stock
en TypeScript, JavaScript o Bash.

## Principios de desarrollo

1. Especificar antes de implementar.
2. Diseñar antes de escribir código.
3. Mantener una relación clara entre especificaciones, diseño, implementación y tests.
4. Implementar solamente lo necesario para cumplir la especificación aprobada.
5. Mantener los cambios pequeños.
6. No anticipar funcionalidades futuras.
7. No mezclar una funcionalidad nueva con una refactorización amplia.
8. Registrar las decisiones arquitectónicas importantes.
9. No afirmar que algo funciona sin ejecutar las verificaciones correspondientes.
10. Detener la implementación cuando exista una ambigüedad relevante en la especificación.

## Flujo SDD obligatorio

Para cada funcionalidad o cambio relevante:

1. Definir el problema.
2. Identificar objetivos y alcance.
3. Identificar reglas de negocio.
4. Detectar ambigüedades.
5. Escribir criterios de aceptación verificables.
6. Aprobar la especificación.
7. Diseñar la solución mínima.
8. Identificar los archivos y componentes afectados.
9. Aprobar el diseño.
10. Implementar respetando la especificación y el diseño.
11. Escribir o actualizar los tests correspondientes.
12. Ejecutar los tests.
13. Ejecutar Ruff.
14. Ejecutar mypy.
15. Revisar el cambio con un subagente distinto del implementador.
16. Actualizar la documentación.
17. Realizar el commit.

## Especificaciones y OpenSpec

Cada funcionalidad debe contar con una especificación escrita antes de ser implementada.

Este proyecto utiliza OpenSpec, instalado y gestionado por Gentle AI, como sistema
principal para Specification-Driven Development.

La documentación se divide en:

- `docs/product/`: visión, glosario y reglas generales del dominio;
- `docs/architecture/`: arquitectura estable y decisiones técnicas;
- `openspec/specs/`: especificaciones vigentes del sistema;
- `openspec/changes/`: cambios propuestos o en desarrollo;
- `openspec/changes/archive/`: cambios terminados y archivados.

Para cada cambio funcional, Gentle AI podrá generar dentro de
`openspec/changes/<nombre-del-cambio>/`:

- propuesta;
- especificaciones incrementales;
- diseño;
- tareas;
- evidencia de verificación.

Las especificaciones deben incluir, cuando corresponda:

- problema que se intenta resolver;
- objetivo;
- alcance;
- comportamiento esperado;
- reglas de negocio;
- entradas;
- salidas;
- errores esperados;
- casos límite;
- criterios de aceptación;
- elementos expresamente fuera de alcance.

Una vez completado y aprobado un cambio, sus especificaciones relevantes deben
integrarse en `openspec/specs/` y el cambio debe archivarse.

No se deben mantener dos especificaciones contradictorias sobre la misma funcionalidad.

Cuando exista una contradicción, ambigüedad o regla de negocio importante sin definir,
la implementación debe detenerse hasta resolverla.

No se debe implementar una funcionalidad si:

- la especificación es contradictoria;
- existen reglas de negocio importantes sin definir;
- el alcance no está claro;
- los criterios de aceptación no pueden verificarse.

## Revisión automática con GGA

El archivo `.gga` configura Gentleman Guardian Angel para revisar los cambios
preparados antes de cada commit.

`AGENTS.md` continúa siendo la fuente principal de reglas del proyecto.

El archivo `.gga` solamente indica a GGA:

- qué proveedor utilizar;
- qué archivo contiene las reglas;
- cuánto tiempo esperar;
- qué archivos revisar.

Las claves de MiniMax y otros secretos deben configurarse mediante variables de
entorno y nunca guardarse dentro de `.gga` ni versionarse en Git.