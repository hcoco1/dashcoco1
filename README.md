# High School Students' Grades Dashboard

This project creates an interactive dashboard to visualize and analyze the grades of high school students over time. The dashboard is built using Python, Dash, and Plotly, with Bootstrap for styling.

## Features

- **Student Selection**: Choose a student from a dropdown to view their grades.
- **Year Selection**: Filter grades by academic year.
- **Subject Performance**: View performance in different subjects.
- **Grade Average**: See the average grade for each student.
- **Detailed Exam Scores**: Examine scores for individual exams.
- **Performance Over Time**: Visualize performance trends across multiple exams.

## Installation

Ensure you have Python 3 and `pip` installed. Follow these steps to set up your environment:

1. **Clone the repository:**
    ```sh
    git clone https://github.com/hcoco1/Dashboard-Plothy-Dash.git
    cd Dashboard-Plothy-Dash
    ```

2. **Set up a virtual environment:**
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

## Running the App

1. **Navigate to the source directory:**
    ```sh
    cd hcoco1/src
    ```

2. **Run the application:**
    ```sh
    python3 app.py
    ```

3. **Access the dashboard:**
   Open your web browser and go to `http://127.0.0.1:8050/`.

## Application Structure

```sh
.
├── Procfile
├── README.md
├── requirements.txt
├── runtime.txt
└── src
    ├── app.py
    └── __init__.py

1 directory, 6 files
```

## Authentication

### Dash Enterprise Auth

"The `BasicAuth` method shown in the provided Python code snippet is not secure and should only be used for very basic purposes or in development environments. 

```python
auth = dash_auth.BasicAuth(
    app,
    {'bugsbunny': 'topsecret'}
)
```

This method employs basic HTTP authentication, where the username (`bugsbunny`) and password (`topsecret`) are transmitted with each request in an easily decodable format. Here are the key points to consider:

1. **Lack of Encryption**: BasicAuth does not encrypt credentials, making them vulnerable to interception and unauthorized access if transmitted over an unsecured connection (HTTP).

2. **Single Point of Failure**: Using a single set of credentials for access means that if those credentials are compromised, the entire application is exposed to potential misuse.

3. **Inadequate for Sensitive Data**: This authentication method is insufficient for applications handling sensitive or personal information, as it does not provide the security measures necessary to protect such data.

4. **Limited User Management**: There is no facility for managing multiple users or permissions, making it impractical for applications that require role-based access control or individualized user accounts.

5. **Development-Only Use**: BasicAuth is suitable for development or simple use cases where security is not a primary concern, such as internal tools or testing environments. For production applications, more robust authentication methods, such as OAuth, JWT, or multi-factor authentication (MFA), should be implemented.

In summary, while `BasicAuth` offers a straightforward and easy-to-implement solution for basic authentication needs, its inherent security weaknesses make it inappropriate for any application requiring strong security measures."  (ChatGPT 4o. 5/28/2024)


### Dash Docs

https://dash.plotly.com/authentication

### GitHub Plotly

https://github.com/plotly/dash-auth
