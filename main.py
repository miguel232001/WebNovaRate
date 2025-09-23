from flask import Flask, render_template, request, flash, redirect, url_for, session
from model import RequestModel
from service import ApiService
from service.ApiService import APIService

app = Flask(__name__)

@app.route("/")
def main_page():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]

        if not usuario or not password:
            flash("No puede haber campos vacíos", "error")
        else:
            # Construir la ruta como en MAUI
            ruta = f"http://localhost:8080/usuarios/login/usuario/{usuario}/contrasena/{password}"

            req = RequestModel(
                method="Post",
                route=ruta,
                data=None
            )

            response = APIService.execute_request(req)

            if response.success == 0:
                # Login correcto → guardar usuario en sesión
                session["usuario"] = usuario
                flash("Login correcto ✅", "success")

                # Ahora verificamos si la cuenta está activada (igual que en MAUI)
                ruta_activacion = f"http://localhost:8080/usuarios/activacion/{usuario}"
                req_activacion = RequestModel("Post", ruta_activacion, None)
                response_activacion = APIService.execute_request(req_activacion)

                if response_activacion.success == 0:
                    flash("Cuenta activada ✅", "success")
                    return redirect(url_for("menu"))
                else:
                    flash("Cuenta desactivada ⚠️, activa primero", "warning")
                    return redirect(url_for("codigo"))

            else:
                flash("Usuario o contraseña incorrectos ❌", "error")

    return render_template("login.html")
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        usuario = request.form["usuario"]
        correo = request.form["correo"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if not usuario or not correo or not password or not confirm_password:
            flash("No puede haber campos vacíos", "error")
        elif password != confirm_password:
            flash("Las contraseñas no coinciden", "error")
        else:
            # Construir el DTO como en MAUI
            usuario_dto = {
                "nombre": usuario,
                "email": correo,
                "contraseña": password
            }

            # Crear el request
            req = RequestModel(
                method="Post",
                route="http://localhost:8080/usuarios/registrar",
                data=usuario_dto
            )

            # Ejecutar la petición
            response = ApiService.execute_request(req)

            if response.success == 0:
                flash("Usuario registrado correctamente ✅", "success")
                return redirect(url_for("login"))
            elif response.success == 1:
                flash("El nombre de usuario ya existe", "error")
            elif response.success == 2:
                flash("El correo ya está en uso", "error")
            else:
                flash("Error al registrar usuario: " + response.message, "error")

    return render_template("registro.html")

@app.route("/activar/<usuario>", methods=["GET", "POST"])
def activar(usuario):
    if request.method == "POST":
        codigo = request.form["codigo"]

        if not codigo:
            flash("No puede haber campos vacíos", "error")
            return redirect(url_for("activar", usuario=usuario))

        # Simulación de RequestModel -> aquí llamas a tu API de Java
        url = f"http://localhost:8080/usuarios/comprobarCodigo/correo/{usuario}/codigo/{codigo}"
        response = request.post(url)

        if response.status_code == 200 and response.json().get("success") == 0:
            flash("✅ Código correcto, cuenta activada", "success")
            return redirect(url_for("login"))
        else:
            flash("❌ Código incorrecto", "error")

    return render_template("codigo_activacion.html", usuario=usuario)
if __name__ == "__main__":
    app.run(debug=True)
