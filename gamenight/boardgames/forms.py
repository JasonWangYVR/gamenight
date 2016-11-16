from django import forms

class SearchForm(forms.Form):
    want_page = forms.IntegerField()

    def process(self):
    # Assumes .cleaned_data exists because this method is always invoked after .is_valid(), otherwise will raise AttributeError
    	cd = self.cleaned_data
    	if not cd:
    		self = 1 

class PerPageForm(forms.Form):
    page_size = forms.IntegerField()

    def process(self):
    # Assumes .cleaned_data exists because this method is always invoked after .is_valid(), otherwise will raise AttributeError
    	cd = self.cleaned_data
    	if not cd:
    		self = 20 