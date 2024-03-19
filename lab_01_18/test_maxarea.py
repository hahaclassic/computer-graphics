import math
import pytest
from src.circle import QPointF
from src.maxarea import find_max_area

@pytest.fixture
def valid_sets():
    set1 = [QPointF(1, 0), QPointF(0, 1), QPointF(0, -1)]
    set2 = [QPointF(5, 0), QPointF(4, 1), QPointF(4, -1)]
    return set1, set2

def test_area_equal_radii(valid_sets):
    set1, set2 = valid_sets
    area, _, _ = find_max_area(set1, set2)
    assert math.isclose(area, 4.0)

def test_area_circles_arranged_horizontally(valid_sets):
    set1, set2 = valid_sets
    set2 = [QPointF(6, 0), QPointF(4, 2), QPointF(4, -2)]
    area, _, _ = find_max_area(set1, set2)
    assert math.isclose(area, 6.18465, rel_tol=1e-3)

def test_area_circles_arranged_vertically(valid_sets):
    set1, set2 = valid_sets
    set2 = [QPointF(0, 6), QPointF(2, 4), QPointF(-2, 4)]
    area, _, _ = find_max_area(set1, set2)
    assert math.isclose(area, 6.18465, rel_tol=1e-3)

def test_area_general_case(valid_sets):
    set1, set2 = valid_sets
    set2 = [QPointF(4, 1), QPointF(4, 5), QPointF(6, 3)]
    area, _, _ = find_max_area(set1, set2)
    assert math.isclose(area, 7.6485, rel_tol=1e-3)

def test_search():
    set1 = [
        QPointF(1, 0), QPointF(0, 1), QPointF(0, -1),
        QPointF(2, 0), QPointF(0, 2), QPointF(0, -2)
    ]
    set2 = [
        QPointF(6, 0), QPointF(4, 2), QPointF(4, -2),
        QPointF(0, 6), QPointF(2, 4), QPointF(-2, 4),
        QPointF(4, 1), QPointF(4, 5), QPointF(6, 3)
    ]
    area, circle1, circle2 = find_max_area(set1, set2)

    assert math.isclose(area, 103.59924, rel_tol=1e-3)

    assert circle1.center() == QPointF(-1.5, 0.0)
    assert math.isclose(circle1.radius(), 2.5, rel_tol=1e-3)

    assert circle2.center() == QPointF(9.5, 9.5)
    assert math.isclose(circle2.radius(), 10.12422, rel_tol=1e-3)

def test_search_degenerate_circles():
    set1 = [QPointF(1, 1), QPointF(20, 20), QPointF(30, 30)]
    set2 = [QPointF(1, 1), QPointF(1, 1), QPointF(1, 1)]

    area, circle1, circle2 = find_max_area(set1, set2)

    assert math.isclose(area, -math.inf)
    assert circle1 is None
    assert circle2 is None

def test_search_when_one_circle_in_another():
    set1 = [QPointF(1, 0), QPointF(0, 1), QPointF(0, -1)]
    set2 = [QPointF(2, 0), QPointF(0, 2), QPointF(0,-2)]

    area, circle1, circle2 = find_max_area(set1, set2)

    assert math.isclose(area, -math.inf)
    assert circle1 is None
    assert circle2 is None
