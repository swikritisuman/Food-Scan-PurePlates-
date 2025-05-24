from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd

app = Flask(__name__)

df = pd.read_csv("PurePlates.csv")
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

@app.route("/")
def logo():
    return render_template("logo.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # You can add real auth logic here
        return redirect(url_for("dashboard"))
    return render_template("login.html")

# **Add this signup route below:**
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        fullname = request.form.get("fullname")
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        # TODO: Save user data logic here
        return redirect(url_for("dashboard"))
    return render_template("signup.html")

@app.route("/dashboard")
def dashboard():
    return render_template("result.html")

@app.route("/api/search", methods=["POST"])
def search():
    query = request.get_json().get("query", "").lower()
    results = []

    for _, row in df.iterrows():
        if any(query in str(row[col]).lower() for col in df.columns):
            results.append({
                "food": row.get("food_product", ""),
                "ingredients": row.get("main_ingredient", ""),
                "allergens": row.get("allergic_ingredients", ""),
                "allergy_type": row.get("associated_allergies", ""),
                "symptoms": row.get("symptoms", "")
            })

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
