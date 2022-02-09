from django.http import JsonResponse
from django.shortcuts import redirect
from icecream import ic
from scipy.stats import pearsonr

from data_proc.celery import app
from .models import Correlation


@app.task
def correlation_calculation(first_value,
                            second_value,
                            x_data_type,
                            y_data_type,
                            ):
    cor, p_value = pearsonr(first_value, second_value)
    Correlation(
        x_data_type=x_data_type,
        y_data_type=y_data_type,
        value=cor,
        p_value=p_value
    ).save()
