from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from main.models import User


class AdminAddForm(UserCreationForm):
    birthday = forms.DateField(
        localize=True,
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
        label="تاريخ الميلاد"
    )

    phone = forms.CharField(
        required=True,
        label="رقم الهاتف"
    )
    password1 = forms.CharField(label="كلمة المرور",
                                strip=False,
                                widget=forms.PasswordInput())
    password2 = forms.CharField(label="تاكيد كلمة المرور",
                                strip=False,
                                widget=forms.PasswordInput())
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username','password1','password2','name','birthday','phone', )
        labels = {"name": "الاسم ",
                  "username": "اسم المستخدم",
                  "password1": "كلمة المرور",
                  "password2": "تاكيد كلمة المرور"
                  }
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_admin = True
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(AdminAddForm, self).__init__(*args, **kwargs)


        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'