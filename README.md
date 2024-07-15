# Receipt Processor

## Overview

Receipt Processor is a web service that processes receipts and calculates points based on predefined rules. The service provides two endpoints: one for submitting a receipt for processing and another for retrieving the points awarded for a specific receipt.

The application is bulit using python and flask, this repository includes the required setup to run the application, Kindly follow the below steps to run app.py

## How to Run the Application

### Prerequisites

- Docker

### Steps

1. **Clone the Repository**:

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Build the Docker Image**:

    ```sh
    docker build -t praveen_fetch_oa .
    ```

3. **Run the Docker Container**:

    ```sh
    docker run -p 8080:8080 praveen_fetch_oa
    ```

4. **Access the API**:

    - Submit a Receipt: `POST http://localhost:8080/receipts/process`
    - Get Points: `GET http://localhost:8080/receipts/{receipt_id}/points`

#### Example Request

##### POST
```sh
curl -X POST http://localhost:8080/receipts/process -H "Content-Type: application/json" -d '{
  "retailer": "Target",
  "purchaseDate": "2022-01-01",
  "purchaseTime": "13:01",
  "items": [
    {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
    {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
    {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
    {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
    {"shortDescription": "Klarbrunn 12-PK 12 FL OZ", "price": "12.00"}
  ],
  "total": "35.35"
}'
```
##### GET
```sh
curl http://localhost:8080/receipts/7fb1377b-b223-49d9-a31a-5a02701dd310/points
```
#### Example Response

##### POST
```json
{ "id": "6ea6ec1d-744d-41d3-ae65-8e3b575e156e" }
```

##### GET
```json
{"points":28}
```

