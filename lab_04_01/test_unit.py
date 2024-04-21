import pytest
from PyQt6.QtCore import QPointF, QPoint
import src.draw as draw

EPS = 1e-04

@pytest.fixture
def circle():
    return draw.Circle(QPointF(0, 0), 3)

@pytest.fixture
def ellipse():
    return draw.Ellipse(QPointF(0, 0), 4, 2)

@pytest.fixture
def circle_plotter():
    return draw.CirclePlotter(None)

@pytest.fixture
def ellipse_plotter():
    return draw.EllipsePlotter(None)


def test_circle_canonical(circle_plotter, circle):
    expected_points = [
        QPoint(0, 3), QPoint(0, 3), QPoint(0, -3), QPoint(0, -3),
        QPoint(3, 0), QPoint(-3, 0), QPoint(3, 0), QPoint(-3, 0),
        QPoint(1, 3), QPoint(-1, 3), QPoint(1, -3), QPoint(-1, -3),
        QPoint(3, 1), QPoint(-3, 1), QPoint(3, -1), QPoint(-3, -1),
        QPoint(2, 2), QPoint(-2, 2), QPoint(2, -2), QPoint(-2, -2),
        QPoint(2, 2), QPoint(-2, 2), QPoint(2, -2), QPoint(-2, -2)
    ] 
    points = circle_plotter.canonical(circle)
    
    assert points == expected_points

def test_ellipse_canonical(ellipse_plotter, ellipse):
    expected_points = [
       QPoint(0, 2), QPoint(0, 2), QPoint(0, -2), QPoint(0, -2), 
       QPoint(1, 2), QPoint(-1, 2), QPoint(1, -2), QPoint(-1, -2), 
       QPoint(2, 2), QPoint(-2, 2), QPoint(2, -2), QPoint(-2, -2), 
       QPoint(3, 1), QPoint(-3, 1), QPoint(3, -1), QPoint(-3, -1), 
       QPoint(4, 0), QPoint(-4, 0), QPoint(4, 0), QPoint(-4, 0)
    ] 
    points = ellipse_plotter.canonical(ellipse)
    
    assert points == expected_points

def test_circle_bresenham(circle_plotter, circle):
    expected_points = [
        QPoint(0, 3), QPoint(0, 3), QPoint(0, -3), QPoint(0, -3),
        QPoint(3, 0), QPoint(-3, 0), QPoint(3, 0), QPoint(-3, 0), 
        QPoint(1, 3), QPoint(-1, 3), QPoint(1, -3), QPoint(-1, -3), 
        QPoint(3, 1), QPoint(-3, 1), QPoint(3, -1), QPoint(-3, -1), 
        QPoint(2, 2), QPoint(-2, 2), QPoint(2, -2), QPoint(-2, -2), 
        QPoint(2, 2), QPoint(-2, 2), QPoint(2, -2), QPoint(-2, -2)
    ] 
    points = circle_plotter.bresenham(circle)
    
    assert points == expected_points

def test_ellipse_bresenham(ellipse_plotter, ellipse):
    expected_points = [
        QPoint(0, 2), QPoint(0, 2), QPoint(0, -2), QPoint(0, -2), 
        QPoint(1, 2), QPoint(-1, 2), QPoint(1, -2), QPoint(-1, -2), 
        QPoint(2, 2), QPoint(-2, 2), QPoint(2, -2), QPoint(-2, -2), 
        QPoint(3, 2), QPoint(-3, 2), QPoint(3, -2), QPoint(-3, -2), 
        QPoint(4, 1), QPoint(-4, 1), QPoint(4, -1), QPoint(-4, -1), 
        QPoint(5, 0), QPoint(-5, 0), QPoint(5, 0), QPoint(-5, 0)
    ] 
    points = ellipse_plotter.bresenham(ellipse)
    
    assert points == expected_points

