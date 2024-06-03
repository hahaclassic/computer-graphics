import pytest
from PyQt6.QtCore import QPointF, QPoint
import src.horizon as horizon


class MockView:
    def __init__(self, w: int, h: int) -> None:
        self.w = w
        self.h = h
    
    def width(self) -> int:
        return self.w
    
    def height(self) -> int:
        return self.h

    def mapFromScene(self, point: QPointF) -> QPoint:
        return point.toPoint()

@pytest.fixture
def visible_top_point() -> QPointF:
    return QPointF(40, 40)


@pytest.fixture
def visible_bottom_point() -> QPointF:
    return QPointF(10, 10)


@pytest.fixture
def invisible_point() -> QPointF:
    return QPointF(20, 20)


@pytest.fixture
def outside_view_point() -> QPointF:
    return QPointF(120, 120)


@pytest.fixture
def custom_horizon() -> horizon.Horizon:
    h = horizon.Horizon(MockView(100, 100))
    h.bottom = [15] * 100
    h.top = [30] * 100
    return h


def test_visible_with_visible_top_point(custom_horizon, visible_top_point) -> None:
    v = custom_horizon.visible(visible_top_point)
    assert horizon.TOP == v
   
def test_visible_with_visible_bottom_point(custom_horizon, visible_bottom_point) -> None:
    v = custom_horizon.visible(visible_bottom_point)
    assert horizon.BOTTOM == v

def test_visible_with_invisible_point(custom_horizon, invisible_point) -> None:
    v = custom_horizon.visible(invisible_point)
    assert horizon.INVISIBLE == v

def test_visible_with_outsize_view_point(custom_horizon, outside_view_point) -> None:
    v = custom_horizon.visible(outside_view_point)
    assert v is None
    