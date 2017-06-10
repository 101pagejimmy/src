from django.contrib import admin

# Register your models here.
from .models import Guide, GuideImage

class GuideModelAdmin(admin.ModelAdmin):
	list_display = ["guide_name", "updated", "timestamp"]
	list_display_links = ["updated"]
	list_filter = ["updated", "timestamp"]

	search_fields = ["guide_name", "story"]
	class Meta:
		model = Guide


admin.site.register(Guide, GuideModelAdmin)

admin.site.register(GuideImage)