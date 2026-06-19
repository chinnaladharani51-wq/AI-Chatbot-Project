from flask import Flask, render_template, request, redirect, url_for
import requests
<<<<<<< HEAD
import os

app = Flask(__name__)

# Get API Key from Environment Variable
API_KEY = os.getenv("OPENROUTER_API_KEY")

=======

app = Flask(__name__)

API_KEY = ""
>>>>>>> 67799a718a9c3eed6eccb5276da580dc25d936f9

# =========================
# REGISTER
# =========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        with open("users.txt", "a") as file:
            file.write(f"{username},{password}\n")

        return redirect(url_for("login"))

    return render_template("register.html")


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        try:
            with open("users.txt", "r") as file:

                for line in file:

                    user, pwd = line.strip().split(",")

                    if username == user and password == pwd:
<<<<<<< HEAD
=======

>>>>>>> 67799a718a9c3eed6eccb5276da580dc25d936f9
                        return redirect(url_for("home"))

        except:
            pass

        return "Invalid Username or Password"

    return render_template("login.html")


# =========================
# CHATBOT HOME
# =========================

@app.route("/", methods=["GET", "POST"])
def home():

    reply = ""
    history = ""

    if request.method == "POST":

        message = request.form.get("message")
        language = request.form.get("language", "English")

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": f"Answer in {language}: {message}"
                }
            ]
        }

        try:

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data
            )

            result = response.json()

            if "choices" in result:
<<<<<<< HEAD
                reply = result["choices"][0]["message"]["content"]
            else:
                reply = str(result)

            with open("chat_history.txt", "a", encoding="utf-8") as file:
=======

                reply = result["choices"][0]["message"]["content"]

            else:

                reply = str(result)

            with open("chat_history.txt", "a", encoding="utf-8") as file:

>>>>>>> 67799a718a9c3eed6eccb5276da580dc25d936f9
                file.write(f"👤 User: {message}\n")
                file.write(f"🤖 AI: {reply}\n\n")

        except Exception as e:
<<<<<<< HEAD
            reply = str(e)

    try:
        with open("chat_history.txt", "r", encoding="utf-8") as file:
            history = file.read()

    except:
=======

            reply = str(e)

    try:

        with open("chat_history.txt", "r", encoding="utf-8") as file:

            history = file.read()

    except:

>>>>>>> 67799a718a9c3eed6eccb5276da580dc25d936f9
        history = ""

    return render_template(
        "index.html",
        reply=reply,
        history=history
    )


if __name__ == "__main__":
    app.run(debug=True)
