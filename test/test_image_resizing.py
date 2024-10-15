import unittest
from unittest.mock import patch, MagicMock
from PIL import Image
from app.googly_eyes import Googly

class TestImageResize(unittest.TestCase):
    
    @patch('PIL.Image.open')
    @patch('werkzeug.datastructures.FileStorage')
    def test_save_image_without_resizing(self, mock_file_storage, mock_image_open):
        # Arrange
        mock_image = MagicMock(spec=Image.Image)
        mock_image.size = (800, 600)
        mock_image_open.return_value = mock_image

        mock_file = MagicMock()

        instance = Googly('/tmp', apply_resizing=False)

        # Act
        result = instance.resize_image(mock_file, 'test_image')

        # Assert
        mock_image.save.assert_called_once_with('/tmp/test_image.jpeg')
        self.assertEqual(result, '/tmp/test_image.jpeg')

    @patch('PIL.Image.open')
    @patch('werkzeug.datastructures.FileStorage')
    def test_resize_image_with_resizing(self, mock_file_storage, mock_image_open):
        # Arrange
        mock_image = MagicMock(spec=Image.Image)  # Mock the image object
        mock_image.size = (800, 600)  # Mock image size
        mock_image_open.return_value = mock_image

        mock_file = MagicMock()  # Mock the file storage object

        instance = Googly('/tmp',  image_resize_width=400, apply_resizing=True)

        # Act
        result = instance.resize_image(mock_file, 'test_image')

        # Assert
        mock_image.resize.assert_called_once_with((400, 300), Image.LANCZOS)  # Check resizing
        self.assertEqual(result, '/tmp/test_image.jpeg')  # Check correct path was returned
