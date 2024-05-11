from .models import UserInfo
from django.shortcuts import get_object_or_404
import os
def userinfo(request):
    userinfo = None
    key = os.environ.get('GGMAP_API_KEY')
    if request.user.is_authenticated:
        userinfo = get_object_or_404(UserInfo, id=request.user.id)
    return {'userinfo': userinfo, 'key': key}
