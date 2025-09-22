from django.shortcuts import render
from django.db import connection

def index(request):
    total_users = 0

    # Get the total number of users from the custom table
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM users")
        row = cursor.fetchone()
        if row:
            total_users = row[0]

    # Pass the count to the template
    context = {
        "total_users": total_users
    }

    return render(request, 'pages/index.html', context)
