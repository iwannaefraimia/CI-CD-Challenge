# CI-CD-Challenge
## Mars Mission CRUD API 🚀

This is a simple CRUD API for managing space station resources.

## Project Overview
This API allows users to manage space station resources, including their name, ID, and quantity. The project is containerized with Docker and follows a CI/CD pipeline using GitHub Actions to ensure quality and automated deployment.
## How to Run

1. Clone the repository:
git clone https://github.com/iwannaefraimia/CI-CD-Challenge.git / cd CI-CD-Challenge

3. Create and activate a virtual environment:
python -m venv venv source venv/bin/activate (For Mac/Linux) / venv\Scripts\activate (For Windows)

3. Install dependencies:
pip install -r requirements.txt

4. Run the application:
python app.py

5. API Endpoints:
- `POST /resources` → Add new resource
- `GET /resources` → Get all resources
- `PUT /resources/:id` → Update a resource
- `DELETE /resources/:id` → Delete a resource

#### CI/CD Pipeline
CI - Mission Safety Checks
The project uses GitHub Actions for continuous integration. Every push triggers:
Linting with pylint
Unit testing with pytest

#### Build Automation
The application is Dockerized using a Dockerfile.
A GitHub Actions workflow builds the Docker image and pushes it to Docker Hub.

#### Deployment
The CI/CD pipeline ensures automatic deployment of a working version of the API.
Branch protection rules ensure only tested and reviewed code is merged into main.
Running with Docker
To build and run the application inside a container:

docker build -t mars-mission-api .
docker run -p 5000:5000 mars-mission-api

Enjoy the Mars Mission! 🚀
