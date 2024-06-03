import pytest
import json
from src.interface import Interface
from PyQt6.QtCore import QPointF, QPoint
from PyQt6.QtGui import QPolygon
import src.horizon as horizon

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
    x_interval = parse_interval_data(test["x_interval"])
    z_interval = parse_interval_data(test["z_interval"])
    transform = parse_transform_data(test["transform"])
    interface.function_box.setCurrentIndex(
        int(test["func_num"])
    )

    def get_data():
        return x_interval, z_interval, transform
    interface.get_data = get_data

    interface.view.setMinimumSize(836, 903)
    interface.plot()

    label_string = interface.time_label.text()
    elapsed_time = float(label_string.split()[0])

    return elapsed_time


def parse_transform_data(json_transform) -> horizon.Transformation:
    angle_x = float(json_transform["angle_x"])
    angle_y = float(json_transform["angle_y"])
    angle_z = float(json_transform["angle_z"])
    scale_ratio = float(json_transform["scale_ratio"])
    return horizon.Transformation(
        horizon.Rotation(angle_x, angle_y, angle_z),
        scale_ratio
    )


def parse_interval_data(json_interval) -> horizon.Interval:
    start, end = float(json_interval['start']), float(json_interval['end']) 
    step = float(json_interval['step'])
    return horizon.Interval(start, end, step)
