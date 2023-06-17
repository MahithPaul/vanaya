def add_user_to_context(request):
    user = request.user
    return {'current_user': user}
