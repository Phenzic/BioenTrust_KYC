# User API Documentation

## Table of Content
- [Endpoint](#endpoints)
  - [Home](#get-home)
  - [Signup](#post-signup)
  - [Verify Email](#post-verify_email)
  - [Signin](#post-signin)

## Base URL

```
<base-url>/user
```

## Endpoints

### `GET /home`

#### Description
Returns a welcome message from the BioEntrust Auth server.

#### Request
- Method: `GET`
- URL: `user/home`

#### Response
- **200 OK**

  ```json
  {
      "message": "Welcome to BioEntrust Auth server"
  }
  ```

### `POST /signup`

#### Description
Registers a new user and sends an OTP to the provided email for verification.

#### Request
- Method: `POST`
- URL: `/user/signup`
- Body: JSON

  ```json
  {
      "first_name": "John",
      "last_name": "Doe",
      "email": "john.doe@example.com",
      "password": "password123"
  }
  ```

#### Response
- **200 OK**

  ```json
  {
      "otp_request_id": "some_unique_id",
      "response": "otp sent"
  }
  ```

- **400 Bad Request**

  ```json
  {
      "error": "Password should be more than 7 characters"
  }
  ```

- **409 Conflict**

  ```json
  {
      "error": "Email address already in use"
  }
  ```

### `POST /verify_email`

#### Description
Verifies the user's email by checking the provided OTP.

#### Request
- Method: `POST`
- URL: `/user/verify-email`
- Body: JSON

  ```json
  {
      "otp": "123456",
      "otp_request_id": "some_unique_id"
  }
  ```

#### Response
- **200 OK**

  ```json
  {
      "message": "Logged In",
      "token": {
          "access": "access_token",
          "refresh": "refresh_token"
      }
  }
  ```

- **401 Unauthorized**

  ```json
  {
      "error": "Signup Failed"
  }
  ```

### `POST /signin`

#### Description
Authenticates a user and returns an access token and a refresh token.

#### Request
- Method: `POST`
- URL: `/user/signin`
- Body: JSON

  ```json
  {
      "email": "john.doe@example.com",
      "password": "password123"
  }
  ```

#### Response
- **200 OK**

  ```json
  {
      "message": "Logged In",
      "token": {
          "access": "access_token",
          "refresh": "refresh_token"
      }
  }
  ```

- **401 Unauthorized**

  ```json
  {
      "error": "Invalid login credentials"
  }
  ```