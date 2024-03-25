import math
import pytest
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QVector2D
import src.geometry as geo

EPS = 1e-04

@pytest.fixture
def point1():
    return QPointF(6.0, 0.0)

@pytest.fixture
def point2():
    return QPointF(2.5, 2.5)

@pytest.fixture
def vector1():
    return QVector2D(6, 6)

@pytest.fixture
def vector2():
    return QVector2D(0, 6)

# the overloaded __eq__ for QPointF in this case will 
# not work because of the calculation error.
def are_points_equal(point1: QPointF, point2: QPointF):
    x = math.fabs(point1.x() - point2.x())
    y = math.fabs(point1.y() - point2.y())
    assert x < EPS
    assert y < EPS


def test_move_point(point1, point2):
    shifted_point1 = geo.move_point(point1, 10.5, 10.5)
    are_points_equal(shifted_point1, QPointF(16.5, 10.5))

    shifted_point2 = geo.move_point(point2, 2.5, 0)
    are_points_equal(shifted_point2, QPointF(5, 2.5))


def test_rotate_point(point1, point2):
    rotated_point1 = geo.rotate_point(point1, QPointF(0,0), math.pi / 2)
    are_points_equal(rotated_point1, QPointF(0.0, 6.0))

    rotated_point2 = geo.rotate_point(point2, QPointF(0,0), math.pi)
    are_points_equal(rotated_point2, QPointF(-2.5, -2.5))


def test_scale_point(point1, point2):
    scaled_point1 = geo.scale_point(point1, QPointF(0,0), 2)
    are_points_equal(scaled_point1, QPointF(12.0, 0.0))
   
    scaled_point2 = geo.scale_point(point2, QPointF(0,0), 0.5)
    are_points_equal(scaled_point2, QPointF(1.25, 1.25))


def test_rotate_vector(vector1):
    rotated_vec = geo.rotate_vector(vector1, math.pi)
    are_points_equal(rotated_vec.toPointF(), QPointF(-6, -6))


def test_angle_between_vectors(vector1, vector2):
    angle = geo.angle_between_vectors(vector1, vector2)

    assert pytest.approx(angle, EPS) == math.pi / 4


def test_reflect_vector(vector1, vector2):
    reflected_vec2 = geo.reflect_vector(vector2, vector1) 
    are_points_equal(reflected_vec2.toPointF(), QPointF(6, 0))

    reflected_vec1 = geo.reflect_vector(vector1, vector2)
    are_points_equal(reflected_vec1.toPointF(), QPointF(-6, 6))
