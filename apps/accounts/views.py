# apps/accounts/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from supabase import create_client, Client
import os

# -------------------------
# Supabase client
# -------------------------
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------------
# Custom login_required decorator
# -------------------------
def login_required_custom(view_func):
    """Protect views for logged-in users."""
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

# -------------------------
# Login view
# -------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        response = supabase.table("users").select("*").eq("username", username).execute()
        user = response.data[0] if response.data else None

        if user and check_password(password, user['password']):
            request.session['user_id'] = user['id']
            request.session['username'] = user['username']
            request.session['is_staff'] = user.get('is_staff', False)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")

# -------------------------
# Logout view
# -------------------------
def logout_view(request):
    request.session.flush()
    messages.success(request, "You have successfully logged out.")
    return redirect('login')

# -------------------------
# Register / Signup view
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
            messages.error(request, "Passwords do not match")
            return redirect('register')

        # Check if username or email exists
        existing = supabase.table("users").select("*").or_(f"username.eq.{username},email.eq.{email}").execute()
        if existing.data:
            messages.error(request, "Username or email already exists")
            return redirect('register')

        hashed_password = make_password(password)
        supabase.table("users").insert({
            "username": username,
            "email": email,
            "password": hashed_password,
            "first_name": first_name,
            "last_name": last_name,
            "is_active": True
        }).execute()

        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')

    return render(request, "accounts/register.html")

# -------------------------
# Dashboard view
# -------------------------
@login_required_custom
def dashboard(request):
    
    return redirect( "index")

# -------------------------
# Profile view
# -------------------------
@login_required_custom
def account_profile(request):
    user_id = request.session.get("user_id")
    response = supabase.table("users").select("*").eq("id", user_id).execute()
    user_data = response.data[0] if response.data else None

    if not user_data:
        return redirect("login")

    context = {
        "user": user_data
    }
    return render(request, "accounts/profile.html", context)
