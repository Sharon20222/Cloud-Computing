
```markdown
# Machine Learning on Kubernetes

## CS571 - Week 10 Homework 1

**Name:** Saron Yemane Haile
**ID:** 20069

[Exercise Link](https://hc.labnet.sfbu.edu/~henry/sfbu/course/cloud_computing/genai/slide/exercise_kubernetes.html)

---

## Overview

This project demonstrates deploying a machine learning model on Kubernetes using Docker and Flask. The model, which is a logistic regression classifier, predicts customer purchasing behavior based on specific features. The deployment is managed using Minikube in Google Cloud Platform (GCP).

---

## Project Structure

- `Dockerfile`: Defines the environment and application setup.
- `flask_api.py`: Contains the Flask application that serves the model.
- `requirements.txt`: Lists the Python dependencies required by the Flask application.
- `logreg.pkl`: The pre-trained logistic regression model.

---

## Setup and Installation

### Prerequisites

1. **Google Cloud Platform (GCP) Account**
2. **Minikube Installed**: To manage Kubernetes clusters locally.
3. **Docker Installed**: To containerize the application.

### Steps

1. **Start Minikube:**
   ```sh
   minikube start
   ```

2. **Create `requirements.txt`:**
   ```sh
   nano requirements.txt
   ```
   Add the following content:
   ```plaintext
   Flask==1.1.1
   gunicorn==19.9.0
   itsdangerous==1.1.0
   Jinja2==2.10.1
   MarkupSafe==1.1.1
   Werkzeug==0.15.5
   numpy==1.19.5
   scipy>=0.15.1
   scikit-learn==0.24.2
   matplotlib>=1.4.3
   pandas>=0.19
   flasgger==0.9.42
   ```

3. **Upload `logreg.pkl`:**
   - Click the three dots in the top-right part of the Cloud Shell Terminal.
   - Choose `Upload` and select the `logreg.pkl` file.

4. **Create `flask_api.py`:**
   ```sh
   nano flask_api.py
   ```
   Add the following content:
   ```python
   # -*- coding: utf-8 -*-
   """
   Created on Mon May 25 12:50:04 2020
   @author: pramod.singh
   """
   from flask import Flask, request
   import numpy as np
   import pickle
   import pandas as pd
   from flasgger import Swagger

   app = Flask(__name__)
   Swagger(app)
   pickle_in = open("logreg.pkl", "rb")
   model = pickle.load(pickle_in)

   @app.route('/')
   def home():
       return "Welcome to the Flask API!"

   @app.route('/predict', methods=["GET"])
   def predict_class():
       """Predict if Customer would buy the product or not.
       ---
       parameters:
         - name: age
           in: query
           type: number
           required: true
         - name: new_user
           in: query
           type: number
           required: true
         - name: total_pages_visited
           in: query
           type: number
           required: true
       responses:
         200:
           description: Prediction
       """
       age = int(request.args.get("age"))
       new_user = int(request.args.get("new_user"))
       total_pages_visited = int(request.args.get("total_pages_visited"))
       prediction = model.predict([[age, new_user, total_pages_visited]])
       return "Model prediction is " + str(prediction)

   @app.route('/predict_file', methods=["POST"])
   def prediction_test_file():
       """Prediction on multiple input test file.
       ---
       parameters:
         - name: file
           in: formData
           type: file
           required: true
       responses:
         200:
           description: Test file Prediction
       """
       df_test = pd.read_csv(request.files.get("file"))
       prediction = model.predict(df_test)
       return str(list(prediction))

   if __name__ == '__main__':
       app.run(debug=True, host='0.0.0.0', port=5000)
   ```

5. **Create `Dockerfile`:**
   ```sh
   nano Dockerfile
   ```
   Add the following content:
   ```dockerfile
   FROM python:3.8-slim
   WORKDIR /app
   COPY . /app
   EXPOSE 5000
   RUN pip install -r requirements.txt
   CMD ["python", "flask_api.py"]
   ```

6. **Build the Docker Image:**
   ```sh
   sudo docker build -t ml_app_docker .
   ```

7. **Run the Docker Container:**
   ```sh
   docker container run -p 5000:5000 ml_app_docker
   ```

---

## Testing

1. **Access the Flask Application:**
   - Click the "Web preview" button (the eye icon) in the top-right corner of the Cloud Shell terminal.
   - Select "Preview on port 5000".

2. **Interact with the API:**
   - Append `/apidocs/` to the URL to access the API documentation.
   - **GET Request:**
     - Click `Try it out`, fill in the parameters, and click `Execute`.
   - **POST Request:**
     - Upload a test data file and click `Execute` to see predictions for multiple inputs.

3. **Stopping the Docker Container:**
   ```sh
   docker ps
   ```
   - Note the `CONTAINER_ID`.
   ```sh
   docker kill <CONTAINER_ID>
   ```

---

## Enhancement

**Future Enhancements:**
- **Model Improvement:** Train and deploy a more complex model for better accuracy.
- **Scalability:** Use Kubernetes for scaling the application based on demand.
- **Logging and Monitoring:** Implement logging and monitoring for better maintenance and troubleshooting.

---

## Conclusion

This project showcases how to deploy a machine learning model using Docker and Flask, and manage it with Kubernetes. It demonstrates the power of containerization and cloud-based deployments in delivering scalable machine learning solutions.

---

