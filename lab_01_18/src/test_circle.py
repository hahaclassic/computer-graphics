import unittest
from src.circle import Circle, QPointF

class TestCircle(unittest.TestCase):
    def setUp(self):

        # Valid circle1
        self.valid_circle1 = Circle(QPointF(1,0), QPointF(0,1), QPointF(0,-1))
        
        # Valid circle2
        self.valid_circle2 = Circle(QPointF(20,20), QPointF(30,30), QPointF(36,12))

        # Valid circle3
        self.valid_circle3 = Circle(
            QPointF(23.5, 40),
            QPointF(-15.109321980635, 57.998844109706),
            QPointF(-18.0563608879779, 24.9594603992044)
        )

        # Invalid (degenerate) circle1
        self.invalid_circle1 = Circle(QPointF(1,1), QPointF(20,20), QPointF(30,30))

        # Invalid (degenerate) circle2 
        self.invalid_circle2 = Circle(QPointF(1,1), QPointF(1,1), QPointF(1,1))

    def test_is_valid(self):
        self.assertEqual(self.valid_circle1.is_valid(), True)
        self.assertEqual(self.valid_circle2.is_valid(), True)
        self.assertEqual(self.valid_circle3.is_valid(), True)

        self.assertEqual(self.invalid_circle1.is_valid(), False)
        self.assertEqual(self.invalid_circle2.is_valid(), False)
    
    def test_center(self):
        self.assertEqual(self.valid_circle1.center(), QPointF(0,0))
        self.assertEqual(self.valid_circle2.center(), QPointF(30,20))
        # self.assertEqual(self.valid_circle3.center(), QPointF(0,40))

        self.assertEqual(self.invalid_circle1.center(), QPointF(0,0)) 
        self.assertEqual(self.invalid_circle2.center(), QPointF(0,0))

    def test_radius(self):
        self.assertAlmostEqual(self.valid_circle1.radius(), 1.0, places=3)
        self.assertAlmostEqual(self.valid_circle2.radius(), 10.0, places=3)
        self.assertAlmostEqual(self.valid_circle3.radius(), 23.5, places=3)

        self.assertAlmostEqual(self.invalid_circle1.radius(), 0.0, places=3)
        self.assertAlmostEqual(self.invalid_circle2.radius(), 0.0, places=3)
    
    def test_centers_distance(self):
        self.assertAlmostEqual(self.valid_circle1.centers_distance(self.valid_circle2), 36.0555, places=3)
        self.assertAlmostEqual(self.valid_circle3.centers_distance(self.valid_circle1), 40.0, places=3)
        self.assertAlmostEqual(self.valid_circle2.centers_distance(self.valid_circle3), 36.0555, places=3)
