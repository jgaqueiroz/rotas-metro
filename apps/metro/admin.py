from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminMixin
from apps.metro.models import Linha, Estacao, Destino

admin.site.site_header = 'Metrô do Recife (Rotas)'
admin.site.site_title  = 'Metrô do Recife (Rotas)' 
admin.site.index_title  = 'Administração da Aplicação' 

@admin.register(Estacao)
class EstacaoAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("nome", "cor_e_linha")
    list_filter = ["linha"]
    search_fields = ["nome"]
    
    def cor_e_linha(self, obj):
        return format_html(
            '<span style="color:{0}">&#9632;</span> {1}', obj.linha.cor, obj.linha.nome
        )

    cor_e_linha.short_description = 'linha'
    cor_e_linha.allow_tags = True

@admin.register(Linha)
class LinhaAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("cor_e_linha",)

    def cor_e_linha(self, obj):
        return format_html(
            '<span style="color:{0}">&#9632;</span> {1}', obj.cor, obj.nome
        )

    cor_e_linha.short_description = 'linha'
    cor_e_linha.allow_tags = True

@admin.register(Destino)
class DestinoAdmin(SortableAdminMixin, admin.ModelAdmin):
    #list_display = ["nome", "origem", "destino"]
    list_display = ["nome", "custom_origem_destino"]

    def custom_origem_destino2(self, obj):
        return format_html(
            '{0} <span style="color:{1}">&#9632;</span> {2} &#10230; {3} <span style="color:{4}">&#9632;</span> {5}', 
            obj.origem.nome, obj.origem.linha.cor, obj.origem.linha, obj.destino.nome, obj.destino.linha.cor, obj.destino.linha, 
        )

    custom_origem_destino2.short_description = format_html('origem &#10230; destino')
    custom_origem_destino2.allow_tags = True

    def custom_origem_destino(self, obj):
        return format_html(
            '<span style="color:{0}">&#9632;</span> {1} &#10230; <span style="color:{2}">&#9632;</span> {3}', 
            obj.origem.linha.cor, obj.origem.nome, obj.destino.linha.cor, obj.destino.nome 
        )

    custom_origem_destino.short_description = format_html('origem &#10230; destino')
    custom_origem_destino.allow_tags = True
    #list_filter = ["origem", "destino"]
