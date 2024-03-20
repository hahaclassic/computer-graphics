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

    start = time.monotonic()
    for action in test["cmd"]:
        clear_fields(interface)
        parse_fields(interface, action)
        press_button(interface, qtbot, action["type"])
    elapsed_time = time.monotonic() - start

    return elapsed_time

def press_button(interface: Interface, qtbot, operation_type: str):
    match operation_type:
        case "move":
            qtbot.mouseClick(interface.offset_button, Qt.MouseButton.LeftButton)
        case "rotate":
            qtbot.mouseClick(interface.rotate_button, Qt.MouseButton.LeftButton)
        case "scale":
            qtbot.mouseClick(interface.scale_button, Qt.MouseButton.LeftButton)
        case "reset":
            qtbot.mouseClick(interface.button_reset, Qt.MouseButton.LeftButton)

def parse_fields(interface: Interface, action):
    data = action["input"]
    if "offset_dx" in data:
        QTest.keyClicks(interface.offset_input_x, str(data["offset_dx"]))
    if "offset_dy" in data:
        QTest.keyClicks(interface.offset_input_y, str(data["offset_dy"]))
    if "rotate_center_x" in data:
        QTest.keyClicks(interface.rotate_input_x, str(data["rotate_center_x"]))
    if "rotate_center_y" in data:
        QTest.keyClicks(interface.rotate_input_y, str(data["rotate_center_y"]))
    if "angle" in data:
        QTest.keyClicks(interface.rotate_angle_input, str(data["angle"]))
    if "scale_center_x" in data:
        QTest.keyClicks(interface.scale_input_x, str(data["scale_center_x"]))
    if "scale_center_y" in data:
        QTest.keyClicks(interface.scale_input_y, str(data["scale_center_y"]))
    if "scale_ratio" in data:
        QTest.keyClicks(interface.scale_ratio_input, str(data["scale_ratio"]))

def clear_fields(interface: Interface):
    interface.offset_input_x.clear()
    interface.offset_input_y.clear()
    interface.rotate_input_x.clear()
    interface.rotate_input_y.clear()
    interface.rotate_angle_input.clear()
    interface.scale_input_x.clear()
    interface.scale_input_y.clear()
    interface.scale_ratio_input.clear()
    