import pytest
from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QPolygon
import src.cut_shapes as cut


@pytest.fixture
def convex_polygon() -> QPolygon:
    return QPolygon([
        QPoint(0, 0),
        QPoint(100, 0),
        QPoint(0, 100)
    ])


@pytest.fixture
def nonconvex_polygon() -> QPolygon:
    return QPolygon([
        QPoint(0, 0),
        QPoint(200, 0),
        QPoint(100, 100),
        QPoint(200, 200),
        QPoint(0, 200)
    ])


@pytest.fixture
def degenerate_polygon() -> QPolygon:
    return QPolygon([
        QPoint(0, 0),
        QPoint(100, 100),
        QPoint(200, 200)
    ])


def test_is_polygon_convex_with_convex(convex_polygon) -> None:
    ok = cut.is_polygon_convex(convex_polygon)
    assert ok
   

def test_is_polygon_convex_with_nonconvex(nonconvex_polygon) -> None:
    ok = cut.is_polygon_convex(nonconvex_polygon)
    assert not ok


def test_is_polygon_convex_with_degenerate(degenerate_polygon) -> None:
    ok = cut.is_polygon_convex(degenerate_polygon)
    assert not ok
