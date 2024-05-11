from .models import UserInfo
from django.shortcuts import get_object_or_404
from allauth.socialaccount.models import SocialAccount
import os
def userinfo(request):
    userinfo = None
    key = os.environ.get('GGMAP_API_KEY')
    if request.user.is_authenticated:
        checkusersocailregisters=UserInfo.objects.filter(id=request.user.id)
        if checkusersocailregisters.exists() is False:
            social_accounts = SocialAccount.objects.filter(user=request.user)
            google_account = social_accounts.filter(provider='google').first()
            if google_account:
                google_given_name = google_account.extra_data.get('given_name', None)
                google_family_name = google_account.extra_data.get('family_name', None)
                newuser=UserInfo(id=request.user.id)
                newuser.firstname=google_given_name
                newuser.lastname=google_family_name
                newuser.avatar='avatar_test.jpg'
                newuser.save()
        userinfo = get_object_or_404(UserInfo, id=request.user.id)
    return {'userinfo': userinfo, 'key': key}
