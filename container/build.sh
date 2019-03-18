docker build . -t flask-tutorial


docker build -t monkey-repo .
docker tag monkey-repo:latest 121769289400.dkr.ecr.us-east-1.amazonaws.com/monkey-repo:latest
docker push 121769289400.dkr.ecr.us-east-1.amazonaws.com/monkey-repo:latest

