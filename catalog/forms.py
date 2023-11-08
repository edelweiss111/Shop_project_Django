from django import forms

from catalog.models import Product, Version


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'category', 'price',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        cleaned_data = self.cleaned_data.get('name')
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        for word in forbidden_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError('Такое название запрещено')

        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data.get('description')
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        for word in forbidden_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError('Такое описание запрещено')

        return cleaned_data


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ('product', 'name', 'number', 'is_active',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
