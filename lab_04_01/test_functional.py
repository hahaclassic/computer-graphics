import pytest
import json
import time
from PyQt6.QtWidgets import QTabWidget
from src.interface import Interface
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt

TEST_FILE = "./test_data/test.json"
RESULT_DIR = "./results/"
TEST_REPEATS = 3 
BUFFER = "./func_buf.txt"

@pytest.fixture
def interface(qtbot):
    interface = Interface()
    qtbot.addWidget(interface)
    return interface

def test(interface: Interface, qtbot):

    with open(TEST_FILE, "r") as f:
        tests = json.load(f)

    report = open(BUFFER, "w")
    report.write(f"number of tests: {len(tests)}\n")

    for idx, test in enumerate(tests):
        
        elapsed_time = 0.0

        for _ in range(TEST_REPEATS):
            press_button(interface, qtbot, "reset")
            elapsed_time += run_test(interface, qtbot, test)

        test_time = (elapsed_time / TEST_REPEATS) * 1000
        report.write(f"< test: {idx + 1}, time: {test_time:.4f} >\n")

        path = RESULT_DIR + "test" + str(idx + 1)

        with open(path + "_description.txt", "w") as descrp_f:
            descrp_f.write(test["description"])

        image = interface.grab()

        image.save(path + "_image_.png")

    report.close()
    

def run_test(interface: Interface, qtbot, test) -> float:

    elapsed_time = 0.0
    for action in test["cmd"]:
        clear_fields(interface)
        parse_fields(interface, action)

        start = time.monotonic()
        press_button(interface, qtbot, action["type"])
        end = time.monotonic()

        elapsed_time += (end - start)

    return elapsed_time

def press_button(interface: Interface, qtbot, operation_type: str):
    match operation_type:
        case "circle":
            qtbot.mouseClick(interface.plot_circle_button, Qt.MouseButton.LeftButton)
        case "circle_spectrum":
            qtbot.mouseClick(interface.plot_circle_spectrum_button, Qt.MouseButton.LeftButton)
        case "ellipse":
            qtbot.mouseClick(interface.plot_ellipse_button, Qt.MouseButton.LeftButton)
        case "ellipse_spectrum":
            qtbot.mouseClick(interface.plot_ellipse_spectrum_button, Qt.MouseButton.LeftButton)
        case "reset":
            qtbot.mouseClick(interface.clear_button, Qt.MouseButton.LeftButton)

def parse_fields(interface: Interface, action):
    if "type" not in action or "algorithm" not in action:
        return
    
    tab_widget = interface.findChild(QTabWidget, "tabWidget")

    parse_figure_data(interface, action, tab_widget)
    parse_spectrum_data(interface, action, tab_widget)

    match str(action["algorithm"]):
        case "canonical":
            interface.algorithm.setCurrentIndex(0)
        case "parametric":
            interface.algorithm.setCurrentIndex(1)
        case "bresenham":
            interface.algorithm.setCurrentIndex(2)
        case "midpoint":
            interface.algorithm.setCurrentIndex(3)
        case "build_in":
            interface.algorithm.setCurrentIndex(4)

def parse_figure_data(interface: Interface, action, tab_widget: QTabWidget):
    action_type = str(action["type"])

    if action_type == "circle" or action_type == "circle_spectrum":
        tab_widget.setCurrentIndex(0)
        data = action["circle_data"]

        if "center_x" in data:
            QTest.keyClicks(interface.circle_center_x, str(data["center_x"]))
        if "center_y" in data:
            QTest.keyClicks(interface.circle_center_y, str(data["center_y"]))
        if "radius" in data:
            QTest.keyClicks(interface.circle_radius, str(data["radius"]))

    elif action_type == "ellipse" or action_type == "ellipse_spectrum":
        tab_widget.setCurrentIndex(1)
        data = action["ellipse_data"]

        if "center_x" in data:
            QTest.keyClicks(interface.ellipse_center_x, str(data["center_x"]))
        if "center_y" in data:
            QTest.keyClicks(interface.ellipse_center_y, str(data["center_y"]))
        if "semi_major_axis" in data:
            QTest.keyClicks(interface.ellipse_semi_major_axis, str(data["semi_major_axis"]))
        if "semi_minor_axis" in data:
            QTest.keyClicks(interface.ellipse_semi_minor_axis, str(data["semi_minor_axis"])) 

def parse_spectrum_data(interface: Interface, action, tab_widget: QTabWidget):
    action_type = str(action["type"])
    if action_type == "circle_spectrum":
        data = action["spectrum"]
        tab_widget.setCurrentIndex(0)

        if "step" in data:
            QTest.keyClicks(interface.circle_step, str(data["step"]))
        if "num_figures" in data:
            QTest.keyClicks(interface.circle_num_figures, str(data["num_figures"]))

    elif action_type == "ellipse_spectrum":
        data = action["spectrum"]
        tab_widget.setCurrentIndex(1)

        if "step" in data:
            QTest.keyClicks(interface.ellipse_step, str(data["step"]))
        if "num_figures" in data:
            QTest.keyClicks(interface.ellipse_num_figures, str(data["num_figures"]))

  
def clear_fields(interface: Interface):
    interface.circle_center_x.clear()
    interface.circle_center_y.clear()
    interface.circle_radius.clear()
    interface.circle_num_figures.clear()
    interface.circle_step.clear()
    interface.ellipse_center_x.clear()
    interface.ellipse_center_y.clear()
    interface.ellipse_semi_major_axis.clear()
    interface.ellipse_semi_minor_axis.clear()
    interface.ellipse_num_figures.clear()
    interface.ellipse_step.clear()
    