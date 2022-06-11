from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("article_id", "title", "published_at", "url")
    list_display_links = ("title", "article_id")
    search_fields = ("title", "article_id")
    fields = ("article_id", "title", "full_text", "published_at", "url")

    readonly_fields = ("url", )
