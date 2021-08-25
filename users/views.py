from django.views import View
from django.shortcuts import render
from . import forms

class LoginView(View):

    def get(self, request):
        form = forms.LoginForm(initial={"email" : "itn@las.com"})
        return render(request, "users/login.html", {"form" : form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        # print(form)

        # 데이터 유효성 검사.
        # 1) 데이터 존재 확인
        # 2) 데이터 정리
        # 3) 데이터 접근(cleaned_data를 통해)
        if form.is_valid():
            print(form.cleaned_data)
        return render(request, "users/login.html", {"form" : form})




# def login_view(request):
#     if request.method == "GET":
#     elif request.method == "POST":