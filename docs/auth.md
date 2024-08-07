# User API Documentation

## Table of Content
- [Endpoint](#endpoints)
  - [Home](#get-home)
  - [Protected](#get-protected)
  - [Signup](#post-signup)
  - [Verify Email](#post-verify_email)
  - [Signin](#post-signin)
  - [Verify SMS](#post-verify_sms)
  - [Signout](#delete-signout)
  - [Refresh](#get-refresh)
  - [Forgot Password](#post-forgot_password)
  - [Reset Password](#post-reset_password)

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
      "new_data": "Welcome to BioEntrust Auth server"
  }
  ```

- **500 Internal Server Error**

  ```json
  {
      "status": "error",
      "message": "Error message"
  }
  ```

### `GET /protected`

#### Description
Returns a protected message from the BioEntrust Auth server. Requires JWT authentication.

#### Request
- Method: `GET`
- URL: `user/protected`

#### Response
- **200 OK**

  ```json
  {
      "new_data": "Protected data"
  }
  ```

- **401 Unauthorized**

  ```json
  {
      "status": "error",
      "message": "Unauthorized"
  }
  ```

- **500 Internal Server Error**

  ```json
  {
      "status": "error",
      "message": "Error message"
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

### `POST /verify_sms`

#### Description
Verifies the user's phone number by checking the provided SMS OTP.

#### Request
- Method: `POST`
- URL: `/user/verify-sms`
- Body: JSON

  ```json
  {
      "app_id": 09876,
      "otp": "123456",
      "otp_request_id": "some_unique_id"
  }
  ```

#### Response
- **200 OK**

  ```json
  {
      "message": "Phone number verified"
  }
  ```

- **401 Unauthorized**

  ```json
  {
      "error": "Verification failed"
  }
  ```

### `DELETE /signout`

#### Description
Signs out the user by revoking the access and refresh tokens.

#### Request
- Method: `DELETE`
- URL: `/user/signout`
- Required Bearer Authentication (refresh-token)

#### Response
- **200 OK**

  ```json
  {
      "message": "Signed out successfully"
  }
  ```

### `GET /refresh`

#### Description
Refreshes the access token using the refresh token.

#### Request
- Method: `GET`
- URL: `/user/refresh`
- Requires Bearer Authentication (refresh-token)

#### Response
- **200 OK**

  ```json
  {
    "token":
    {
      "access": "yada-yada-yada-yada-yada-yada-yada-yada-yada-yada-"
    }
  }
  ```

### `POST /forgot-password`

#### Description
Sends a password reset link to the user's email.

#### Request
- Method: `POST`
- URL: `/user/forgot-password`
- Body: JSON

  ```json
  {
      "email": "john.doe@example.com",
      "password": "1234567890"
  }
  ```

#### Response
- **200 OK**

  ```json
  {
      "message": "Password reset link sent"
  }
  ```

### `POST /reset-password`

#### Description
Resets the user's password using the provided token.

#### Request
- Method: `POST`
- URL: `/auth/reset-password`
- Body: JSON
- Requires Bearer Authentication (access-token)

  ```json
  {
      "email": "example@gmail.com",
      "password": "newpassword123"
  }
  ```

#### Response
- **200 OK**

  ```json
  {
      "message": "Password reset successfully"
  }
  ```

- **400 Bad Request**

  ```json
  {
      "error": "Invalid token or password"
  }
  ```