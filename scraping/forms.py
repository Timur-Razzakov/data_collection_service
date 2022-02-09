from django import forms

from .models import City, Speciality, Vacancies


class Find_job(forms.Form):
    """создаём форму для вакансий"""
    city = forms.ModelChoiceField(
        queryset=City.objects.all(), to_field_name='slug',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Город'
    )
    speciality = forms.ModelChoiceField(
        queryset=Speciality.objects.all(), to_field_name='slug',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Специальность'
    )

class VForm(forms.ModelForm):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Город'
    )
    language = forms.ModelChoiceField(
        queryset=Speciality.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Специальность'
    )
    url = forms.CharField(label='URL', widget=forms.URLInput(
        attrs={'class': 'form-control'}))
    title = forms.CharField(label='Заголовок вакансии', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    company = forms.CharField(label='Компания', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    description = forms.CharField(label='Описание вакансии',
                                  widget=forms.Textarea(
                                      attrs={'class': 'form-control'}))

    class Meta:
        model = Vacancies
        fields = '__all__'