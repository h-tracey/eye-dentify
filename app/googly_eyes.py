import os
import uuid
from typing import List, Tuple
from PIL import Image, ImageDraw
import face_recognition
from random import choice
from werkzeug.datastructures import FileStorage

class Googly:   

    def __init__(
        self, tmp_dir: str, image_resize_width: int = 400, apply_resizing: bool = True
    ):
        """Object to hold logic for facial feature detection/markup from images.

        Args:
            tmp_dir (str): The location of the tmp dir we will use for writing the
                file to disk
            image_resize_width (int, optional): The default width of images we wish
                to resize images to. Defaults to 400.
            apply_resizing (bool, optional): Whether to apply resizing to images. If
                false, the image will be processed as-is. this can be a much slower operation,
                but can help with large group phhotos contining multiple faces. Defaults to True.
        """
        self.tmp_dir = tmp_dir
        self.image_resize_width = image_resize_width
        self.apply_resizing = apply_resizing

    def resize_image(self, image: FileStorage, image_name: str) -> str:
        """persists image bytes to disk, optionally resizing the image 
        whilst maintaining aspect ratio.

        Args:
            image (FileStorage): the image as sent down the wire to flask.
            image_name (str): the name to save the image as (this should be
            unique to avoid clashes during concurrent requests).
        Returns:
            str: absolute path for where the image is persisted.
        """

        img = Image.open(image)
        if self.apply_resizing:
            wpercent = self.image_resize_width / float(img.size[0])
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((self.image_resize_width, hsize), Image.LANCZOS)
        img_path = f"{self.tmp_dir}/{image_name}.jpeg"
        img.save(img_path)
        return img_path

    @staticmethod
    def add_googly(drawable: ImageDraw, googly_target_coords: List[Tuple[int, int]]) -> None:
        """draws a googly eye on an image at a given face landmark.

        Args:
            drawable (ImageDraw): the drawable image to update.
            googly_target_coords (list[tuple[int, int]]): the target coordinates where
            the googly eyes should be placed.
        """

        min_x_bound = min(x for x, _ in googly_target_coords)
        max_x_bound = max(x for x, _ in googly_target_coords)

        min_y_bound = min(y for _, y in googly_target_coords)
        max_y_bound = max(y for _, y in googly_target_coords)

        x_coords = list(range(min_x_bound, max_x_bound))
        y_coords = list(range(min_y_bound, max_y_bound))

        op = choice(["add", "subtract"])
        if op == "add":
            radius = len(x_coords) + choice(range(len(y_coords)))
        else:
            radius = len(x_coords) - choice(range(len(y_coords)))

        drawable.circle(googly_target_coords[1], radius=radius, fill="white")
        drawable.circle(choice(googly_target_coords), radius=radius / 2, fill="black")

    def add_googlies(self, file: FileStorage) -> str:
        """takes in an image and superimposed randomised googly
        eyes onto the eyes of all detedted faces

        Args:
            file (FileStorage): the image as sent down the wire to flask.

        Returns:
            str: absolute path for where the image is persisted
        """

        # get a unique ID to enure image consistence accross concurrent requests
        tmp_image = str(uuid.uuid4())
        image_path = self.resize_image(file, tmp_image)

        # Load the jpg file into a numpy array
        image = face_recognition.load_image_file(image_path)

        os.remove(image_path)

        # Find all facial features in all the faces in the image
        face_landmarks_list = face_recognition.face_landmarks(image)

        print(f"found {len(face_landmarks_list)} face(s) in this photograph.")

        # Create a PIL imagedraw object so we can draw on the picture
        pil_image = Image.fromarray(image)
        d = ImageDraw.Draw(pil_image)

        for face_landmarks in face_landmarks_list:
            self.add_googly(d, face_landmarks["left_eye"])
            self.add_googly(d, face_landmarks["right_eye"])
        pil_image.save(image_path)
        return image_path
