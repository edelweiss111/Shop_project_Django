from django import forms

from catalog.models import Product, Version


class StyleFormMixin:
    """Миксин для стилизации форм"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    """Форма для модели Product"""

    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'category', 'price',)

    def clean_name(self):
        """Валидация поля name по запрещенным словам"""
        cleaned_data = self.cleaned_data.get('name')
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        for word in forbidden_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError('Такое название запрещено')

        return cleaned_data

    def clean_description(self):
        """Валидация поля description по запрещенным словам"""
        cleaned_data = self.cleaned_data.get('description')
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        for word in forbidden_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError('Такое описание запрещено')

        return cleaned_data


class ModeratorProductForm(ProductForm):
    class Meta:
        model = Product
        fields = ('description', 'category', 'is_published',)


class VersionForm(StyleFormMixin, forms.ModelForm):
    """Форма для модели Version"""

    class Meta:
        model = Version
        exclude = ('product',)
