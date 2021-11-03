from django.contrib import admin

from .models import RadiologyService, RadiologyRequest, RadiologyServiceType, RadiologyReport

admin.site.register(RadiologyServiceType)

admin.site.register(RadiologyService)

admin.site.register(RadiologyRequest)

admin.site.register(RadiologyReport)
