from django.contrib import admin
from .models import Group, Predmets, Prepods, Cabs, PredM, Schedule
# Register your models here.

# Регистрация моделей в админке
class PredmetsAdmin(admin.ModelAdmin):
    list_display = ('group', 'get_predm_name', 'hours_total')
    readonly_fields = ('get_predm_name', )

    def get_predm_name(self, obj):
        return obj.name.name

    get_predm_name.short_description = "Название предмета"


admin.site.register(Predmets, PredmetsAdmin)
admin.site.register(Prepods)
admin.site.register(Group)
# admin.site.register(Predmets)
admin.site.register(Cabs)
admin.site.register(PredM)
admin.site.register(Schedule)

# admin.site.register(PredPred)


