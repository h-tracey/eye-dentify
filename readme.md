# EYE-DENTITY API
This is a simple api which leverages the dlib API to do facial feature recognition.
![Keir Starmer!](/assets/starmer-googlied.jpg "The Prime Minister of the UK with random googly eyes superimposed over his eyes")

# Running the API locally
A prebuilt version of this image is available on Docker Hub. Use `docker pull akaishmael/eye-dentify-api` to get the image. Otherwise, the container can be built manually using `docker build -t <some-meaningful-tag> .` from within this project's root. Start the service via `docker run -p 5000:5000 akaishmael/eye-dentify-api`
```
curl --request POST \
  --url http://<host>:5000/googly \
  --header 'Content-Type: multipart/form-data' \
  --header 'User-Agent: insomnia/10.0.0' \
  --form 'file=@some/path/to/photo.jpg'
  ```
  # Examples


### Multiple People
  ![Group Before!](/assets/group.jpg "before the eyes are added")
  ![Group After!](/assets/group-googlied.jpg "With googly eyes")

### Big Group
on large group photos, the automatic (aspect-ratio maintaining) resizing can cause problems with the face detection. As such, we can make te request with the param `resize=false`, and the original file size will be maintained. This has implications for the performance of the service, which is why resizing is on by default.
  ![Big Group Before!](/assets/biggroup.jpg "before the eyes are added")
  ![Big Group After!](/assets/biggroup-googlied.jpg "With googly eyes")
  ![Big Group After!](/assets/biggroup-googlied-big.jpg "With googly eyes")
