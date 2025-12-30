from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, authenticate
from django.utils.html import strip_tags
from django.core.validators import RegexValidator


User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        max_length=66,
        widget=forms.EmailInput(attrs={'class': 'input-register form-control', 'placeholder': 'Твой email'})
    )
    first_name = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'input-register form-control', 'placeholder': 'Твоё Имя'})
    )
    last_name = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'input-register form-control', 'placeholder': 'Твоя Фамилия'})
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'input-register form-control', 'placeholder': 'Твой пароль'})
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'input-register form-control', 'placeholder': 'Повтори пароль'})
    )
    marketing_consent1 = forms.BooleanField(
        required=False,
        label="Я согласен получать коммерческие, рекламные и маркетинговые сообщения.",
        widget=forms.CheckboxInput(attrs={'class': 'checkbox-input-register'})
    )
    marketing_consent2 = forms.BooleanField(
        required=False,
        label="Я согласен получать персонализированные рекламные сообщения.",
        widget=forms.CheckboxInput(attrs={'class': 'checkbox-input-register'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2',
                  'marketing_consent1', 'marketing_consent2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот адрес электронной почты уже используется.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = None
        user.marketing_consent1 = self.cleaned_data['marketing_consent1']
        user.marketing_consent2 = self.cleaned_data['marketing_consent2']
        if commit:
            user.save()
        return user


class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Email',
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'input-register form-control', 'placeholder': 'Твой Email'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'input-register form-control', 'placeholder': 'Твой пароль'})
    )

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(self.request, username=email, password=password)  # Используйте username вместо email
            if self.user_cache is None:
                raise forms.ValidationError('Неверный адрес электронной почты или пароль.')
            elif not self.user_cache.is_active:
                raise forms.ValidationError('Этот аккаунт неактивен.')
        return self.cleaned_data


class CustomUserUpdateForm(forms.ModelForm):
    phone = forms.CharField(
        required=False,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', "Enter a valid phone number.")],
        widget=forms.TextInput(attrs={'class': 'input-register form-control', 'placeholder': 'Твой телефон номер'})
    )
    first_name = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'input-register form-control', 'placeholder': 'Твоё имя'})
    )
    last_name = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'input-register form-control', 'placeholder': 'Твоя фамилия'})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'input-register form-control', 'placeholder': 'Твой email'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'address1', 'address2',
                  'city', 'country', 'province', 'postal_code', 'phone')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'input-register form-control', 
                                             'placeholder': 'Твой email'}),
            'first_name': forms.TextInput(attrs={'class': 'input-register form-control', 
                                                 'placeholder': 'Твое имя'}),
            'last_name': forms.TextInput(attrs={'class': 'input-register form-control', 
                                                'placeholder': 'Твоя фамилия'}),
            'address1': forms.TextInput(attrs={'class': 'input-register form-control', 
                                               'placeholder': 'Адрес 1'}),
            'address2': forms.TextInput(attrs={'class': 'input-register form-control', 
                                               'placeholder': 'Адрес 2'}),
            'city': forms.TextInput(attrs={'class': 'input-register form-control', 
                                           'placeholder': 'Твой город'}),
            'country': forms.TextInput(attrs={'class': 'input-register form-control', 
                                              'placeholder': 'Твоя страна'}),
            'province': forms.TextInput(attrs={'class': 'input-register form-control', 
                                               'placeholder': 'Твоя провинция'}),
            'postal_code': forms.TextInput(attrs={'class': 'input-register form-control', 
                                                  'placeholder': 'Твой почтовый индекс'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Этот адрес электронной почты уже используется.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('email'):
            cleaned_data['email'] = self.instance.email

        for field in ['address1', 'address2', 'city', 'country', 'province',
                      'postal_code', 'phone']:
            if cleaned_data.get(field):
                cleaned_data[field] = strip_tags(cleaned_data[field])

        return cleaned_data
