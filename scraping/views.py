from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from .forms import Find_job, VForm
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
        paginator = Paginator(qs, 5)  # показывает 5 листов

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj
    return render(request, 'scraping/vacant_list.html', context)


"""
Функция для вывода вакансии, которая вас заинтересовала 
"""


# 1-var
def v_detail(request, pk=None):
    object_ = get_object_or_404(Vacancies, pk=pk)
    return render(request, 'scraping/detail.html', {'object': object_})
#
#
# # 2-var
# class VDetail(DetailView):
#     queryset = Vacancies.objects.all()
#     template_name = 'scraping/detail.html'
#     # context_object_name = 'object'


# class VList(ListView):
#     model = Vacancies
#     template_name = 'scraping/vacant_list.html'
#     form = Find_job()
#     paginate_by = 10
#     #
#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
#         context = super().get_context_data(**kwargs)
#         context['city'] = self.request.GET.get('city')
#         context['speciality'] = self.request.GET.get('speciality')
#         context['form'] = self.form
#
#         return context
#
#     def get_queryset(self):
#         city = self.request.GET.get('city')
#         language = self.request.GET.get('speciality')
#         qs = []
#         if city or language:
#             _filter = {}
#             if city:
#                 _filter['city__slug'] = city
#             if language:
#                 _filter['speciality__slug'] = language
#             qs = Vacancies.objects.filter(**_filter).select_related('city', 'speciality')
#         return qs


class VCreate(CreateView):
    model = Vacancies
    # fields = '__all__'
    form_class = VForm
    template_name = 'scraping/create.html'
    success_url = reverse_lazy('home')


class VUpdate(UpdateView):
    model = Vacancies
    form_class = VForm
    template_name = 'scraping/create.html'
    success_url = reverse_lazy('home')


class VDelete(DeleteView):
    model = Vacancies
    # template_name = 'scraping/delete.html'
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Запись успешно удалена.')
        return self.post(request, *args, **kwargs)
