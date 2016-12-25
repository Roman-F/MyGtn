from django.contrib import admin
import models

admin.site.register([models.EntityNaturalPerson,
                    models.EntityVehicle,
                    models.VehicleColor,
                    models.VehicleEngine,
                    models.VehicleBrand,
                    models.BrandEngine,
                    models.OrganizationIssue,
                    models.Country,
                    models.Manufacturer,
                    models.KindVehicle,
                    models.TypeProp,
                    models.TypeAndGroupVehicle])
# Register your models here.
