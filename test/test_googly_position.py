import unittest
from unittest.mock import MagicMock, patch
from PIL import ImageDraw
from app.googly_eyes import Googly

class TestGooglyEye(unittest.TestCase):

    def test_add_googly_adds_circles(self):
        # Arrange
        mock_drawable = MagicMock(spec=ImageDraw.ImageDraw)
        googly_target_coords = [(50, 50), (150, 150)]        

        # Act
        Googly.add_googly(mock_drawable, googly_target_coords)

        # Assert
        expected_radius = list(range(200))
        self.assertEqual(mock_drawable.circle.call_count, 2)
