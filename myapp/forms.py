from django import forms
from myapp.models import Order, Review
class SearchForm(forms.Form):
    LENGTH_CHOICES = [
    (8, '8 Weeks'),
    (10, '10 Weeks'),
    (12, '12 Weeks'),
    (14, '14 Weeks'),
    ]
    name = forms.CharField(max_length=100, required=False, label='Student Name')
    length = forms.TypedChoiceField(widget=forms.RadioSelect,
                                    choices = LENGTH_CHOICES, coerce=int, required=False, label='Prefered course duration')
    max_price = forms.IntegerField(label='Maximum Price', min_value=0)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['courses', 'Student', 'order_status']
        widgets = {'courses': forms.CheckboxSelectMultiple(), 'order_type':forms.RadioSelect}
        labels = {'Student': u'Student Name', }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer','course','rating','comments']
        widgets = {'course': forms.RadioSelect}
        labels = {'reviewer': u'Please enter a valid email', 'rating':u'Rating An Integer between 1(worst) and 5(best)'}
#     def clean_rating(self):
#         data = self.cleaned_data.get('rating')
#         if not is_rating_valid(data):
#             raise forms.ValidationError('Ratings must be between 1 to 5')
#         return data
#
# def is_rating_valid(rating):
#     return 5 >= rating >= 1