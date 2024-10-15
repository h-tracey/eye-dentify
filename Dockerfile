FROM animcogn/face_recognition:cpu

COPY app/ app/

ENV PYTHONPATH=/app
WORKDIR /app
RUN apt-get update && apt install gcc -y
RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
ENTRYPOINT [ "uwsgi", "--ini", "wsgi.ini" ]