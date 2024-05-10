from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomPasswordResetForm
from .forms import CustomSetPasswordForm,CustomSetPasswordChange
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView 
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView
from DjangoApp.models import *
from openai import OpenAI
import os,json
from django.http import JsonResponse,HttpResponseBadRequest
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.timezone import localtime
from allauth.socialaccount.models import SocialAccount

    
    
class CustomPasswordResetView(PasswordResetView):
    template_name = 'Forget_password.html'
    success_url='done'
    form_class = CustomPasswordResetForm
    html_email_template_name='custom_password_reset_email.html'
    
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name= 'Password_Reset_Done.html'    
    
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name= 'Password_Reset_Complete.html'    

class CustomPasswordConfirmView(PasswordResetConfirmView):
    template_name= 'Password_Reset_Confirm.html' 
    form_class= CustomSetPasswordForm   
    success_url='done'
    
def index(request):
    if request.user.is_authenticated:
        return redirect('/usr/{}/'.format(request.user.id))
    top_posts = Post.objects.order_by('-star')[:2]  # Lấy 2 bài đăng có star lớn nhất
    other_posts = Post.objects.exclude(pk__in=[post.pk for post in top_posts])  # Lấy các bài đăng không thuộc top_posts
    if request.method == 'POST':
        if 'button-login' in request.POST:
            email = request.POST.get('input-login-account')
            password = request.POST.get('input-login-password')
            user = authenticate(request, username=email,email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/usr/{}/'.format(request.user.id))
            else:
                return render(request, "index.html", {'error_message_login': 'Invalid email or password','top_posts': top_posts, 'other_posts': other_posts})
        elif 'button-reg' in request.POST:
            email = request.POST.get('input-reg-account')
            password = request.POST.get('input-reg-password')
            try:
                validate_password(password)
            except ValidationError as e:
                return render(request,"index.html",{'error_message_reg_2': 'Your password is invalid', 'reg_check': True,'top_posts': top_posts, 'other_posts': other_posts})
            confirm_password = request.POST.get('input-reg-repassword')
            if User.objects.filter(username=email).exists():
                return render(request,"index.html",{'error_message_reg_1': 'Your email is exists', 'reg_check': True,'top_posts': top_posts, 'other_posts': other_posts})
            elif password != confirm_password:
                return render(request, 'index.html', {'error_message_reg': 'Passwords do not match', 'reg_check': True,'top_posts': top_posts, 'other_posts': other_posts})
            else: 
                user = User.objects.create_user(username=email,email=email, password=password)
                user.save()
                login(request,user)
                newuserinfo=UserInfo(id=request.user.id)
                newuserinfo.avatar='avatar_test.jpg'
                newuserinfo.save()
                return redirect('/usr/{}/'.format(request.user.id))
    else:
        return render(request, 'index.html', {'top_posts': top_posts, 'other_posts': other_posts} )
@login_required
def logoutPage(request):
    logout(request)
    return redirect('index')

@login_required
def whilelogin(request, user_id):
    checkusersocailregisters=UserInfo.objects.filter(id=request.user.id)
    if checkusersocailregisters.exists() is True:
        social_accounts = SocialAccount.objects.filter(user=request.user)
        google_account = social_accounts.filter(provider='google').first()
        if google_account:
            google_given_name = google_account.extra_data.get('given_name', None)
            google_family_name = google_account.extra_data.get('family_name', None)
            google_picture=google_account.extra_data.get('picture', None)
            newuser=UserInfo.objects.create()
            newuser.firstname=google_given_name
            newuser.lastname=google_family_name
            newuser.avatar=google_picture
            newuser.save()
    if request.user.id==user_id:
        userinfo=get_object_or_404(UserInfo,id=user_id)
        ListHistorychat=HistoryChat.objects.filter(iduser=userinfo)
        top_posts = Post.objects.order_by('-star')[:2]  # Lấy 2 bài đăng có star lớn nhất
        other_posts = Post.objects.exclude(pk__in=[post.pk for post in top_posts])  # Lấy các bài đăng không thuộc top_posts
        form = PostForm()
        if request.method == 'POST' and 'dangbai' in request.POST:
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save()
                return redirect('/post/{}/'.format(post.id))
        return render(request,'index_login.html', {'form': form,'top_posts': top_posts, 'other_posts': other_posts, 'userinfo': userinfo,'ListHistorychat': ListHistorychat})
    else:
        if request.user.is_authenticated:
            return redirect('/usr/{}/'.format(request.user.id))
        else:
            return redirect('index')
    
@login_required
def changepass(request, user_id):
    if request.user.id == user_id and request.user.is_authenticated:
        if request.method == 'POST' and "changepass-btn" in request.POST:
            formchangepass = CustomSetPasswordChange(data=request.POST, user=request.user)
            if formchangepass.is_valid():
                formchangepass.save()
                return redirect('/usr/{}/changepass/done'.format(request.user.id))
            else:
                return render(request, 'passwordchange.html', {'formchangepass': formchangepass})
        else:
            formchangepass = CustomSetPasswordChange(user=request.user)
            return render(request, 'passwordchange.html', {'formchangepass': formchangepass})
    return redirect('index')
@login_required
def changepassdone(request,user_id):
    return redirect('/usr/{}/'.format(request,user_id))
def search(request):
    searched = ""
    keys = []
    user = request.user if request.user.is_authenticated else None
    if request.method == "POST" and 'Search' in request.POST:
        searched = request.POST.get("searched", "")
        keys = Post.objects.filter(title__contains=searched)
    return render(request, 'search.html', {"searched": searched, "keys": keys, "user": user})

@login_required
def ai_suggest(request):
    if request.user.is_authenticated:
        userinfo=get_object_or_404(UserInfo,id=request.user.id)
        ListHistorychat=HistoryChat.objects.filter(iduser=userinfo)
        if request.method=="POST":
            data=json.loads(request.body.decode('utf-8'))
            form_type=data.get('form_type')
            if form_type == 'chatbot':
                question=data.get('content')
                newChat=HistoryChat.objects.create(iduser=userinfo)
                newChat.content=question
                newChat.fromAI=0
                newChat.save()
                allpost= Post.objects.all()
                trainning=""
                for post in allpost:
                    trainning+=f'{post.title}, địa chỉ: {post.address}, đánh giá: {post.star} sao; \n'
                question= f'Bạn tên là FoodieFriend, nhiệm vụ của bạn chỉ là tư vấn về món ăn, không trả lời câu hỏi không liên quan đến món ăn và không trả lời những câu hỏi mà bạn không rõ yêu cầu, hãy đọc câu hỏi sau: "{question}". Nếu câu hỏi hợp lệ hãy trả lời ngắn gọn và thật thông minh phù hợp với câu hỏi của người dùng dựa theo các dữ liệu sau(bạn không cần liệt kê hết, chỉ đưa ra những gì phù hợp, và đừng nhầm lẫn giữa quán ăn và quán bán nước): {trainning}. Nếu không hợp lệ thì không trả lời. Bạn không được dùng kí tự đặc biệt trong câu trả lời.'
                api_key = None
                with open("env","r") as file:
                    api_key=file.read()
                client = OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model='gpt-3.5-turbo-0125',
                    messages=[
                        {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": question},
                        ],
                        }
                    ],
                    stream=True,
                )
                ai_response = ""
                for chunk in response:
                    if chunk.choices[0].delta.content is not None:
                        ai_response += chunk.choices[0].delta.content
                newChat1=HistoryChat.objects.create(iduser=userinfo)
                newChat1.content=ai_response
                newChat1.fromAI=1
                newChat1.save()
                return JsonResponse({'ai_response': ai_response})
        return render(request, 'index_login.html', {'ListHistorychat': ListHistorychat})
    else:
        return redirect('index')

def profile(request, user_id):
    if request.user.id==user_id:
        is_owner = True
        userinfo = get_object_or_404(UserInfo,id=user_id)
        if request.method=="POST":
            if 'savebtn' in request.POST:
                userinfo.firstname=request.POST.get('firstname')
                userinfo.lastname=request.POST.get('lastname')
                userinfo.phonenumber=request.POST.get('phonenumber')
                userinfo.gender=request.POST.get('gender')
                userinfo.avatar=request.FILES.get('inputavatar')
                userinfo.introduction=request.POST.get('introduction')
                userinfo.save()
                return render(request, 'profile.html',{'user':userinfo, 'is_owner': is_owner})
            if 'cancelbtn' in request.POST:
                return redirect('/usr/{}/'.format(request.user.id))
        return render(request, 'profile.html',{'user':userinfo, 'is_owner': is_owner})
    else:
        is_owner = False
        otheruserinfo = get_object_or_404(UserInfo, id=user_id)
        return render(request, 'profile.html', {'otheruserinfo': otheruserinfo, 'is_owner': is_owner})

def post(request, post_id):
    
    post = get_object_or_404(Post, pk=post_id)
    userpostinfo = post.idUser
    listcomment= Comment.objects.filter(idPost=post_id)
    check = {}
    for comment in listcomment:
        if comment.idcommentReply is None:
            check[comment.id] = 1
    if request.user.is_authenticated:
        userstar=0
        userinfo=get_object_or_404(UserInfo,id=request.user.id)
        if React.objects.filter(idpost= post.id, iduser=userinfo.id).exists() is True:
            userstarobj=get_object_or_404(React,idpost= post, iduser=userinfo)
            userstar=userstarobj.star
        if request.method == 'POST':
            if request.content_type != 'application/json':
                print(request.content_type)
                return HttpResponseBadRequest('Invalid content type.')
            try:
                data_post = json.loads(request.body.decode('utf-8'))
                form_type=data_post.get('form_type')
            except json.JSONDecodeError:
                return HttpResponseBadRequest('Invalid JSON data.')
            if data_post.get('form_type')=='react':
                st=data_post.get('star')
                if React.objects.filter(idpost= post.id, iduser=userinfo.id).exists() is True:
                    previous=get_object_or_404(React,idpost= post, iduser=userinfo)
                    post.totalstar-=previous.star
                    post.numcreact-=1
                    previous.star=st
                    previous.save()
                else:
                    newreact=React.objects.create()
                    newreact.star=st
                    newreact.idpost=post
                    newreact.iduser=userinfo
                    newreact.save()
                post.totalstar+=st
                post.numcreact+=1
                post.star=round((1.0*post.totalstar/post.numcreact),1) 
                post.save()
                return JsonResponse({
                    'star': post.star,
                })
            comment_content = data_post.get('content')
            if not comment_content or not comment_content.strip():
                return HttpResponseBadRequest('Invalid comment content.')
            new_comment = Comment.objects.create()
            new_comment.content=comment_content
            if form_type=='formcommentreply':
                idcommentrep=data_post.get('idcommentrep')
                new_comment.idcommentReply=get_object_or_404(Comment,id=idcommentrep)
            new_comment.idPost=post
            new_comment.idUsercomment=userinfo
            new_comment.save()
            new_comment.date=(new_comment.date.strftime("%B %d, %Y, %I:%M %p").replace(" 0", " "))
            new_comment.date=(new_comment.date[:-2] + new_comment.date[-2:].lower())
            new_comment.date = new_comment.date.replace("pm", "p.m.")
            return JsonResponse({
                'success': True,
                'comment': {
                    'id': new_comment.id,
                    'content': new_comment.content,
                    'date': new_comment.date,
                }
            })
        return render(request, 'index_post.html', {'post': post, 'userpostinfo': userpostinfo, 'userinfo': userinfo, 'listcomment':listcomment,'check':check,'userstar': userstar})
    else:
        return render(request, 'index_post.html', {'post': post, 'userpostinfo': userpostinfo,'listcomment':listcomment})

def search_suggestions(request):
    suggestions = []
    if request.method == 'POST' and 'inputValue' in request.POST:
        input_value = request.POST['inputValue']
        # Tìm các bài đăng có tiêu đề chứa từ khóa nhập vào
        suggestions = Post.objects.filter(title__icontains=input_value)
        # Lọc các tiêu đề duy nhất và giới hạn số lượng gợi ý
        unique_suggestions = list(set(suggestions))[:4]
        # Chuyển đổi các gợi ý thành danh sách
        suggestions = [post.title for post in unique_suggestions]
        postids = [post.id for post in unique_suggestions]
    return JsonResponse({'suggestions': suggestions, 'postids': postids})

def category(request):
    mon_chay_posts = []
    thuc_an_nhanh_posts = []
    tra_sua_posts = []
    an_sang_posts = []

    # Lấy các bài viết có tag "Món chay"
    mon_chay_tag = Tag.objects.get(name="món chay")      
    mon_chay_posts = Post.objects.filter(tags=mon_chay_tag)[:9]

    # Lấy các bài viết có tag "thức ăn nhanh"
    thuc_an_nhanh_tag = Tag.objects.get(name="thức ăn nhanh")      
    thuc_an_nhanh_posts = Post.objects.filter(tags=thuc_an_nhanh_tag)[:9]

    # Lấy các bài viết có tag "trà sữa
    tra_sua_tag = Tag.objects.get(name="trà sữa")   
    tra_sua_posts = Post.objects.filter(tags=tra_sua_tag)[:9]
    
    # Lấy các bài viết có tag "Trà sữa"
    an_sang_tag = Tag.objects.get(name="ăn sáng")
    an_sang_posts = Post.objects.filter(tags=an_sang_tag)[:9]

    return render(request, 'category.html', {'mon_chay_posts': mon_chay_posts, 'thuc_an_nhanh_posts': thuc_an_nhanh_posts, 'tra_sua_post': tra_sua_posts, 'an_sang_post': an_sang_posts})

from datetime import date
def daily(request):
    # Lấy ngày hiện tại
    current_date = date.today()

    # Lấy tất cả các bài viết trong ngày
    daily_posts = Post.objects.filter(date__date=current_date)

    return render(request, 'daily.html', {'daily_posts': daily_posts})

def ranking(request):
    top_posts = Post.objects.order_by('-star')
    return render(request, 'ranking.html', {'top_posts': top_posts})