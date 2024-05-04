from django.contrib import admin
from .models import *

# Permite gerir os modelos da App Community
from django.apps import apps

app = apps.get_app_config('Community')

for model_name, model in app.models.items():
    admin.site.register(model)
