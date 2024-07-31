# **Configmap: Signature Project: MongoDB + Python Flask Web Framework + REST API + GKE**

## **Overview**

The Bookshelf Management System is a RESTful API designed for managing a collection of books. This project includes a Flask application that interacts with a MongoDB database and is deployed on Google Kubernetes Engine (GKE). It features endpoints to create, read, update, and delete book records. The system also includes a student server that demonstrates how to interact with the API.

## **Features**

- **CRUD Operations**:
  - **Create**: Add new books to the collection.
  - **Read**: Retrieve details of all books or a specific book.
  - **Update**: Modify the details of an existing book.
  - **Delete**: Remove a book from the collection.

- **Deployment**:
  - Deployed on GKE using Kubernetes.
  - Exposed via Ingress with Nginx.

## **Requirements**

- **Google Kubernetes Engine (GKE)**
- **MongoDB**
- **Flask**
- **Python**
- **curl**

## **Setup and Installation**

### **1. Clone the Repository**

```bash
git clone https://github.com/your-repo/bookshelf-management-system.git
cd bookshelf-management-system
```

### **2. Environment Configuration**

#### **Environment Variables**

Ensure you have the following environment variables set for both the student server and the bookshelf service:

- **`MONGO_URL`**: External IP or hostname of your MongoDB instance.
- **`MONGO_DATABASE`**: Name of the MongoDB database.

### **3. MongoDB Configuration**

Create a `ConfigMap` for MongoDB configuration:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: bookshelf-config
data:
  MONGO_URL: "<your-mongodb-external-ip>"
  MONGO_DATABASE: "mydb"
```

### **4. Flask Application**

**Deployment Configuration:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: bookshelf-deployment
  labels:
    app: bookshelf-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: bookshelf-deployment
  template:
    metadata:
      labels:
        app: bookshelf-deployment
    spec:
      containers:
        - image: your-docker-repo/bookshelf
          imagePullPolicy: Always
          name: bookshelf
          ports:
            - containerPort: 5000
          env:
            - name: MONGO_URL
              valueFrom:
                configMapKeyRef:
                  name: bookshelf-config
                  key: MONGO_URL
            - name: MONGO_DATABASE
              valueFrom:
                configMapKeyRef:
                  name: bookshelf-config
                  key: MONGO_DATABASE
```

**Service Configuration:**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: bookshelf-service
spec:
  type: LoadBalancer
  ports:
    - port: 5000
      targetPort: 5000
  selector:
    app: bookshelf-deployment
```

**Ingress Configuration:**

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: bookshelf-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
spec:
  rules:
    - host: cs571.project.com
      http:
        paths:
          - path: /bookshelf(/|$)(.*)
            pathType: Prefix
            backend:
              service:
                name: bookshelf-service
                port:
                  number: 5000
```

### **5. Student Server**

**Deployment Configuration:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: studentserver-deployment
  labels:
    app: studentserver-deploy
spec:
  replicas: 1
  selector:
    matchLabels:
      app: studentserver-deploy
  template:
    metadata:
      labels:
        app: studentserver-deploy
    spec:
      containers:
        - image: your-docker-repo/studentserver
          imagePullPolicy: Always
          name: studentserver
          ports:
            - containerPort: 8080
          env:
            - name: MONGO_URL
              valueFrom:
                configMapKeyRef:
                  name: studentserver-config
                  key: MONGO_URL
            - name: MONGO_DATABASE
              valueFrom:
                configMapKeyRef:
                  name: studentserver-config
                  key: MONGO_DATABASE
```

**Service Configuration:**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: studentserver-service
spec:
  type: LoadBalancer
  ports:
    - port: 8080
      targetPort: 8080
  selector:
    app: studentserver-deploy
```

**Ingress Configuration:**

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: studentserver-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
spec:
  rules:
    - host: cs571.project.com
      http:
        paths:
          - path: /studentserver(/|$)(.*)
            pathType: Prefix
            backend:
              service:
                name: studentserver-service
                port:
                  number: 8080
```

## **Endpoints**

### **Bookshelf API**

- **GET /bookshelf/books**
  - Retrieve all books.

- **POST /bookshelf/book**
  - Create a new book.
  - Request Body:
    ```json
    {
      "book_name": "string",
      "book_author": "string",
      "isbn": "string"
    }
    ```

- **PUT /bookshelf/book/{id}**
  - Update an existing book.
  - Request Body:
    ```json
    {
      "book_name": "string",
      "book_author": "string",
      "isbn": "string"
    }
    ```

- **DELETE /bookshelf/book/{id}**
  - Delete a book by ID.

### **Student Server API**

- **GET /studentserver/api/score?student_id={id}**
  - Retrieve student details by student ID.

## **Testing**

Use `curl` commands to test the API endpoints:

- **Create a Book**:
  ```bash
  curl -X POST -d "{\"book_name\": \"cloud computing\",\"book_author\": \"unknown\", \"isbn\": \"123456\" }" http://cs571.project.com/bookshelf/book
  ```

- **Update a Book**:
  ```bash
  curl -X PUT -d "{\"book_name\": \"123\",\"book_author\": \"test\", \"isbn\": \"123updated\" }" http://cs571.project.com/bookshelf/book/{id}
  ```

- **Delete a Book**:
  ```bash
  curl -X DELETE http://cs571.project.com/bookshelf/book/{id}
  ```

- **Fetch All Books**:
  ```bash
  curl http://cs571.project.com/bookshelf/books
  ```

- **Fetch Student Details**:
  ```bash
  curl http://cs571.project.com/studentserver/api/score?student_id={id}
  ```

## **Troubleshooting**

- Ensure MongoDB is correctly configured and accessible.
- Check Kubernetes logs for errors if services are not reachable.
- Verify `ConfigMap` and `Ingress` configurations for correct settings.

## **Presentation Slides**
- https://docs.google.com/presentation/d/1LtEhS3HNJFIEZ4s_nZElea39hB8_XgnoJN8-GQ4s5CY/edit?usp=sharing
  
