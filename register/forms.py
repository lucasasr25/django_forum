from django import forms
from myapp.models import Author

class UpdateForm(forms.ModelForm):
    delete_all_data = forms.BooleanField(
        required=False,  # The checkbox is not required
        label="Delete all user data",  # Label for the checkbox
    )
    
    class Meta:
        model = Author
        fields = ("fullname", "bio")