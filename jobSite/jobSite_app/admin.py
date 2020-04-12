from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(JobOffer)
admin.site.register(Comment)
