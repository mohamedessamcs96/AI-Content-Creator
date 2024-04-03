from django.contrib import admin
from .models import UserAdmin,HomeInfo,ProjectManger,ContentCreator,Types,Style,TargetAudience
# Register your models here.

 
 
 
admin.site.site_header=''
admin.site.register(HomeInfo)
admin.site.register(Types)
admin.site.register(ProjectManger)
admin.site.register(UserAdmin)
admin.site.register(TargetAudience)
admin.site.register(Style)
admin.site.register(ContentCreator)

