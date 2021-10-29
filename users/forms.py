from django import forms
from . import models

class LoginForm(forms.Form):
    # username(= email), password
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        print(self.cleaned_data)
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password is incorrect"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))


class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=80)
    last_name = forms.CharField(max_length=80)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Config Password")


    def clean_email(self):
        email = self.cleaned_data.get("email")
        print(self.cleaned_data)
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError("User alreaday exists with that email")
        except models.User.DoesNotExist:
            return email

    # clean메서드는 필드 위에서부터 하나씩 타고가기때문에
    # password, password1 값을 비교하기 위해서 clean_password1 메서드를 이용한다.
    def clean_password1(self):
        password = self.cleaned_data.get("password")
        print(self.cleaned_data)
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    # def clean_password1(self):
    #     # password = self.cleaned_data.get("password")
    #     password1 = self.cleaned_data.get("password1")
    #     print(self.cleaned_data)
    #     return password1


    def save(self):
        print(self.cleaned_data)
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        user = models.User.objects.create_user(email, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()


    # clean_[] 메서드 : field의 데이터를 지워주는 역할
    # # self : LoginForm객체
    # def clean_email(self):
    #     # 입력한 email필드값 출력.
    #     # print(self.cleaned_data)
    #     email = self.cleaned_data.get('email')
    #     # 입력한 email필드와 일치하는 user가 존재할 경우, email 반환.
    #     try:
    #         models.User.objects.get(username=email)
    #         return email
    #     except models.User.DoesNotExist:
    #         # 에러 발생
    #         raise forms.ValidationError("User does not exist")
    
    # # self : LoginForm객체
    # def clean_password(self):
    #     # 입력한 password필드값과
    #     # 위의 clean_email메서드에서 반환한 email값이 함께 출력됨 !
    #     # print(self.cleaned_data)
    #     password = self.cleaned_data.get('password')
    #     return password

    # self : LoginForm객체..... => self.cleaned_data하면 views.py에서와 같이 {'email': '...', 'password': '...'} 출력되네.
    # def clean(self):
    #     email = self.cleaned_data.get("email")
    #     password = self.cleaned_data.get("password")
    #     try:
    #         user = models.User.objects.get(username=email)
    #         if user.check_password(password):
    #             # return password
    #             return self.cleaned_data
    #         else:
    #             # raise forms.ValidationError("Password is wrong")
    #             self.add_error("password", forms.ValidationError("Password is wrong"))
    #     except models.User.DoesNotExist:
    #         # raise forms.ValidationError("User does not exist")
    #         self.add_error("email", forms.ValidationError("User does not exist"))

