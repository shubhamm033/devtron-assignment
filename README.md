# devtron-assignment

Pre-Req

1.Make sure you have added aws key and aws secret key 
  in the settings file in project folder

2.Make Sure you have docker running in your machine

Step 1:

Create docker image using following command

docker build -t devtron-assignment .

Step 2:

Run container and map host machine 5000 port to containers 8000 port 
Use the folloing command

docker run -d -p 5000:8000 devtron-assignment

Step 3:

curl --location 'localhost:5000/search/text' \
--header 'Content-Type: application/json' \
--data '{ "keyword":"Hello","from":"2024-01-20", "to": "2024-01-24"}'