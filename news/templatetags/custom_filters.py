from django import template


register = template.Library()

cens = ['Конь', 'Редис', 'Пупа']

# Регистрируем наш фильтр под именем censor, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()

   # Возвращаемое функцией значение подставится в шаблон.
def censor(word):
   if isinstance(word, str):
      for i in word.split():
         if i.capitalize() in cens:
               word = word.replace(i, i[0] + '*' * len(i))
   else:
      raise ValueError(
         'custom_filters -> censor -> A string is expected, but a different data type has been entered')
   return word