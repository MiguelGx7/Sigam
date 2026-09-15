from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def login_usuario(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        usuario = authenticate(
            request,
            username=username,
            password=password
        )

        if usuario is not None:
            login(request, usuario)

            return redirect("inicio")

        return render(
            request,
            "user/login.html",
            {
                "error": "Usuario o contraseña incorrectos."
            }
        )

    return render(
        request,
        "user/login.html"
    )


@login_required
def inicio(request):
    return render(
        request,
        "user/inicio.html"
    )


def logout_usuario(request):
    logout(request)

    return redirect("login")