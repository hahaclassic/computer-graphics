import pytest
import json
from src.interface import Interface
from PyQt6.QtCore import QPointF, QPoint
from PyQt6.QtGui import QPolygon

TEST_FILE = "./test_data/test.json"
RESULT_DIR = "./results/"
TEST_REPEATS = 3 
BUFFER = "./func_buf.txt"

@pytest.fixture
def interface(qtbot):
    interface = Interface()
    qtbot.addWidget(interface)
    return interface

def test(interface: Interface):

    with open(TEST_FILE, "r") as f:
        tests = json.load(f)

    report = open(BUFFER, "w")
    report.write(f"number of tests: {len(tests)}\n")

    for idx, test in enumerate(tests):
        
        elapsed_time = 0.0

        for _ in range(TEST_REPEATS):
            interface.clear()
            elapsed_time += run_test(interface, test)

        test_time = (elapsed_time / TEST_REPEATS)
        report.write(f"< test: {idx + 1}, time: {test_time:.4f} >\n")

        path = RESULT_DIR + "test" + str(idx + 1)

        with open(path + "_description.txt", "w") as descrp_f:
            descrp_f.write(test["description"])

        image = interface.grab()

        image.save(path + "_image_.png")

    report.close()
    

def run_test(interface: Interface, test) -> float:
    interface.shapes = parse_shapes_data(test["shapes"])
    interface.clipper = parse_cutter_data(test["cutter"])
    interface.update_scene()
    interface.is_clipper_closed = True

    interface.cut()

    label_string = interface.time_label.text()
    elapsed_time = float(label_string.split()[0])

    return elapsed_time

def parse_shapes_data(json_shapes) -> list[QPolygon]:
    shapes = []

    for json_shape in json_shapes:
        shape = QPolygon()
        for json_point in json_shape:
            point = parse_point(json_point)
            shape.append(point)
        shapes.append(shape)

    return shapes


def parse_cutter_data(json_cutter) -> QPolygon:
    cutter = QPolygon()

    for json_point in json_cutter:
        point = parse_point(json_point)
        cutter.append(point)

    return cutter
        

def parse_point(json_point) -> QPoint:
    x, y = float(json_point["x"]), float(json_point["y"])
    return QPointF(x, y).toPoint()
