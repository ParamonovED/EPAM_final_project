from .models import Target, Ad
from django.forms import ModelForm, Textarea, NumberInput


class TargetForm(ModelForm):
    class Meta:
        model = Target
        fields = ["title", "wanted_price"]
        widgets = {
            "title": Textarea(attrs={
                "class": "form-control",
                "type": "text",
                "placeholder": "Title",
                "rows": "5"
            }),
            "wanted_price": NumberInput(attrs={
                "class": "form-control",
                "type": "text",
                "placeholder": "Wanted price"
            })
        }


# class UpdateTargetForm(ModelForm):
#     class Meta:
#         model = Ad
#         fields = ["target"]
