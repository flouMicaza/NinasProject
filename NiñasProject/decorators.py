from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def alumna_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='usuarios:login'):
    '''
    Decorator for views that checks that the logged in user is a student,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.es_alumna,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def profesora_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='usuarios:login'):
    '''
    Decorator for views that checks that the logged in user is a teacher,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.es_profesora,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def docente_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='usuarios:login'):
    '''
    Decorator for views that checks that the logged in user is a teacher,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and (u.es_profesora or u.es_voluntaria or u.es_coordinadora),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def coordinadora_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='usuarios:login'):
    '''
    Decorator for views that checks that the logged in user is a coordinator,
    redirects to the log-in page if necessary.
    '''
    actual_decorator =  user_passes_test(
        lambda u: u.is_active and u.es_coordinadora,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator