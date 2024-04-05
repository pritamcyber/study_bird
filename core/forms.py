from django.forms import ModelForm


from .models import Room


class Room_form(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        # fields = ['host','participants',]
        exclude = ['host','participants']
        