### README.md


# Flask Application for File Management and External Posting

This Flask application provides functionality for managing files in a specific directory, validating user input, and sending file content to an external server. It includes features like user authentication with OTP, file listing, file content display, and sending JSON content to a specified endpoint.

## Features

- **User Authentication**:
  - Secure login with username, password, and OTP.
  - OTP generation for testing purposes.

- **File Management**:
  - List files in a specific directory.
  - Display file content on the frontend.
  - Send file content as JSON to an external server.

- **Validation**:
  - Protects against specific banned keywords in file paths.

## Prerequisites

- Python 3.x installed on your machine.
- Flask framework and additional dependencies installed (see `requirements.txt`).

## Installation

1. Clone the repository or copy the files into your project directory.

2. Navigate to the project directory.

3. Install the required dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```

4. Modify the `FILE_FOLDER` variable in the code to point to the directory containing your files:
   ```python
   FILE_FOLDER = "/path/to/your/files"
   ```

## Usage

1. **Run the Application**:
   Start the Flask application with:
   ```bash
   python app.py
   ```

   The application will run on `http://0.0.0.0:5000`.

2. **Access the Application**:
   Open a web browser and navigate to `http://localhost:5000`.

3. **Login**:
   Use the following credentials:
   - Username: `admin`
   - Password: `HAHAHAHADIDYOUREALLYILLADDAPASWORDHERE?!`

   Generate an OTP by sending a POST request to `/generate_otp`:
   ```bash
   curl -X POST http://localhost:5000/generate_otp -H "Content-Type: application/json" -d '{"username":"admin", "password":"HAHAHAHADIDYOUREALLYILLADDAPASWORDHERE?!"}'
   ```

4. **View Files**:
   After logging in, view the files in the directory through the web interface.

5. **Send File Content to an External Server**:
   Select a file and send its content as JSON to the external server endpoint.

## API Endpoints

### 1. `/`
- **Method**: GET
- **Description**: Home page.

### 2. `/login`
- **Method**: GET, POST
- **Description**: Login page.

### 3. `/generate_otp`
- **Method**: POST
- **Description**: Generate an OTP for login.
- **Request Body**:
  ```json
  {
    "username": "admin",
    "password": "HAHAHAHADIDYOUREALLYILLADDAPASWORDHERE?!"
  }
  ```

### 4. `/tree_control`
- **Method**: GET
- **Description**: Main file management page.

### 5. `/get_files`
- **Method**: GET
- **Description**: List files in the specified directory.

### 6. `/run_command`
- **Method**: POST
- **Description**: Execute a command on the selected file.
- **Request Body**:
  ```json
  {
    "filepath": "example.json"
  }
  ```

### 7. `/send_to_external`
- **Method**: POST
- **Description**: Send the JSON content of the selected file to an external server.
- **Request Body**:
  ```json
  {
    "filepath": "example.json"
  }
  ```

## Security Considerations

- The application performs basic validation to avoid harmful commands via `bannedWords`.
- **Do not expose this application to the public internet without proper security hardening.**

## License

This project is open source and available under the [MIT License](LICENSE).
