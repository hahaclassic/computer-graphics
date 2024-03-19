import pytest
import json
import time
from src.interface import Interface

from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt

TEST_FILE = "./test_data/test.json"

@pytest.fixture
def interface(qtbot):
    interface = Interface()
    qtbot.addWidget(interface)
    return interface

def test(interface, qtbot):

    with open(TEST_FILE, "r") as f:
        tests = json.load(f)

    for i, test in enumerate(tests):
        run_test(interface, qtbot, test)

def run_test(interface: Interface, qtbot, test):

    # Добавить время
    for action in test["cmd"]:
        press_button(interface, qtbot, "reset")
        parse_fields(interface, action)
        press_button(interface, qtbot, action["type"])
    
    image = interface.grab()
    image_name = "./results/test" + str(test["test_number"]) + ".png"
    image.save(image_name)
    # Добавить сохранение в папку изображений и описания

def press_button(interface, qtbot, operation_type: str):
    match operation_type:
        case "move":
            qtbot.mouseClick(interface.offset_button, Qt.MouseButton.LeftButton)
        case "rotate":
            qtbot.mouseClick(interface.rotate_button, Qt.MouseButton.LeftButton)
        case "scale":
            qtbot.mouseClick(interface.scale_button, Qt.MouseButton.LeftButton)
        case "reset":
            qtbot.mouseClick(interface.button_reset, Qt.MouseButton.LeftButton)

def parse_fields(interface, action):
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
