from flask import Flask, render_template, redirect, url_for, request, session, jsonify
import random
import os
import threading
import requests
import json

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Store OTP for demo purposes
otp_storage = {}
FILE_FOLDER = "/home/elfie/LightControllerCTFChallenge/jsonPics/"  # Replace with your actual folder path
bannedWords = ["nc","python","bash","base64","<<<","<<", "&&","&","|","||"," ","/"]  # Example banned words
#"pixel_art.json;cat${IFS}${PATH:0:1}home${PATH:0:1}elfie${PATH:0:1}.ssh${PATH:0:1}id_rsa" solution 


def contains_banned_words(text, banned_words):
    """
    Check if a string contains any word from a list of banned words.
    """
    for word in banned_words:
        if word in text:
            print(word)
            return True
    return False


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/robots.txt")
def robots():
    return """
    User-agent: *
    Disallow: /login
    # Flag: XMAS{Secret_Flag_Here}
    """


@app.route("/login", methods=["POST", "GET"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    otp = request.form.get("otp")

    if username == "admin" and password == "xmas2024":
        if otp == otp_storage.get(username):
            session["logged_in"] = True
            return redirect(url_for("tree_control"))
        else:
            return "Invalid OTP", 403
    return render_template("login.html")


@app.route("/generate_otp", methods=["POST"])
def generate_otp():
    data = request.get_json()  # Accept JSON data instead of form data
    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "xmas2024":
        otp = str(random.randint(100000, 999999))  # Generate a 6-digit OTP
        otp_storage[username] = otp  # Store OTP temporarily
        return jsonify({"otp": otp})  # Send OTP to client for testing

    return jsonify({"error": "Invalid credentials"}), 401


@app.route("/tree_control")
def tree_control():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("tree_control.html")


@app.route("/get_files", methods=["GET"])
def get_files():
    """Fetch the list of files in the directory."""
    if not session.get("logged_in"):
        return "Unauthorized", 401

    try:
        files = os.listdir(FILE_FOLDER)
        return jsonify({"files": files})
    except Exception as e:
        return str(e), 500


def execute_command_in_thread(filepath, output):
    """Threaded function to execute the ommand."""
    try:
        temp_output_file = "/tmp/output.txt"
        command = f"cat /home/elfie/LightControllerCTFChallenge/jsonPics/" + filepath + " > " + temp_output_file
        print(command)
        os.system(command)

        # Read the redirected output
        with open(temp_output_file, "r") as f:
            content = f.read()

        output["content"] = content
    except Exception as e:
        output["error"] = str(e)

@app.route("/send_to_external", methods=["POST"])
def send_to_external():
    """
    Reads the content of the selected file, parses it as JSON, and sends it as a POST request
    to the external server at http://192.168.3.9:5000/external_post.
    """
    data = request.get_json()
    if not data or "filepath" not in data:
        return "Invalid request: 'filepath' is required", 400

    filepath = data["filepath"]
    print(f"Preparing to send file: {filepath}")

    try:
        # Read the content of the file
        full_path = os.path.join(FILE_FOLDER, filepath)
        if not os.path.exists(full_path):
            return "File not found", 404

        with open(full_path, "r") as file:
            file_content = file.read()

        # Parse the file content as JSON
        try:
            parsed_content = json.loads(file_content)
        except json.JSONDecodeError:
            return "File content is not valid JSON", 400

        # Send the parsed content to the external server
        external_url = "http://192.168.3.3:5000/external_post"
        payload = {"content": parsed_content}
        print(f"Sending parsed content to {external_url}")

        # Perform the POST request
        response = requests.post(external_url, json=payload)
        response.raise_for_status()

        return jsonify({"message": f"Content of '{filepath}' sent successfully.", "status": response.status_code})
    except requests.RequestException as e:
        return f"Failed to send content to the external server: {e}", 500
    except Exception as e:
        return str(e), 500


@app.route("/run_command", methods=["POST"])
def run_command():
    """Run a command on the given file."""
    if not session.get("logged_in"):
        return "Unauthorized", 401

    data = request.get_json()
    if not data or "filepath" not in data:
        return "Invalid request: 'filepath' is required", 400

    # Get the file path from the POST request
    filepath = data["filepath"]
    print(filepath)

    # Ensure the file path does not contain banned words
    if contains_banned_words(filepath, bannedWords):
        return "Do not be naughty!", 401

    # Use threading to execute the command
    output = {}
    thread = threading.Thread(target=execute_command_in_thread, args=(filepath, output))
    thread.start()
    thread.join()

    # Return the output or an error
    if "error" in output:
        return output["error"], 500
    return jsonify({"output": output["content"]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
