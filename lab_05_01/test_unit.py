import pytest
from PyQt6.QtCore import QPoint, QLine
from PyQt6.QtGui import QPolygon
import src.draw as draw

EPS = 1e-04

@pytest.fixture
def figures() -> list[QPolygon]:
    figures = [QPolygon(), QPolygon()]
    figures[0].append(QPoint(600, 600))
    figures[0].append(QPoint(700, 800))
    figures[0].append(QPoint(800, 600))
    figures[1].append(QPoint(320, 320))
    figures[1].append(QPoint(400, 520))
    figures[1].append(QPoint(480, 320))
    figures[1].append(QPoint(280, 440))
    figures[1].append(QPoint(520, 440))
    return figures

def test_find_extremes(figures):
    y_min, y_max = draw.find_extremes(figures)

    assert y_min == 320
    assert y_max == 800

def test_create_edges_list(figures):
    edges = draw.create_edges_list(figures)

    expected = [
        QLine(QPoint(600, 600), QPoint(700, 800)),
        QLine(QPoint(700, 800), QPoint(800, 600)),
        QLine(QPoint(800, 600), QPoint(600, 600)),
        QLine(QPoint(320, 320), QPoint(400, 520)),
        QLine(QPoint(400, 520), QPoint(480, 320)),
        QLine(QPoint(480, 320), QPoint(280, 440)),
        QLine(QPoint(280, 440), QPoint(520, 440)),
        QLine(QPoint(520, 440), QPoint(320, 320)),
    ]
    assert edges == expected
