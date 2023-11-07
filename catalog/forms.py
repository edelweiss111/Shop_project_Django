from django import forms

from catalog.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'category', 'price',)

    def clean_name(self):
        cleaned_data = self.cleaned_data.get('name')
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        for word in forbidden_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError('Такое название запрещено')

        return cleaned_data


class VersionForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
