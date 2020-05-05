from django import forms

class PackagingForm(forms.Form):
    pass


class RecipeToBasketForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=10, required=True)
    