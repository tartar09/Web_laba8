menu = [
    {'title': "Главная", 'url_name': 'home'},
    {'title': "Поиск рецептов", 'url_name': 'find'},
    # {'title': "Войти", 'url_name': 'login'},
    {'title': "Добавить свой рецепт", 'url_name': 'add'},
    {'title': "О сайте", 'url_name': 'about'},
]


class DataMixin:
    paginate_by = 3
    title_page = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page
        if 'menu' not in self.extra_context:
            self.extra_context['menu'] = menu

    def get_mixin_context(self, context, **kwargs):
        if self.title_page:
            context['title'] = self.title_page

        context['menu'] = menu
        context['cat_selected'] = None
        context.update(kwargs)
        return context
