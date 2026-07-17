"""Unit tests for the ``Producto`` domain entity.

Pure in-process tests: no DB, no network, no clock dependencies beyond
stdlib ``datetime``/``uuid``. Covers every invariant declared in the
spec's ``alta-productos`` slice and in design D1.
"""

from __future__ import annotations

import dataclasses
from datetime import UTC, datetime, timedelta
from uuid import UUID

import pytest

from volterra_stock.domain import Producto, ProductoYaExiste, ValidationError


class TestProductoInvariants:
    def test_constructor_ok_returns_instance(self) -> None:
        producto = Producto(codigo_interno="ABC-001", nombre="Aceite")
        assert isinstance(producto, Producto)
        assert producto.codigo_interno == "ABC-001"
        assert producto.nombre == "Aceite"

    def test_codigo_interno_blank_raises_validation_error(self) -> None:
        with pytest.raises(ValidationError):
            Producto(codigo_interno="   ", nombre="Aceite")

    def test_codigo_interno_empty_string_raises_validation_error(self) -> None:
        with pytest.raises(ValidationError):
            Producto(codigo_interno="", nombre="Aceite")

    def test_nombre_blank_raises_validation_error(self) -> None:
        with pytest.raises(ValidationError):
            Producto(codigo_interno="ABC-001", nombre="   ")

    def test_nombre_empty_string_raises_validation_error(self) -> None:
        with pytest.raises(ValidationError):
            Producto(codigo_interno="ABC-001", nombre="")

    def test_codigo_interno_over_64_chars_raises_validation_error(self) -> None:
        codigo_largo = "A" * 65
        with pytest.raises(ValidationError):
            Producto(codigo_interno=codigo_largo, nombre="Aceite")

    def test_codigo_interno_exactly_64_chars_is_accepted(self) -> None:
        codigo_max = "A" * 64
        producto = Producto(codigo_interno=codigo_max, nombre="Aceite")
        assert producto.codigo_interno == codigo_max

    def test_nombre_over_200_chars_raises_validation_error(self) -> None:
        nombre_largo = "A" * 201
        with pytest.raises(ValidationError):
            Producto(codigo_interno="ABC-001", nombre=nombre_largo)

    def test_nombre_exactly_200_chars_is_accepted(self) -> None:
        nombre_max = "A" * 200
        producto = Producto(codigo_interno="ABC-001", nombre=nombre_max)
        assert producto.nombre == nombre_max


class TestProductoNormalization:
    def test_codigo_interno_whitespace_is_trimmed_and_uppercased(self) -> None:
        producto = Producto(codigo_interno="  abc-001  ", nombre="Aceite")
        assert producto.codigo_interno == "ABC-001"

    def test_codigo_interno_mixed_case_is_uppercased(self) -> None:
        producto = Producto(codigo_interno="aBc-007", nombre="Aceite")
        assert producto.codigo_interno == "ABC-007"

    def test_nombre_whitespace_is_trimmed_but_case_preserved(self) -> None:
        producto = Producto(codigo_interno="ABC-001", nombre="  Aceite de Oliva  ")
        assert producto.nombre == "Aceite de Oliva"

    def test_length_caps_are_evaluated_after_normalization(self) -> None:
        # 66 raw chars with surrounding whitespace should still be rejected
        # because the post-strip length is 66, exceeding 64.
        codigo_largo_normalizado = "A" * 66
        with pytest.raises(ValidationError):
            Producto(codigo_interno=f"  {codigo_largo_normalizado}  ", nombre="Aceite")


class TestProductoDefaults:
    def test_activo_defaults_to_true(self) -> None:
        producto = Producto(codigo_interno="ABC-001", nombre="Aceite")
        assert producto.activo is True

    def test_id_is_a_uuid(self) -> None:
        producto = Producto(codigo_interno="ABC-001", nombre="Aceite")
        assert isinstance(producto.id, UUID)

    def test_id_is_unique_per_instance(self) -> None:
        a = Producto(codigo_interno="ABC-001", nombre="Aceite")
        b = Producto(codigo_interno="ABC-002", nombre="Otro")
        assert a.id != b.id

    def test_creado_en_is_a_datetime_with_utc(self) -> None:
        producto = Producto(codigo_interno="ABC-001", nombre="Aceite")
        assert isinstance(producto.creado_en, datetime)
        assert producto.creado_en.tzinfo is not None
        assert producto.creado_en.utcoffset() == timedelta(0)
        assert producto.creado_en.tzinfo == UTC

    def test_actualizado_en_equals_creado_en_at_construction(self) -> None:
        producto = Producto(codigo_interno="ABC-001", nombre="Aceite")
        assert producto.actualizado_en == producto.creado_en


class TestProductoFrozen:
    def test_frozen_dataclass_rejects_attribute_assignment(self) -> None:
        producto = Producto(codigo_interno="ABC-001", nombre="Aceite")
        with pytest.raises(dataclasses.FrozenInstanceError):
            producto.codigo_interno = "XYZ-999"  # type: ignore[misc]

    def test_frozen_dataclass_rejects_activo_assignment(self) -> None:
        producto = Producto(codigo_interno="ABC-001", nombre="Aceite")
        with pytest.raises(dataclasses.FrozenInstanceError):
            producto.activo = False  # type: ignore[misc]

    def test_frozen_dataclass_rejects_id_assignment(self) -> None:
        producto = Producto(codigo_interno="ABC-001", nombre="Aceite")
        with pytest.raises(dataclasses.FrozenInstanceError):
            producto.id = "not-a-uuid"  # type: ignore[misc]

    def test_slots_are_declared(self) -> None:
        # @dataclass(slots=True) installs __slots__; the canonical signal
        # is that the instance no longer carries a per-instance __dict__.
        producto = Producto(codigo_interno="ABC-001", nombre="Aceite")
        assert "__dict__" not in dir(producto)
        cls = type(producto)
        assert hasattr(cls, "__slots__")
        assert isinstance(cls.__slots__, str) or all(isinstance(s, str) for s in cls.__slots__)


class TestProductoScope:
    def test_no_precio_attribute(self) -> None:
        producto = Producto(codigo_interno="ABC-001", nombre="Aceite")
        assert not hasattr(producto, "precio")

    def test_no_stock_attribute(self) -> None:
        producto = Producto(codigo_interno="ABC-001", nombre="Aceite")
        assert not hasattr(producto, "stock")

    def test_no_cantidad_attribute(self) -> None:
        producto = Producto(codigo_interno="ABC-001", nombre="Aceite")
        assert not hasattr(producto, "cantidad")


class TestProductoYaExiste:
    def test_carries_codigo_interno(self) -> None:
        exc = ProductoYaExiste("ABC-001")
        assert exc.codigo_interno == "ABC-001"

    def test_message_mentions_codigo_interno(self) -> None:
        exc = ProductoYaExiste("ABC-001")
        assert "ABC-001" in str(exc)

    def test_is_an_exception(self) -> None:
        assert issubclass(ProductoYaExiste, Exception)


class TestValidationError:
    def test_is_a_value_error(self) -> None:
        assert issubclass(ValidationError, ValueError)
