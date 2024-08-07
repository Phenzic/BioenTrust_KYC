# Client Admin Documentation


## Table of Contents
- [Endpoints](#endpoints)
  - [Create App](#post-apicreate_app)


## Base URL
```
<base-url>/client
```

### Authentication
All endpoints require JWT authentication. Include the token in the `Authorization` header as follows:
```
Authorization: Bearer <your_token>
```

## Endpoints

### Admin WebSocket
#### `GET /admin_websocket/<endpoint>`
Fetches various client data based on the specified endpoint.

- **URL Parameters:**
  - `endpoint`: The specific data to retrieve. Valid values are `verifications`, `get_all_apps`, `profile`, `charges`.

- **Response:**
  - `200 OK`: Returns the requested data.
  - `404 Not Found`: Invalid endpoint specified.
  - `500 Internal Server Error`: Server error.

- **Example Request:**
  ```http
  GET /admin_websocket/profile
  ```

- **Example Response:**
  ```json
  {
      "client_id": "12345",
      "name": "John Doe",
      "email": "john.doe@example.com"
  }
  ```

### Get User Details
#### `POST /get-user-details`
Fetches detailed information about a user.

- **Request Body:**
  ```json
  {
      "user_id": "658b2f8051ac8289de78c515"
  }
  ```

- **Response:**
  - `200 OK`: Returns user details.

- **Example Request:**
  ```http
  POST /get_user_details
  Content-Type: application/json

  {
      "user_id": "658b2f8051ac8289de78c515"
  }
  ```

- **Example Response:**
  ```json
  {
      "user_data": {
          "user_id": "user123",
          "name": "Jane Smith",
          "email": "jane.smith@example.com"
      }
  }
  ```

### Dashboard
#### `GET /dashboard/all-data`
Fetches dashboard data, including counts of different statuses.

- **Response:**
  - `200 OK`: Returns the dashboard data.

- **Example Request:**
  ```http
  GET /dashboard
  ```

- **Example Response:**
  ```json
  {
      "Total": 100,
      "Success": 80,
      "Failed": 20
  }
  ```

### 4. Get Wallet Transactions
#### `GET /wallet_transactions/<user_id>`
Fetches wallet transactions for a user.


- **Response:**
  - `200 OK`: Returns wallet transactions.

- **Example Request:**
  ```http
  GET /get-wallet-transactions
  ```

- **Example Response:**
  ```json
  [
      {
          "transaction_id": "txn123",
          "amount": 100,
          "type": "fund",
          "status": "Success"
      }
  ]
  ```

### Fund Wallet
#### `POST /fund`
Adds funds to a user's wallet.

- **Request Body:**
  ```json
  {
      "amount": 50
  }
  ```

- **Response:**
  - `200 OK`: Returns updated user data.

- **Example Request:**
  ```http
  POST /fund_wallet
  Content-Type: application/json

  {
      "amount": 50
  }
  ```

- **Example Response:**
  ```json
  {
      "user_id": "user123",
      "wallet": 150
  }
  ```

### Dashboard by Date
#### `GET /dashboard_date`
Fetches dashboard data grouped by date and status.

- **Response:**
  - `200 OK`: Returns the dashboard data grouped by date.

- **Example Request:**
  ```http
  GET /dashboard_date
  ```

- **Example Response:**
  ```json
  {
      "2024-08-07": {
          "Success": 10,
          "Failed": 2
      },
      "2024-08-06": {
          "Success": 8,
          "Failed": 1
      }
  }
  ```

### Delete App
#### `DELETE /delete_app`
Deletes a specified app for the client.

- **Request Body:**
  ```json
  {
      "app_id": "app123"
  }
  ```

- **Response:**
  - `200 OK`: Returns updated client apps details.

- **Example Request:**
  ```http
  DELETE /delete-app
  Content-Type: application/json

  {
      "app_id": "app123"
  }
  ```

- **Example Response:**
  ```json
  {
      "client_id": "client123",
      "apps": []
  }
  ```

### Get App
#### `POST /get-app`
Fetches details of a specific app by its ID.

- **Request Body:**
  ```json
  {
      "app_id": "app123"
  }
  ```

- **Response:**
  - `200 OK`: Returns app details.

- **Example Request:**
  ```http
  POST /get_app
  Content-Type: application/json

  {
      "app_id": "app123"
  }
  ```

- **Example Response:**
  ```json
  {
      "app_id": "app123",
      "name": "App Name",
      "status": "active"
  }
  ```

### Get Client Profile
#### `GET /get-client-profile/`
Fetches the profile of a specific client by their ID.

- **URL Parameters:**
  - `client_id`: The ID of the client.

- **Response:**
  - `200 OK`: Returns client profile details.

- **Example Request:**
  ```http
  GET /client_profile/client123
  ```

- **Example Response:**
  ```json
  {
      "client_id": "client123",
      "name": "Client Name",
      "email": "client@example.com"
  }
  ```