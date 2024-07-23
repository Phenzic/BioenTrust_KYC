# API Documentation

## Table of Content
- [Endpoints](#endpoints)
    - [Get all live api](#get-apiget_all_liveapiclient_id) 
    - [Get all snadbox api](#get-apiget_all_sandboxapiclient_id)
    - [Get live api](#get-apiget_live_api_logsapi_key)
    - [Get sandbox api](#get-apiget_sandbox_api_logsapi_key)
    - [Create live api key](#get-apicreate_live_key)
    - [Create Sandbox api key](#get-apicreate_sandbox_key)
    - [Delete live api key](#delete-apidelete_live_key)
    - [Delete Sandbox api key](#delete-apidelete_sandbox_key)


## Base URL

```
<base-url>/api
```

## Endpoints

### `GET /api/get_all_liveapi/<client_id>`

#### Description
Retrieves all live API keys associated with a given client ID.

#### Request
- Method: `GET`
- URL: `/api/get_all_liveapi/<client_id>`

#### Response
- **200 OK**

  ```json
  {
    "live_keys": [
        {
            "api_key": "live_api_key_1",
            "secret_key": "live_secret_key_1"
        },
        {
            "api_key": "live_api_key_2",
            "secret_key": "live_secret_key_2"
        }
    ]
  }
  ```

- **400 Bad Request**

  ```json
  {
    "message": "User has no generated API key"
  }
  ```



### `GET /api/get_all_sandboxapi/<client_id>`

#### Description
Retrieves all sandbox API keys associated with a given client ID.

#### Request
- Method: `GET`
- URL: `/api/get_all_sandboxapi/<client_id>`

#### Response
- **200 OK**

  ```json
  {
    "sandbox_keys": [
        {
            "api_key": "sandbox_api_key_1",
            "secret_key": "sandbox_secret_key_1"
        },
        {
            "api_key": "sandbox_api_key_2",
            "secret_key": "sandbox_secret_key_2"
        }
    ]
  }
  ```

- **400 Bad Request**

  ```json
  {
    "message": "User has no generated API key"
  }
  ```

### `GET /api/get_sandbox_api_logs/<api_key>`

#### Description
Retrieves logs for a given sandbox API key.

#### Request
- Method: `GET`
- URL: `/api/get_sandbox_api_logs/<api_key>`

#### Response
- **200 OK**

  ```json
  {
    "logs": [
        {
            "timestamp": "2024-01-01T12:00:00.000Z",
            "request": "GET /api/resource",
            "response": "200 OK"
        }
    ]
  }
  ```

- **403 Forbidden**

  ```json
  {
    "message": "Invalid API key, Use a Sandbox API key"
  }
  ```

- **404 Not Found**

  ```json
  {
    "message": "No logs found for this API key"
  }
  ```

### `GET /api/get_live_api_logs/<api_key>`

#### Description
Retrieves logs for a given live API key.

#### Request
- Method: `GET`
- URL: `/api/get_live_api_logs/<api_key>`

#### Response
- **200 OK**

  ```json
  {
    "logs": [
        {
            "timestamp": "2024-01-01T12:00:00.000Z",
            "request": "GET /api/resource",
            "response": "200 OK"
        }
    ]
  }
  ```

- **403 Forbidden**

  ```json
  {
    "message": "Invalid API key, Use a Live API key"
  }
  ```

- **404 Not Found**

  ```json
  {
    "message": "No logs found for this API key"
  }
  ```

### `GET /api/create_sandbox_key`

#### Description
Creates a new sandbox API key and secret key for a given user ID.

#### Request
- Method: `GET`
- URL: `/api/create_sandbox_key`
- Headers:
  - `Authorization: Bearer <JWT_TOKEN>`
- Body: JSON

  ```json
  {
    "user_id": "user123"
  }
  ```

#### Response
- **201 Created**

  ```json
  {
    "status": "Sandbox API key and secret key created and stored successfully",
    "api_key": "new_sandbox_api_key",
    "secret_key": "new_sandbox_secret_key"
  }
  ```

- **404 Not Found**

  ```json
  {
    "status": "User not found"
  }
  ```

### `GET /api/create_live_key`

#### Description
Creates a new live API key and secret key for a given user ID.

#### Request
- Method: `GET`
- URL: `/api/create_live_key`
- Headers:
  - `Authorization: Bearer <JWT_TOKEN>`
- Body: JSON

  ```json
  {
    "user_id": "user123"
  }
  ```

#### Response
- **201 Created**

  ```json
  {
    "status": "Live API key and secret key created and stored successfully",
    "api_key": "new_live_api_key",
    "secret_key": "new_live_secret_key"
  }
  ```

- **404 Not Found**

  ```json
  {
    "status": "User not found"
  }
  ```

### `DELETE /api/delete_sandbox_key`

#### Description
Deletes a sandbox API key and secret key for a given user ID.

#### Request
- Method: `DELETE`
- URL: `/api/delete_sandbox_key`
- Headers:
  - `Authorization: Bearer <JWT_TOKEN>`
- Body: JSON

  ```json
  {
    "user_id": "user123",
    "api_key": "sandbox_api_key",
    "secret_key": "sandbox_secret_key"
  }
  ```

#### Response
- **200 OK**

  ```json
  {
    "message": "API key and secret key deleted successfully"
  }
  ```

- **400 Bad Request**

  ```json
  {
    "message": "Key pair not found"
  }
  ```

- **404 Not Found**

  ```json
  {
    "message": "User not found"
  }
  ```

- **500 Internal Server Error**

  ```json
  {
    "message": "No keys were deleted"
  }
  ```

### `DELETE /api/delete_live_key`

#### Description
Deletes a live API key and secret key for a given user ID.

#### Request
- Method: `DELETE`
- URL: `/api/delete_live_key`
- Headers:
  - `Authorization: Bearer <JWT_TOKEN>`
- Body: JSON

  ```json
  {
    "user_id": "user123",
    "api_key": "live_api_key",
    "secret_key": "live_secret_key"
  }
  ```

#### Response
- **200 OK**

  ```json
  {
    "message": "API key and secret key deleted successfully"
  }
  ```

- **400 Bad Request**

  ```json
  {
    "message": "Key pair not found"
  }
  ```

- **404 Not Found**

  ```json
  {
    "message": "User not found"
  }
  ```

- **500 Internal Server Error**

  ```json
  {
    "message": "No keys were deleted"
  }
  ```