from django import forms
from django_countries.fields import CountryField
from . import models


# Form fields 참고
# https://docs.djangoproject.com/en/3.2/ref/forms/fields/

# django-country 라이브러리에서 form태그 안에 쓰일 Form field 참고.
# https://github.com/SmileyChris/django-countries
class SearchForm(forms.Form):

    city = forms.CharField(initial="Anywhere")
    price = forms.IntegerField(required=False)
    # html에서 <select>, <option> 태그와 동일한 역할 하는 필드
    room_type = forms.ModelChoiceField(
        required=False, empty_label="Any kind", queryset=models.RoomType.objects.all()
    )
    country = CountryField(default="KR").formfield()
    guests = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)
    instant_book = forms.BooleanField(required=False)
    superhost  = forms.BooleanField(required=False)
    amenities = forms.ModelMultipleChoiceField(
        required=False, queryset=models.Amenity.objects.all(), widget=forms.CheckboxSelectMultiple
    )
    facilities = forms.ModelMultipleChoiceField(
        required=False, queryset=models.Facility.objects.all(), widget=forms.CheckboxSelectMultiple
    )