from django import forms

from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError


class AuthenticationForm(forms.Form):
    username = forms.CharField(
        label="اسم المستخدم")
    password = forms.CharField(widget=forms.PasswordInput(),label="كلمة المرور")

    class Meta:
        fields = {'username', 'password'}
        labels = {"username": "اسم المستخدم",
                  "password": "كلمة المرور",

                  }

    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': "username"})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': "Password"})


class PasswordChangeCustomForm(PasswordChangeForm):
    class Meta:

        labels = {'old_password': 'كلمة المرور الحالية'
            ,"new_password1": "كلمة المرور الجديدة ",
                  "new_password2": " تاكيد كلمة المرور ",

                  }
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': "Old Password"})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': "New Password"})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': "New Password"})

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise ValidationError("لاتتطابق كلمات المرور")

        return new_password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]

        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user
