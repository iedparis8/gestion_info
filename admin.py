from __future__ import unicode_literals
# coding=utf-8
from django.contrib import admin
from gestion_info.models import TypeEquipement, Salle, Equipement, TypeBaseEquipement


class EquipementInline(admin.TabularInline):
    model = Equipement
    extra = 1


class EquipementAdmin(admin.ModelAdmin):
    search_fields = ['salle__label']


class SalleAdmin(admin.ModelAdmin):
    inlines = [EquipementInline]
    search_fields = ['label', 'equipements__mac_adresse']
    list_display = ['__str__', 'liste_equipement', 'config_dhcp']
    readonly_fields = ['liste_equipement', 'config_dhcp']
    ordering = ['label']

    def liste_equipement(self, obj):
        result = ''
        for equipement in obj.equipements.all():
            result += str(equipement) + '<br>'
        return result
    liste_equipement.allow_tags = True

    def config_dhcp(self, obj):
        result = "#{}<br>".format(obj.label)
        for equipement in obj.equipements.filter(type__base__code='CL'):
            if equipement.type.base.code == 'CL' and equipement.ip:
                result += 'host {} {{ hardware ethernet {}; fixed-address {}; }} <br>'.format(
                    equipement.name.strip().replace(' ', '_'),
                    str(equipement.mac_adresse).lower(),
                    equipement.ip)
            else:
                result += 'host {} {{ hardware ethernet {}; }} <br>'.format(equipement.name.strip().replace(' ', '_'),
                                                                        str(equipement.mac_adresse).lower())
        imprimantes = obj.equipements.filter(type__base__code='IMP')
        if imprimantes:
            result += '<hr> Imprimante <br>'
        for equipement in obj.equipements.filter(type__base__code='IMP'):
            result += 'host {} {{ hardware ethernet {}; fixed-address {}; }} <br>'.format(
                equipement.name.strip().replace(' ', '_'),
                str(equipement.mac_adresse).lower(),
                equipement.ip)

        return result
    config_dhcp.allow_tags = True


admin.site.register(TypeEquipement)
admin.site.register(Equipement, EquipementAdmin)
admin.site.register(Salle, SalleAdmin)
admin.site.register(TypeBaseEquipement)
