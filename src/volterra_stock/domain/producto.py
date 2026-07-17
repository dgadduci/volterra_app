"""Pure domain entities, invariants, and exceptions for Volterra Stock.

This module is deliberately free of infrastructure concerns. No SQLAlchemy,
no Alembic, no I/O. Anything that needs persistence lives in
``volterra_stock.infrastructure.persistence``; this layer only describes
the business shape and the rules the rules the rest of the system must
respect.

The slice ``alta-productos`` adds ``Producto`` and two exceptions:
``ValidationError`` for invariant violations and ``ProductoYaExiste`` for
the duplicate-codigo case raised by application/infra layers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

CODIGO_INTERNO_MAX_LEN = 64
NOMBRE_MAX_LEN = 200


class ValidationError(ValueError):
    """Raised when a domain invariant is violated (blank, too long, ...)."""


class ProductoYaExiste(Exception):
    """Raised when a product cannot be persisted because its codigo is taken.

    Carries the offending ``codigo_interno`` so callers (CLI, application
    handlers) can surface a precise message to the operator without
    re-parsing the original exception chain.
    """

    def __init__(self, codigo_interno: str) -> None:
        super().__init__(f"Ya existe un producto con codigo_interno={codigo_interno!r}")
        self.codigo_interno = codigo_interno


@dataclass(frozen=True, slots=True)
class Producto:
    """A registered product in Volterra Stock.

    Required fields are declared first so the dataclass accepts the
    default factories used for ``id`` and ``creado_en``. ``actualizado_en``
    is derived from ``creado_en`` and is therefore not an ``__init__``
    parameter; it is assigned in ``__post_init__`` via
    ``object.__setattr__`` because ``frozen=True`` disables normal
    attribute assignment.
    """

    codigo_interno: str
    nombre: str
    id: UUID = field(default_factory=uuid4)
    activo: bool = True
    creado_en: datetime = field(default_factory=lambda: datetime.now(UTC))
    actualizado_en: datetime = field(init=False)

    def __post_init__(self) -> None:
        codigo_normalizado = self.codigo_interno.strip().upper()
        if not codigo_normalizado:
            raise ValidationError("codigo_interno no puede estar vacio")
        if len(codigo_normalizado) > CODIGO_INTERNO_MAX_LEN:
            raise ValidationError(
                f"codigo_interno no puede superar {CODIGO_INTERNO_MAX_LEN} caracteres"
            )

        nombre_normalizado = self.nombre.strip()
        if not nombre_normalizado:
            raise ValidationError("nombre no puede estar vacio")
        if len(nombre_normalizado) > NOMBRE_MAX_LEN:
            raise ValidationError(f"nombre no puede superar {NOMBRE_MAX_LEN} caracteres")

        object.__setattr__(self, "codigo_interno", codigo_normalizado)
        object.__setattr__(self, "nombre", nombre_normalizado)
        object.__setattr__(self, "actualizado_en", self.creado_en)
