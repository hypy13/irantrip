from django.contrib import admin
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from apps.slider.models import Slider


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', '_photo', 'language']
    list_filter = ['status', 'language', ]

    @admin.display(description=_('Photo'))
    def _photo(self, obj):
        return mark_safe(
            f'<img src={obj.photo.url} width=62 height=62>'
        )
