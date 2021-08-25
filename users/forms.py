from django import forms
from . import models
class LoginForm(forms.Form):

    # username(= email), password
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


    # # clean_[] 메서드 : field의 데이터를 지워주는 역할
    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     try:
    #         models.User.objects.get(username=email)
    #         return email
    #     except models.Users.DoesNotExist:
    #         raise forms.ValidationError("User does not exist")
    
    # def clean_password(self):
    #     # print("clena_password")
    #     password = self.cleaned_data.get('password')
    
    #     return password

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(username=email)
            if user.check_password(password):
                # return password
                return self.cleaned_data
            else:
                # raise forms.ValidationError("Password is wrong")
                self.add_error(form.ValidationError("password", "Password is wrong"))
        except models.Usser.DoesNotExist:
            # raise forms.ValidationError("User does not exist")
            self.add_error(form.ValidationError("email", "User does not exist"))

