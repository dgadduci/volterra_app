# Arquitectura inicial

## Objetivo

Mantener una arquitectura simple, comprensible y suficiente para el alcance actual.

## Capas iniciales

### Domain

Contiene conceptos y reglas puras del negocio.

No debe depender de SQLAlchemy, PostgreSQL, Alembic ni interfaces externas.

### Application

Contiene los casos de uso y coordina el dominio con los puertos de persistencia.

### Infrastructure

Contiene las implementaciones técnicas:

- SQLAlchemy;
- PostgreSQL;
- Alembic;
- repositorios;
- configuración de base de datos.

### Interfaces

Contiene los puntos de entrada al sistema.

La primera interfaz podrá ser una CLI simple.

## Estructura prevista

```text
src/volterra_stock/
├── domain/
├── application/
├── infrastructure/
└── interfaces/