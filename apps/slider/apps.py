from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SliderConfig(AppConfig):
    name = 'apps.slider'
    # icon = settings.SLIDER_APP_ICON
    verbose_name = _('Slider')

