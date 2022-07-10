from django import forms
from account.models import MyUser, Profile


class RegisterForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['username', 'mobile', 'first_name', 'last_name', 'password_1', 'password_2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'نام کاربری'}),
            'mobile': forms.TextInput(attrs={'placeholder': 'شماره همراه'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'نام خود را وارد کنبد'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'نام خانوادگی'}),
            'password_1': forms.PasswordInput(attrs={'placeholder': 'کلمه عبور را وارد کنید'}),
            'password_2': forms.PasswordInput(attrs={'placeholder': 'تکرار کلمه عبور'}),
        }
    def clean_username(self):
        username = self.cleaned_data['username']
        if MyUser.objects.filter(username=username).exists():
            raise forms.ValidationError('نام کاربری از قبل وارد شده است!')
        return username

    def clean_password2(self):
        password_1 = self.cleaned_data.get('password_1')
        password_2 = self.cleaned_data.get('password_2')

        if password_1 and password_2 and password_1 != password_2:
            raise forms.ValidationError('دو پسورد باهم مطابقت ندارند!')

        elif len(password_2) < 8:
            raise forms.ValidationError('پسورد شما باید حداقل 8 حرف باشد')

        elif not any(x.isupper() for x in password_2) < 8:
            raise forms.ValidationError('باید پسورد شما حداقل یک حروف بزرگ داشته باشد')

        return password_2


    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password_2'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField( widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields['username'].help_text = 'None'

        # if not user.is_superuser:
        #     self.fields['username'].disabled = True

    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name','username', 'mobile')


class AddressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(AddressForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Profile
        fields = ('address', 'ostan', 'shahrestan', 'postalcode', 'description')
