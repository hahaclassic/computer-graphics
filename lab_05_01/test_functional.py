import pytest
import json
from src.interface import Interface
from PyQt6.QtGui import QPolygon
from PyQt6.QtCore import QPoint

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

    interface.figures = parse_figures_data(test["figures"])
    interface.paint_shape()

    label_string = interface.time_label.text()
    elapsed_time = float(label_string.split()[0])

    return elapsed_time


def parse_figures_data(json_figures) -> list[QPolygon]:

    figures = []

    for json_figure in json_figures:
        figure = QPolygon()
        for point in json_figure:
            x, y = int(point["x"]), int(point["y"])
            figure.append(QPoint(x, y))
        figures.append(figure)

    return figures
