# -*- coding: utf-8 -*-
from django.contrib import admin
from blog.models import EntryTag, Entry, Comment, EntryImage#, RelEntry

# class RelEntryInline(admin.TabularInline):
#     model = RelEntry
#     fk_name = 'to_entry'

class EntryAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
                'fields': ('created_by', 'title', 'body', 'slug', 'created', 'is_publish', 'allow_comment'),
                }),
        ('タグ', {
                'fields': ('tags',),
                #'classes': ('wide',),
                #'classes': 'collapse'
                }),
        ('関連エントリ', {
                'fields': ('rel_entries',),
                'classes': ('collapse',),
                }),
        )
    date_hierarchy = 'created'
    list_display = ('title', 'created', 'updated', 'comment_count', 'is_publish', 'created_by')
    list_filter = ('created_by', 'created', 'is_publish', 'tags')
    list_per_page = 50
    ordering = ['-created', '-updated']
    search_fields = ['title', 'body']
    list_select_related = True
    save_as = True

    filter_horizontal = ('tags','rel_entries')
#    filter_horizontal = ('tags',)
#    raw_id_fields = ('rel_entries',)
    prepopulated_fields = {'slug': ('title',)}

#    inlines = [ RelEntryInline, ]

class CommentAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ('author', 'body', 'is_publish', 'entry')}),)
    date_hierarchy = ('created')
    list_display = ('created', 'author', 'is_publish', 'entry')
    list_filter = ('created', 'is_publish')
    search_fields = ['author', 'body']
    ordering = ['-created']

    raw_id_fields = ('entry',)

class EntryImageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
                'fields': ('created_by', 'image', 'description', 'is_publish'),
                }),
        ('タグ', {'fields': ('tags',)}),
#         ('関連イメージ', {
#                 'fields': ('rel_entry_images',),
#                 'classes': 'collapse'
#                 }),
        )

    date_hierarchy = 'created'
    list_display = ('__unicode__', 'created', 'updated', 'is_publish', 'created_by')
    list_filter = ('created_by', 'created', 'is_publish', 'tags')
    ordering = ['-created', '-updated']
    search_fields = ['discription', 'image']
    list_select_related = True

    filter_horizontal = ('tags', 'rel_entry_images')

admin.site.register(EntryTag)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(EntryImage, EntryImageAdmin)

