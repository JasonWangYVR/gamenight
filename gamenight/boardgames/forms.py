from django import forms

class SearchForm(forms.Form):
    q = forms.CharField(
        required = True,
        max_length = 50,
        widget=forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder': 'Boardgame, tag',
            }
        )
    )

class PerPageForm(forms.Form):
    page_size = forms.IntegerField()

    def process(self):
    # Assumes .cleaned_data exists because this method is always invoked after .is_valid(), otherwise will raise AttributeError
    	cd = self.cleaned_data
    	if not cd:
    		self = 20 