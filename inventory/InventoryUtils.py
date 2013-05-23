from users.models import UserProfile

#given a request get the restaurant name of the user
def get_rest(request):
    key = request.user.id
    prof = UserProfile.objects.get(user=key)
    rest = prof.restaurant
    return rest