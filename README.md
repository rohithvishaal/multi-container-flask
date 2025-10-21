# Multi Container Flask Application
- A simple flask app that shows a random quote
- Uses postgres as db
- Made this to re-learn on how to write **Docker, Dockerfile and docker-compose.yaml**

# To Run it your System
- make sure you have docker installed
- clone this repo and then run
```shell
docker-compose up --build
```
- Go to `http://localhost`  
### The Env file that I referred in the compose file 
```
DB_NAME="quotes"
DB_USER="postgres"
DB_PASS="tester@123"
DB_HOST="localhost"
DB_PORT=5432
```

### Here's how the end app looks like
- As said it is good app to nail down your fundamentals on Docker
<img width="2940" height="1912" alt="image" src="https://github.com/user-attachments/assets/49edbbbe-b9ec-4c4f-bcf8-4414d01ee2d6" />

