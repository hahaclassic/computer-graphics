from PyQt6.QtCore import QRect, QLine, QPoint
from math import inf

# segment position
VERTICAL = -1
HORIZONTAL = 1
GENERAL = 0


def cohen_sutherland(rect: QRect, segment: QLine) -> tuple[QLine, bool]:
    fl, tan = get_segment_position(segment)
    p1, p2 = segment.p1(), segment.p2()

    bit_mask = 1
    window = create_window_arr(rect)
    for i in range(4):
        p1_code = get_position_code(rect, p1)
        p2_code = get_position_code(rect, p2)

        if p1_code & p2_code:
            return QLine(), False
        if not p1_code | p2_code:
            return QLine(p1, p2), True

        if p1_code & bit_mask == p2_code & bit_mask:
            bit_mask <<= 1
            continue
        if p1_code & bit_mask == 0:
            p1, p2 = p2, p1

        if fl == VERTICAL:
            p1.setY(window[i])
        else:
            if i < 2:
                p1.setY(int(tan * (window[i] - p1.x()) + p1.y()))
                p1.setX(window[i])
            else:
                p1.setX(int((1 / tan) * (window[i] - p1.y()) + p1.x()))
                p1.setY(window[i])

        bit_mask <<= 1

    return QLine(p1, p2), True


def get_segment_position(segment: QLine) -> tuple[int, float]:
    p1, p2 = segment.p1(), segment.p2()

    fl = GENERAL
    if segment.x1() == segment.x2():
        fl = VERTICAL
        tan = inf
    elif segment.y1() == segment.y2():
        fl = HORIZONTAL
        tan = 0.0
    else:
        tan = (p2.y() - p1.y()) / (p2.x() - p1.x())

    return fl, tan


# bit masks
LEFT = 1
RIGHT = 2
BOTTOM = 4
TOP = 8


def get_position_code(rect: QRect, point: QPoint) -> int:
    code = 0
    if point.x() < min(rect.left(), rect.right()):
        code |= LEFT
    if point.x() > max(rect.left(), rect.right()):
        code |= RIGHT
    if point.y() < min(rect.top(), rect.bottom()):
        code |= BOTTOM
    if point.y() > max(rect.top(), rect.bottom()):
        code |= TOP

    return code


def create_window_arr(rect: QRect) -> list[int]:
    x_min, x_max = rect.left(), rect.right()
    y_min, y_max = rect.bottom(), rect.top()
    if x_min > x_max:
        x_min, x_max = x_max, x_min
    if y_min > y_max:
        y_min, y_max = y_max, y_min

    return [x_min, x_max, y_min, y_max]
