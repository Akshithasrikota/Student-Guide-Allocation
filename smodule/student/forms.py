from django import forms
from .models import Guide

# class PreferenceForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Dynamically fetch faculty from the Guide model
#         preferences = Guide.objects.all()

#         # Create a dropdown field for each faculty preference
#         for i, pref in enumerate(preferences, start=1):
#             self.fields[f'preference{i}'] = forms.ChoiceField(
#                 choices=[(p.guide_name, p.guide_name) for p in preferences],
#                 label=f'Preference {i}',
#                 required=False,
#             )


from django import forms
from .models import Guide

class PreferenceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically fetch faculty from the Guide model
        preferences = Guide.objects.all()

        # Create a dropdown field for each faculty preference
        for i, pref in enumerate(preferences, start=1):
            self.fields[f'preference{i}'] = forms.ChoiceField(
                choices=[(p.guide_name, p.guide_name) for p in preferences],
                label=f'Preference {i}',
                required=False,
            )



