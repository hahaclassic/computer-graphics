import pytest
from PyQt6.QtCore import QPoint, QLine, QRect
import src.cut_segment as cut

EPS = 1e-04

@pytest.fixture
def general_segment() -> QLine:
    return QLine(-5, 0, 10, 15)


@pytest.fixture
def vertical_segment() -> QLine:
    return QLine(5, 5, 5, 15)


@pytest.fixture
def horizontal_segment() -> QLine:
    return QLine(-5, 5, 15, 5)


@pytest.fixture
def rectangle1() -> QRect:
    p1 = QPoint(0, 10)
    p2 = QPoint(10, 0)
    return QRect(p1, p2)


@pytest.fixture
def rectangle2() -> QRect:
    p1 = QPoint(100, 110)
    p2 = QPoint(110, 100)
    return QRect(p1, p2)


def equal(seg1: QLine, seg2: QLine) -> bool:
    return seg1.p1() == seg2.p1() and seg1.p2() == seg2.p2() \
        or seg1.p1() == seg2.p2() and seg1.p2() == seg2.p1() 


def test_partially_visible_general_segment(rectangle1, general_segment) -> None:
    cutted, ok = cut.cohen_sutherland(rectangle1, general_segment)
    print(cutted, ok)

    assert ok
    assert equal(cutted, QLine(0, 5, 5, 10))


def test_partially_visible_vertical_segment(rectangle1, vertical_segment) -> None:
    cutted, ok = cut.cohen_sutherland(rectangle1, vertical_segment)
    print(cutted, ok)
    assert ok
    assert equal(cutted, QLine(5, 5, 5, 10))


def test_partially_visible_horizontal_segment(rectangle1, horizontal_segment) -> None:
    cutted, ok = cut.cohen_sutherland(rectangle1, horizontal_segment)
    print(cutted, ok)
    assert ok
    assert equal(cutted, QLine(0, 5, 10, 5))


def test_invisible_general_segment(rectangle2, general_segment) -> None:
    cutted, ok = cut.cohen_sutherland(rectangle2, general_segment)
    assert not ok
    assert cutted == QLine()
