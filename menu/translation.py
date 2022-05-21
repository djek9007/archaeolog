from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

from menu.models import Menu


@register(Menu)
class MenuTranslationOptions(TranslationOptions):
    fields = ('name', )


