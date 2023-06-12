from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, ListView, DetailView, DeleteView

from .forms import Find_job
from .models import Vacancies, Speciality


def home_view(request):
    """ выводит все вакансии """
    form = Find_job()
    return render(request, 'scraping/home.html', {'form': form})


"""
Сортируем city and speciality и  подключаем пагинацию
"""

def list_view(request):
    # print(request.GET)
    form = Find_job()
    city = request.GET.get('city')
    speciality = request.GET.get('speciality')
    context = {'city': city, 'speciality': speciality, 'form': form}
    if city or speciality:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if speciality:
            _filter['speciality__slug'] = speciality
        qs = Vacancies.objects.filter(**_filter).select_related('city', 'speciality')
        paginator = Paginator(qs, 10)  # показывает 10 листов

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj
    return render(request, 'scraping/vacant_list.html', context)



def v_detail(request, pk=None):
    # object_ = Vacancy.objects.get(pk=pk)
    object_ = get_object_or_404(Vacancies, pk=pk)
    return render(request, 'scraping/detail.html', {'object': object_})


class VDetail(DetailView):
    queryset = Vacancies.objects.all()
    template_name = 'scraping/detail.html'
    # context_object_name = 'object'


# class VCreate(CreateView):
#     model = Vacancies
#     # fields = '__all__'
#     form_class = VForm
#     template_name = 'scraping/create.html'
#     success_url = reverse_lazy('home')
#

# class VUpdate(UpdateView):
#     model = Vacancy
#     form_class = VForm
#     template_name = 'scraping/create.html'
#     success_url = reverse_lazy('home')


class VDelete(DeleteView):
    model = Vacancies
    template_name = 'scraping/delete.html'
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Запись успешно удалена.')
        return self.post(request, *args, **kwargs)
