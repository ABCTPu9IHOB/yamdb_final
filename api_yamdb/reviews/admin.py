from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
from reviews.models import (Genre, Category, Title, Review, Comment)


class GenreResource(resources.ModelResource):

    class Meta:
        model = Genre


class CategoryResource(resources.ModelResource):

    class Meta:
        model = Category


class TitleResource(resources.ModelResource):

    class Meta:
        model = Title


class ReviewResource(resources.ModelResource):
    title = Field(attribute='title', column_name='title_id',
                  widget=ForeignKeyWidget(Title))

    class Meta:
        model = Review


class CommentResource(resources.ModelResource):
    review = Field(attribute='review', column_name='review_id',
                   widget=ForeignKeyWidget(Review))

    class Meta:
        model = Comment


@admin.register(Genre)
class GenreAdmin(ImportExportModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name', 'slug')
    resource_classes = [GenreResource]


@admin.register(Category)
class CategoriesAdmin(ImportExportModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name', 'slug')
    resource_classes = [CategoryResource]


@admin.register(Title)
class TitleAdmin(ImportExportModelAdmin):
    list_display = ('name', 'year', 'description', 'category')
    search_fields = ('name', 'year', 'description', 'category')
    list_filter = ('name', 'year', 'description', 'category')
    resource_classes = [TitleResource]


@admin.register(Review)
class ReviewAdmin(ImportExportModelAdmin):
    list_display = (
        'pk',
        'author',
        'text',
        'score',
        'title'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('author', 'score',)
    search_fields = ('author',)
    resource_classes = [ReviewResource]


@admin.register(Comment)
class CommentAdmin(ImportExportModelAdmin):
    list_display = (
        'pk',
        'author',
        'text',
        'review'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('author',)
    search_fields = ('author',)
    resource_classes = [CommentResource]
