from flask import Flask, request, abort, send_file, after_this_request
import os
import shutil
from googly_eyes import Googly

UPLOAD_FOLDER = "/uploads"
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])

shutil.rmtree(UPLOAD_FOLDER, ignore_errors=True)
os.mkdir(UPLOAD_FOLDER)

app = Flask("Googly Eyes API")


def allowed_file(filename: str) -> bool:
    """
    Returns:
        bool: whether the attached file has the appropriate file extention
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/googly", methods=["POST"])
def post():
    #file validity checks
    if "file" not in request.files:
        print(request.files)
        abort(400, "No file part")
    file = request.files["file"]
    if file.filename == "":
        abort(400, "No selected file")
    if not allowed_file(file.filename):
        abort(400, f"Invalid file type. Must be one of {ALLOWED_EXTENSIONS}.")

    resize_image = request.args.get("resize", default="true").lower() == "true"
    
    image_edit = Googly(UPLOAD_FOLDER, 700, resize_image)
    edited_file = image_edit.add_googlies(file)

    @after_this_request
    def clean_up(resp):
        """Once we are done with this request, we should remove any local copies
        of files as these should not be persisted.
        """
        os.remove(edited_file)
        return resp

    return send_file(edited_file, mimetype="image/jpeg")


# debug driver
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
