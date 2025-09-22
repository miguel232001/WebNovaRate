from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)

@app.route("/")
def main_page():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        usuario = request.form["usuario"]
        correo = request.form["correo"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Validaciones simples (como en tu ViewModel)
        if not usuario or not correo or not password or not confirm_password:
            flash("No puede haber campos vacíos", "error")
        elif password != confirm_password:
            flash("Las contraseñas no coinciden", "error")
        else:
            # Aquí iría la lógica de guardarlo en tu backend o BD
            flash("Usuario registrado correctamente ✅", "success")
            return redirect(url_for("login"))

    return render_template("registro.html")


if __name__ == "__main__":
    app.run(debug=True)
