from django.contrib import admin
from .models import *

# Permite gerir as categorias e posts do site
admin.site.register(Categoria)
admin.site.register(Post)
