### Build recommender api server
docker build . --tag faisalbegins/recommender-api:latest

### Run recommender api server
docker run -it  -v /Users/Faisal/Development/recommender-storage/models:/mnt --env DATA_ROOT_DIR='/mnt' -p 5000:5000 faisalbegins/recommender-api:latest