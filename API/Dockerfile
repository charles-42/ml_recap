FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip 

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

# docker build -t spotify_linear_model_api .
# docker run -dp 80:6000 spotify_linear_model_api
# c854ebf532a3d808f6324b40fb0efb8ebca361fcf7812d72039febe802802005
#docker --context api_spotify_aci run -p 80:80 spotify_linear_model_api

#az login
# az acr login --name spotifyregistrycontainer
# docker tag spotify_linear_model_api spotifyregistrycontainer.azurecr.io/spotify_linear_model_api:latest
# docker push  spotifyregistrycontainer.azurecr.io/spotify_linear_model_api:latest