import math
import unittest
from src.circle import QPointF
from src.maxarea import find_max_area

class TestFindMaxArea(unittest.TestCase):

    # Checking that the function calculates the area correctly
    def test_area_equal_radii(self):
        set1 = [QPointF(1, 0), QPointF(0,1), QPointF(0,-1)]
        set2 = [QPointF(5,0), QPointF(4,1), QPointF(4,-1)]
        area, _, _ = find_max_area(set1, set2)
        self.assertAlmostEqual(area, 4.0)
   
    # Checking that the function calculates the area correctly
    def test_area_circles_arranged_horizontally(self):
        set1 = [QPointF(1, 0), QPointF(0,1), QPointF(0,-1)]
        set2 = [QPointF(6,0), QPointF(4,2), QPointF(4,-2)]
        area, _, _ = find_max_area(set1, set2)
        self.assertAlmostEqual(area, 6.18465, places=3)
    
    # Checking that the function calculates the area correctly
    def test_area_circles_arranged_vertically(self):
        set1 = [QPointF(1,0), QPointF(0,1), QPointF(0,-1)]
        set2 = [QPointF(0,6), QPointF(2,4), QPointF(-2,4)]
        area, _, _ = find_max_area(set1, set2)
        self.assertAlmostEqual(area, 6.18465, places=3)

    # Checking that the function calculates the area correctly
    def test_area_general_case(self):
        set1 = [QPointF(1,0), QPointF(0,1), QPointF(0,-1)]
        set2 = [QPointF(4,1), QPointF(4,5), QPointF(6,3)]
        area, _, _ = find_max_area(set1, set2)
        self.assertAlmostEqual(area, 7.6485, places=3)

    # Checking that the function correctly finds the circles and the area
    def test_search(self):
        set1 = [
            QPointF(1,0), QPointF(0,1), QPointF(0,-1),
            QPointF(2,0), QPointF(0,2), QPointF(0,-2)
        ]
        set2 = [
            QPointF(6,0), QPointF(4,2), QPointF(4,-2),
            QPointF(0,6), QPointF(2,4), QPointF(-2,4),
            QPointF(4,1), QPointF(4,5), QPointF(6,3)
        ]
        area, circle1, circle2 = find_max_area(set1, set2)

        self.assertAlmostEqual(area, 103.59924, places=3)

        self.assertEqual(circle1.center(), QPointF(-1.5, 0.0))
        self.assertAlmostEqual(circle1.radius(), 2.5, places=3)

        self.assertEqual(circle2.center(), QPointF(9.5, 9.5))
        self.assertAlmostEqual(circle2.radius(), 10.12422, places=3)

    # Checking that the function behaves correctly when it is impossible
    # to calculate the result
    def test_search_degenerate_circles(self):
        set1 = [QPointF(1,1), QPointF(20,20), QPointF(30,30)]
        set2 = [QPointF(1,1), QPointF(1,1), QPointF(1,1)]

        area, circle1, circle2 = find_max_area(set1, set2)

        self.assertAlmostEqual(area, -math.inf)
        self.assertEqual(circle1, None)
        self.assertEqual(circle2, None)
        
    # Checking that the function behaves correctly when it is impossible
    # to calculate the result
    def test_search_when_one_circle_in_another(self):
        set1 = [QPointF(1,0), QPointF(0,1), QPointF(0,-1)]
        set2 = [QPointF(2,0), QPointF(0,2), QPointF(0,-2)]

        area, circle1, circle2 = find_max_area(set1, set2)

        self.assertAlmostEqual(area, -math.inf)
        self.assertEqual(circle1, None)
        self.assertEqual(circle2, None)

