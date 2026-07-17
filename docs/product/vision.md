# Visión del producto

## Nombre

Volterra Stock

## Propósito

Volterra Stock es un sistema local para administrar las existencias de productos del comercio Volterra.

El sistema debe permitir conocer qué productos existen, cuántas unidades hay disponibles y cómo se modificó el stock a lo largo del tiempo.

## Problema que resuelve

Actualmente el control de stock puede depender de registros manuales, información dispersa o cálculos que no permiten reconstruir con claridad los movimientos realizados.

El sistema busca centralizar esa información y reducir errores en el control de existencias.

## Usuarios iniciales

El usuario inicial será el responsable del comercio Volterra.

En esta primera etapa no se implementarán múltiples usuarios, roles ni permisos.

## Objetivos iniciales

- registrar productos;
- registrar entradas de stock;
- registrar salidas de stock;
- registrar ajustes;
- consultar la existencia de un producto;
- consultar el historial de movimientos;
- conservar trazabilidad de los cambios.

## Fuera de alcance inicial

- ventas;
- facturación;
- proveedores;
- compras;
- precios;
- caja;
- contabilidad;
- sucursales múltiples;
- usuarios y permisos;
- aplicación web;
- aplicación móvil;
- integración con Mercado Libre;
- integración con sistemas externos.

## Criterios generales

- el sistema debe ser simple;
- el comportamiento debe estar especificado antes de implementarse;
- las reglas de negocio no deben depender de la interfaz;
- la persistencia debe utilizar PostgreSQL;
- los cambios en el esquema deben administrarse mediante Alembic;
- cada movimiento de stock debe ser trazable.