import pytest
import json
from src.interface import Interface
from PyQt6.QtCore import QPoint
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QTabWidget

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

        image.save(path + "_image.png")

    report.close()
    

def run_test(interface: Interface, test) -> float:

    interface.update_seed_point(parse_point(test["seed"]))
    if "figures" in test:
        draw_figures(interface, test["figures"])
    if "ellipses" in test:
        draw_ellipses(interface, test["ellipses"])

    interface.paint_shape()

    label_string = interface.time_label.text()
    elapsed_time = float(label_string.split()[0])

    return elapsed_time


def draw_figures(interface: Interface, json_figures) -> None:

    for json_figure in json_figures:

        for json_point in json_figure:
            point = parse_point(json_point)
            interface.add_point(point)
        
        interface.close_shape()

def draw_ellipses(interface: Interface, json_ellipses) -> None:

    tab_widget = interface.findChild(QTabWidget, "tabWidget")
    tab_widget.setCurrentIndex(1)

    for json_ellipse in json_ellipses:

        clear_fields(interface)

        parse_ellipse_fields(interface, json_ellipse)

        interface.draw_ellipse()

    tab_widget.setCurrentIndex(0)

def parse_point(json_point) -> QPoint:
    x, y = int(json_point["x"]), int(json_point["y"])
    return QPoint(x, y)


def parse_ellipse_fields(interface: Interface, json_ellipse):
    QTest.keyClicks(interface.ellipse_center_x, str(json_ellipse["center_x"]))
    QTest.keyClicks(interface.ellipse_center_y, str(json_ellipse["center_y"]))
    QTest.keyClicks(interface.ellipse_semi_major_axis, str(json_ellipse["semi_major_axis"]))
    QTest.keyClicks(interface.ellipse_semi_minor_axis, str(json_ellipse["semi_minor_axis"])) 

  
def clear_fields(interface: Interface):
    interface.ellipse_center_x.clear()
    interface.ellipse_center_y.clear()
    interface.ellipse_semi_major_axis.clear()
    interface.ellipse_semi_minor_axis.clear()
   