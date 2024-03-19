import pytest
from src.circle import Circle, QPointF

@pytest.fixture
def valid_circle1():
    return Circle(QPointF(1, 0), QPointF(0, 1), QPointF(0, -1))

@pytest.fixture
def valid_circle2():
    return Circle(QPointF(20, 20), QPointF(30, 30), QPointF(36, 12))

@pytest.fixture
def valid_circle3():
    return Circle(
        QPointF(23.5, 40),
        QPointF(-15.109321980635, 57.998844109706),
        QPointF(-18.0563608879779, 24.9594603992044)
    )

@pytest.fixture
def invalid_circle1():
    return Circle(QPointF(1, 1), QPointF(20, 20), QPointF(30, 30))

@pytest.fixture
def invalid_circle2():
    return Circle(QPointF(1, 1), QPointF(1, 1), QPointF(1, 1))

def test_is_valid(valid_circle1, valid_circle2, valid_circle3, invalid_circle1, invalid_circle2):
    assert valid_circle1.is_valid() == True
    assert valid_circle2.is_valid() == True
    assert valid_circle3.is_valid() == True

    assert invalid_circle1.is_valid() == False
    assert invalid_circle2.is_valid() == False

def test_center(valid_circle1, valid_circle2, valid_circle3, invalid_circle1, invalid_circle2):
    assert valid_circle1.center() == QPointF(0, 0)
    assert valid_circle2.center() == QPointF(30, 20)

    assert invalid_circle1.center() == QPointF(0, 0)
    assert invalid_circle2.center() == QPointF(0, 0)

def test_radius(valid_circle1, valid_circle2, valid_circle3, invalid_circle1, invalid_circle2):
    assert pytest.approx(valid_circle1.radius(), 0.001) == 1.0
    assert pytest.approx(valid_circle2.radius(), 0.001) == 10.0
    assert pytest.approx(valid_circle3.radius(), 0.001) == 23.5

    assert pytest.approx(invalid_circle1.radius(), 0.001) == 0.0
    assert pytest.approx(invalid_circle2.radius(), 0.001) == 0.0

def test_centers_distance(valid_circle1, valid_circle2, valid_circle3):
    assert pytest.approx(valid_circle1.centers_distance(valid_circle2), 0.001) == 36.0555
    assert pytest.approx(valid_circle3.centers_distance(valid_circle1), 0.001) == 40.0
    assert pytest.approx(valid_circle2.centers_distance(valid_circle3), 0.001) == 36.0555
