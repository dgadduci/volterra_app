# Reglas generales de negocio

Este documento contiene reglas generales del dominio.

Las reglas específicas de cada funcionalidad deben documentarse también en su correspondiente especificación.

## Productos

1. Cada producto debe tener un código interno.
2. El código interno debe ser único.
3. Cada producto debe tener un nombre.
4. Un producto nuevo se crea inicialmente como activo.
5. Un producto desactivado conserva su historial.
6. La eliminación física de productos no forma parte del alcance inicial.

## Movimientos de stock

1. Todo cambio de existencia debe registrarse como un movimiento.
2. Un movimiento debe identificar el producto afectado.
3. Un movimiento debe indicar su tipo.
4. Un movimiento debe indicar la cantidad involucrada.
5. Un movimiento debe tener fecha y hora.
6. Un ajuste debe incluir una justificación.
7. Los movimientos registrados no deben modificarse silenciosamente.
8. La anulación o corrección de movimientos todavía debe especificarse.

## Existencias

1. La existencia debe poder determinarse a partir de información persistida.
2. El sistema no debe perder el historial de modificaciones.
3. Todavía no está definido si se permitirá stock negativo.
4. Todavía no está definido si una salida superior a la existencia debe rechazarse.
5. Estas decisiones deberán resolverse antes de implementar salidas de stock.