from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from django import forms
from django.template.defaultfilters import truncatechars
from .models import Vacancies, Speciality, City, Error


class AdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Vacancies
        fields = '__all__'


class VacanciesAdmin(admin.ModelAdmin):
    form = AdminForm
    list_display = (
        'title', 'company_name',
        'salary', 'city', 'speciality', 'created_at', 'url',)  # исл для показа каких либо данных в админке

    readonly_fields = ('created_at',)
    list_display_links = ('url', 'title','company_name')
    save_as = False  # добавляет кнопку "сохранить как новый объект" в админке
    search_fields = ('id', 'title', 'city')  # поиск по айди и по наименованию


class SpecialityAdmin(admin.ModelAdmin):
    """Заполняем автоматически slug"""
    prepopulated_fields = {"slug": ("name_of_specialty",)}


class CityAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("country_name",)}


admin.site.register(Vacancies, VacanciesAdmin)
admin.site.register(Speciality, SpecialityAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Error)
