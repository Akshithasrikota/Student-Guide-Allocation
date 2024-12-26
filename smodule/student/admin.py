from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Student, Company, UserPreference, Guide,PreferenceTimeframe

# Register your models
admin.site.register(Student)
admin.site.register(Company)
admin.site.register(UserPreference)
admin.site.register(Guide)
admin.site.register(PreferenceTimeframe)

