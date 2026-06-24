from flask import Flask, render_template, request, redirect, url_for, session
import requests
import os

app = Flask(__name__)
app.secret_key = "chatbot_secret_key"


# ==========================
# REGISTER
# ==========================
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        try:
            with open("users.txt", "r") as file:

                for line in file:

                    line = line.strip()

                    if not line:
                        continue

                    parts = line.split(",")

                    if len(parts) != 2:
                        continue

                    user, pwd = parts

                    if user == username:
                        return "Username already exists!"

        except FileNotFoundError:
            pass

        with open("users.txt", "a") as file:
            file.write(f"{username},{password}\n")

        print("Saved:", username, password)

        return redirect(url_for("login"))

    return render_template("register.html")


# ==========================
# LOGIN
# ==========================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        try:
            with open("users.txt", "r") as file:

                for line in file:

                    line = line.strip()

                    if not line:
                        continue

                    parts = line.split(",")

                    if len(parts) != 2:
                        continue

                    user, pwd = parts

                    if username == user and password == pwd:

                        session["user"] = username
                        return redirect(url_for("home"))

        except FileNotFoundError:
            pass

        return "Invalid Username or Password"

    return render_template("login.html")


# ==========================
# LOGOUT
# ==========================
@app.route("/logout")
def logout():

    session.clear()
    return redirect(url_for("login"))


# ==========================
# HOME
# ==========================
@app.route("/", methods=["GET", "POST"])
def home():

    if "user" not in session:
        return redirect(url_for("login"))

    username = session["user"]

    history_file = f"history_{username}.txt"

    reply = ""
    history = ""

    if request.method == "POST":

        message = request.form.get("message")
        language = request.form.get("language", "English")

        api_key = request.form.get("api_key")

        if not api_key:

            reply = "Please enter your OpenRouter API Key."

        else:

            headers = {
                "Authorization": f"Bearer {api_key}",
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

                    reply = result["choices"][0]["message"]["content"]

                else:

                    reply = str(result)

                with open(history_file, "a", encoding="utf-8") as file:

                    file.write(f"👤 {message}\n")
                    file.write(f"🤖 {reply}\n\n")

            except Exception as e:

                reply = str(e)

    try:

        with open(history_file, "r", encoding="utf-8") as file:
            history = file.read()

    except FileNotFoundError:
        history = ""

    return render_template(
        "index.html",
        username=username,
        reply=reply,
        history=history
    )


if __name__ == "__main__":
    app.run(debug=True)
