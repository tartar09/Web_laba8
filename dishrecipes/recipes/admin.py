from django.contrib import admin
from django.core.checks import messages

from .models import Recipes, Category

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Кулинарные рецепты"


class CharFilter(admin.SimpleListFilter):
    title = 'Добавлены харакетристики'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'есть'),
            ('no', 'нет'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(characteristics__isnull=False)
        elif self.value() == 'no':
            return queryset.filter(characteristics__isnull=True)


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_create',
                    'is_published', 'cat', 'brief_info')
    list_display_links = ('title',)
    list_editable = ('is_published',)
    ordering = ['-time_create', 'title']
    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'cat__name']
    list_filter = [CharFilter, 'cat__name', 'is_published']
    fields = ['title', 'content', 'slug', 'cat', 'tags']
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ['tags']

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Recipes.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записи(ей).")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Recipes.Status.DRAFT)
        self.message_user(request, f"{count} записи(ей) сняты с публикации", messages.WARNING)

    @admin.display(description="Краткое описание")
    def brief_info(self, recipes: Recipes):
        return f"Описание {len(recipes.content)} символов."


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

# admin.site.register(Recipes)
# Register your models here.
