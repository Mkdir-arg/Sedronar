def user_groups(request):
    """Context processor para pasar los grupos del usuario al template"""
    if request.user.is_authenticated:
        groups = list(request.user.groups.values_list('name', flat=True))
        return {
            'user_groups_list': groups,
            'user_groups_json': str(groups).replace("'", '"')
        }
    return {
        'user_groups_list': [],
        'user_groups_json': '[]'
    }