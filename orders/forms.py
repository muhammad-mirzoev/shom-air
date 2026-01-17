from django import forms
from django.utils.html import strip_tags


class OrderForm(forms.Form):
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-black rounded-none text-black placeholder-gray-500 focus:outline-none focus:border-black',
            'placeholder': 'Имя'
        })
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-black rounded-none text-black placeholder-gray-500 focus:outline-none focus:border-black',
            'placeholder': 'Фамилия'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 border border-black rounded-none text-black placeholder-gray-500 focus:outline-none focus:border-black',
            'placeholder': 'Email',
            'readonly': 'readonly'
        })
    )
    company = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-black rounded-none text-black placeholder-gray-500 focus:outline-none focus:border-black',
            'placeholder': 'Компания (необязательно)'
        })
    )
    address1 = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-black rounded-none text-black placeholder-gray-500 focus:outline-none focus:border-black pr-10',
            'placeholder': 'Адрес'
        })
    )
    address2 = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-black rounded-none text-black placeholder-gray-500 focus:outline-none focus:border-black',
            'placeholder': 'Адрес 2'
        })
    )
    city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-black rounded-none text-black placeholder-gray-500 focus:outline-none focus:border-black',
            'placeholder': 'Город'
        })
    )
    country = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-black rounded-none text-black placeholder-gray-500 focus:outline-none focus:border-black',
            'placeholder': 'Страна'
        })
    )
    province = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-black rounded-none text-black placeholder-gray-500 focus:outline-none focus:border-black',
            'placeholder': 'Провинция'
        })
    )
    postal_code = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-black rounded-none text-black placeholder-gray-500 focus:outline-none focus:border-black',
            'placeholder': 'Почтовый индекс'
        })
    )
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-black rounded-none text-black placeholder-gray-500 focus:outline-none focus:border-black pr-10',
            'placeholder': 'Телефон (Обязательно)'
        })
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = getattr(user, 'first_name', '')
            self.fields['last_name'].initial = getattr(user, 'last_name', '')
            self.fields['email'].initial = getattr(user, 'email', '')
            self.fields['company'].initial = getattr(user, 'company', '')
            self.fields['address1'].initial = getattr(user, 'address1', '')
            self.fields['address2'].initial = getattr(user, 'address2', '')
            self.fields['city'].initial = getattr(user, 'city', '')
            self.fields['country'].initial = getattr(user, 'country', '')
            self.fields['province'].initial = getattr(user, 'province', '')
            self.fields['postal_code'].initial = getattr(user, 'postal_code', '')
            self.fields['phone'].initial = getattr(user, 'phone', '')

    def clean(self):
        cleaned_data = super().clean()
        for field in ['company', 'address1', 'address2', 'city',
                      'country', 'province', 'postal_code', 'phone']:
            if cleaned_data.get(field):
                cleaned_data[field] = strip_tags(cleaned_data[field])
        return cleaned_data
