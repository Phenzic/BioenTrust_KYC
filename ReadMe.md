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

For detailed information about the user APIs, refer to the [User Documentation](./docs/signup_docs.md).

<!-- ## Encryption Requests

For detailed information about the encryption APIs, refer to the [Encryption Documentation](./docs/encryption_endpoints.md).

## Calendar Requests

For detailed information about the calender APIs, refer to the [Calender Documentation](./docs/calender_endpoints.md).


## Article API Documentation

For detailed information about the article APIs, refer to the [Article API Documentation](./docs/article_endpoints.md).

## Comment API Documentation

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


