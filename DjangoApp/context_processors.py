from .models import UserInfo
from django.shortcuts import get_object_or_404

def userinfo(request):
    userinfo = None
    with open("ggmap_api_key","r") as file:
        key=file.read()
    if request.user.is_authenticated:
        userinfo = get_object_or_404(UserInfo, id=request.user.id)
    return {'userinfo': userinfo, 'key': key}
