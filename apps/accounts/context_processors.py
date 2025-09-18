from django.db import connection

def user_context(request):
    """
    Makes logged-in user info available in all templates.
    """
    user_data = None

    user_id = request.session.get("user_id")
    if user_id:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, username, email, first_name, last_name, date_joined
                FROM users WHERE id = %s
            """, [user_id])
            row = cursor.fetchone()
            if row:
                user_data = {
                    "id": row[0],
                    "username": row[1],
                    "email": row[2],
                    "first_name": row[3],
                    "last_name": row[4],
                    "date_joined": row[5],
                }

    return {"current_user": user_data}
