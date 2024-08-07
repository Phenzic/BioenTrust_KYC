# BioEntrust Server Requests

## Table of Contents

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Contribution](#contribution)
4. [Endpoints](#endpoints)
   - [GET](#get)

- [License](#license)

**_Note: development server url: https://auth-teg6.onrender.com**

## Installation

## Docker

1. Pull from Docker hub:
```
docker pull phenzic/bioentrust_e-verification:v1.0
```

2. Run the project:
```
docker-compose run
```

## Github
1. Clone the repository:

   ```bash
   git clone git@github.com:E-Verification/Auth.git master
   cd Auth
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Start the server:

   ```bash
   flask run
   ```

## Configuration

Configuration settings can be adjusted in the `/config` dir. Make sure to set the appropriate values for your environment.

## Contribution

1. Create a new branch:

   ```bash
   git checkout -b your-branch-name
   ```

2. Format the code:

   ```bash
   autopep8 --in-place --aggressive --aggressive --recursive . --exclude venv
   ```
   or use `black .`

3. Add your changes:

   ```bash
   git add .
   ```

4. Commit your changes:

   ```bash
   git commit -m "<commit-message>"
   ```

5. Push to the newly created branch and open a pull request to the master branch:

   ```bash
   git push origin your-branch-name
   ```

## Endpoints

### GET

**Description**: Welcome message and documentation link.

**Response**:

```json
{
  "message": "Welcome to BioEntrust Server",
  "docs": "https://docs.BioEntrust.com"
}
```

## User Requests

For detailed information about the User APIs, refer to the [User Documentation](./docs/auth.md).

 ## API Requests

For detailed information about the API-Key APIs, refer to the [API Documentation](./docs/api_docs.md).

## APP Requests

For detailed information about the App APIs, refer to the [APP Documentation](./docs/app_docs.md).


## Client Admin Documentation

For detailed information about the Client Admin APIs, refer to the [Client Admin Documentation](./docs/client_docs.md).

<!-- ## Comment API Documentation

For detailed information about the comment APIs, refer to the [Comment API Documentation](./docs/comments_endpoints.md).

## User Profile API Documentation

For detailed information about the user profile APIs, refer to the [User Profile API Documentation](./docs/community_endpoints.md).

## Community API Documentation

For detailed information about the Community APIs, refer to the [Community API Documentation](./docs/community_endpoints.md). -->

<!-- ## Data API Documentation

For detailed information about the Data APIs, refer to the [Data API Documentation](./docs/data_endpoints.md).

## Beta Test Feedback API Documentation

For detailed information about the beta testing feedback APIs, refer to the [Beta Test Feedback API Documentation](./docs/feedback_endpoints.md). -->

## License

This project is licensed under the MIT License - see the [LICENSE](/LICENSE) file for details.


