from django.contrib import admin
from users.models import *

class webuserAdmin(admin.ModelAdmin):
    list_display = ('userid', 'username','password','email','age','hobby')
admin.site.register(webuser,webuserAdmin)

class MetricAdmin(admin.ModelAdmin):
    list_display = ('Metricid','name', 'unit','purpose')
admin.site.register(Metric,MetricAdmin)

class DetectionPointAdmin(admin.ModelAdmin):
    list_display = ('id','num', 'name','location')
admin.site.register(DetectionPoint,DetectionPointAdmin)

class AlertAdmin(admin.ModelAdmin):
    list_display = ('Alertid', 'datetime','content','value')
admin.site.register(Alert,AlertAdmin)

class ThresholdAdmin(admin.ModelAdmin):
    list_display = ('id', 'indicator','indicator_id','threshold')
admin.site.register(Threshold,ThresholdAdmin)

class SensorDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'co_concentration','h2s_concentration','methane_concentration','ammonia_concentration','water_level','report_time')
admin.site.register(SensorData,SensorDataAdmin)

class fanAdmin(admin.ModelAdmin):
    list_display = ('id', 'zt')
admin.site.register(Fan,fanAdmin)