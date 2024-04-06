import pytest
import json
import time
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
        case "segment":
            qtbot.mouseClick(interface.plot_segment_button, Qt.MouseButton.LeftButton)
        case "spectrum":
            qtbot.mouseClick(interface.plot_spectrum_button, Qt.MouseButton.LeftButton)
        case "reset":
            qtbot.mouseClick(interface.clear_button, Qt.MouseButton.LeftButton)

def parse_fields(interface: Interface, action):
    data = action["input"]
    if "start_x" in data:
        QTest.keyClicks(interface.input_start_x, str(data["start_x"]))
    if "start_x" in data:
        QTest.keyClicks(interface.input_start_y, str(data["start_x"]))
    if "end_x" in data:
        QTest.keyClicks(interface.input_end_x, str(data["end_x"]))
    if "end_y" in data:
        QTest.keyClicks(interface.input_end_y, str(data["end_y"]))
    if "angle" in data:
        QTest.keyClicks(interface.input_angle, str(data["angle"]))
    if "algorithm" in data:
        match str(data["algorithm"]):
            case "dda":
                interface.algorithm.setCurrentIndex(0)
            case "bresenham_float":
                interface.algorithm.setCurrentIndex(1)
            case "bresenham_int":
                interface.algorithm.setCurrentIndex(2)
            case "bresenham_smooth":
                interface.algorithm.setCurrentIndex(3)
            case "wu":
                interface.algorithm.setCurrentIndex(4)
            case "build_in":
                interface.algorithm.setCurrentIndex(5)
  
def clear_fields(interface: Interface):
    interface.input_start_x.clear()
    interface.input_start_y.clear()
    interface.input_end_x.clear()
    interface.input_end_y.clear()
    interface.input_angle.clear()
    