from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms


class LoginView(FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")
    initial = {"email":"hyeong77@gmail.com"}

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)



# class 기반 view
# class LoginView(View):

#     def get(self, request):
#         form = forms.LoginForm(initial={"email" : "itn@las.com"})
#         # print(form)
#         return render(request, "users/login.html", {"form" : form})

#     def post(self, request):
#         form = forms.LoginForm(request.POST)
#         ### form객체의 유효성 검사
#         # => form 객체에서 raise Error 등을 통한 에러가 발생하지 않으면 True
#         print(form.is_valid())
#         ### 데이터 유효성 검사.
#         # 1) 데이터 존재 확인
#         # 2) 데이터 정리
#         # 3) 데이터 접근(cleaned_data를 통해)
#         # print(form.cleaned_data)
#         try:
#             if form.is_valid():
#                 email = form.cleaned_data.get("email")
#                 password = form.cleaned_data.get("password")
#                 # email, password와 일치하는 유저가 존재하면 usename반환.
#                 # 존재하지 않으면 None 반환.AssertionError()
#                 user = authenticate(request, username=email, password=password)
#                 if user is not None:
#                     login(request, user)
#                     return redirect(reverse("core:home"))
#             return render(request, "users/login.html", {"form" : form})
#         except:
#             pass
#             return render(request, "users/login.html", {"form" : form})



# class LogoutView(View):

#     def get(self, request):
#         # authenticate 작업 필요.
#         return redirect(reverse("core:home"))

#     def post(self, request):
#         # authenticate 작업 필요.
#         return redirect(reverse("core:home"))




# function 기반 view
# def login_view(request):
#     if request.method == "GET":
#           pass
#     elif request.method == "POST":
#           pass

def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    initial = {
        "first_name":"Nicoas",
        "last_name":"Serr",
        "email":"itn@las.com"
    }

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)
        