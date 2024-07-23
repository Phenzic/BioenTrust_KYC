# Create App API Documentation

## Table of Contents
- [Endpoints](#endpoints)
  - [Create App](#post-apicreate_app)

## Base URL

```
<base-url>/app
```

## Endpoints

### `POST /app/create_app`

#### Description
Creates a new app for the authenticated user and adds it to the user's `apps` array.

#### Request
- Method: `POST`
- URL: `/api/create_app`
- Headers:
  - `Authorization: Bearer <JWT_TOKEN>`
- Body: JSON

  ```json
  {
      "name": "App Name",
      "color": "#F89500",
      "date_of_creation": "2024-01-29T17:53:42.000+00:00",
      "verification": true,
      "user_information": true,
      "on_verification": false,
      "redirect_url": "https://example.com"
  }
  ```

#### Response
- **201 Created**

  ```json
  {
      "status": "App added successfully",
      "app_id": "c407230de2da4c5fa30a6898b787b24a"
  }
  ```

- **400 Bad Request**

  ```json
  {
      "error": "Missing required field: <field_name>"
  }
  ```

- **404 Not Found**

  ```json
  {
      "error": "User not found"
  }
  ```

- **500 Internal Server Error**

  ```json
  {
      "error": "Failed to add app to user"
  }
  ```
