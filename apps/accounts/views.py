from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.db import connection

# -------------------------
# Custom login_required decorator
# -------------------------
def login_required_custom(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get("user_id"):
            messages.error(request, "Please log in first.")
            return redirect("login")
        return view_func(request, *args, **kwargs)
    return wrapper


# -------------------------
# Login view
# -------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, username, password, is_staff FROM users WHERE username=%s",
                [username]
            )
            row = cursor.fetchone()

        if row and check_password(password, row[2]):
            user_id, username, _, is_staff = row
            request.session["user_id"] = user_id
            request.session["username"] = username
            request.session["is_staff"] = bool(is_staff)
            messages.success(request, f"Welcome back, {username}!")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")


# -------------------------
# Logout view
# -------------------------
def logout_view(request):
    request.session.flush()
    messages.success(request, "Logged out successfully.")
    return redirect("login")


# -------------------------
# Register view
# -------------------------
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE username=%s OR email=%s", [username, email])
            if cursor.fetchone():
                messages.error(request, "Username or email already exists.")
                return redirect("register")

            hashed_password = make_password(password)
            cursor.execute(
                "INSERT INTO users (username, email, password, first_name, last_name, is_active) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                [username, email, hashed_password, first_name, last_name, True]
            )

        messages.success(request, "Account created successfully! Please log in.")
        return redirect("login")

    return render(request, "accounts/register.html")


# -------------------------
# Dashboard view
# -------------------------
@login_required_custom
def dashboard(request):
    return redirect("index")


# -------------------------
# Profile view
# -------------------------
@login_required_custom
def account_profile(request):
    user_id = request.session.get("user_id")

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id, username, email, first_name, last_name, is_staff FROM users WHERE id=%s",
            [user_id]
        )
        row = cursor.fetchone()

    if not row:
        messages.error(request, "User not found.")
        return redirect("login")

    user_data = {
        "id": row[0],
        "username": row[1],
        "email": row[2],
        "first_name": row[3],
        "last_name": row[4],
        "is_staff": row[5],
    }

    return render(request, "accounts/profile.html", {"user": user_data})
