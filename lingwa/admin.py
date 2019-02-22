# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Url, Image, Language, Utterence, Keyword, KeywordUrl, LexicalDefinition, LexicalClass

class UrlAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {'fields': ['url', 'active']}),
    ]

    list_display = ['url', 'last_read']
    search_fields = ['url']

admin.site.register(Url, UrlAdmin)

class ImageAdmin(admin.ModelAdmin):

    search_fields = ['src']

admin.site.register(Image, ImageAdmin)

class LanguageAdmin(admin.ModelAdmin):

    list_display = ['name', 'iso2letter', 'iso3letter', 'popular', 'active']
    search_fields = ['name', 'iso2letter']

admin.site.register(Language, LanguageAdmin)

class UtterenceAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {'fields': ['language', 'utterence']}),
    ]

    list_display = ['utterence', 'language', 'count']
    list_filter = ['language']
    search_fields = ['utterence']
    ordering = ['-count']

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "translations" and getattr(self, 'obj', None):
            kwargs["queryset"] = Utterence.objects.all().filter(lexical_class=self.obj.lexical_class.id).exclude(keyword__language=self.obj.keyword.language.id).order_by('keyword__keyword')
        return super(UtterenceAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Utterence, UtterenceAdmin)

class LexicalDefinitionInline(admin.StackedInline):
    model = Keyword.lexical_definitions.through
    extra = 1

    def get_formset(self, request, obj=None, **kwargs):
        self.parent_obj = obj
        return super(LexicalDefinitionInline, self).get_formset(request, obj, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "translations" and getattr(self, 'parent_obj', None):
            kwargs["queryset"] = LexicalDefinition.objects.all().exclude(keyword__language=self.parent_obj.language.id).order_by('keyword__keyword')
        return super(LexicalDefinitionInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

class KeywordAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {'fields': ['language', 'keyword']}),
    ]

    inlines = [LexicalDefinitionInline]

    list_display = ['keyword', 'language', 'count']
    list_filter = ['language']
    search_fields = ['keyword']
    ordering = ['-count']

admin.site.register(Keyword, KeywordAdmin)

class KeywordUrlAdmin(admin.ModelAdmin):

    search_fields = ['keyword']

admin.site.register(KeywordUrl)

class LexicalDefinitionAdmin(admin.ModelAdmin):

    list_filter = ['keyword__language', 'lexical_class']

    def get_object(self, request, object_id, from_field=None):
        self.obj = super(LexicalDefinitionAdmin, self).get_object(request, object_id)
        return self.obj

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "translations" and getattr(self, 'obj', None):
            kwargs["queryset"] = LexicalDefinition.objects.all().filter(lexical_class=self.obj.lexical_class.id).exclude(keyword__language=self.obj.keyword.language.id).order_by('keyword__keyword')
        return super(LexicalDefinitionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(LexicalDefinition, LexicalDefinitionAdmin)

class LexicalClassAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {'fields': ['parent', 'name']}),
    ]

    search_fields = ['name']
    ordering = ['name']

admin.site.register(LexicalClass, LexicalClassAdmin)
