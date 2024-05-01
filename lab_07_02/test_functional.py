import pytest
import json
from src.interface import Interface
from PyQt6.QtCore import QLine, QPointF, QRect

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

    interface.segments = parse_segments_data(test["segments"])
    interface.rectangle = parse_rect_data(test["rectangle"])
    interface.update_scene()

    interface.cut()

    label_string = interface.time_label.text()
    elapsed_time = float(label_string.split()[0])

    return elapsed_time


def parse_segments_data(json_segments) -> list[QLine]:

    segments = []

    for json_segment in json_segments:
        segment = QLine()
        start_x = float(json_segment["start_x"])
        start_y = float(json_segment["start_y"])
        end_x = float(json_segment["end_x"])
        end_y = float(json_segment["end_y"])

        segment.setP1(QPointF(start_x, start_y).toPoint())
        segment.setP2(QPointF(end_x, end_y).toPoint())
        segments.append(segment)

    return segments

def parse_rect_data(json_rectangle) -> QRect:

    left_top_x = float(json_rectangle["left_top_x"])
    left_top_y = float(json_rectangle["left_top_y"])
    right_bottom_x = float(json_rectangle["right_bottom_x"])
    right_bottom_y = float(json_rectangle["right_bottom_y"])

    top_left = QPointF(left_top_x, left_top_y).toPoint()
    bottom_right = QPointF(right_bottom_x, right_bottom_y).toPoint()
    return QRect(top_left, bottom_right)
