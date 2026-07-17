"""Domain layer for Volterra Stock.

Re-exports the public domain surface so callers can write
``from volterra_stock.domain import Producto`` instead of reaching into
``volterra_stock.domain.producto``.
"""

from volterra_stock.domain.producto import Producto, ProductoYaExiste, ValidationError

__all__ = ["Producto", "ProductoYaExiste", "ValidationError"]
