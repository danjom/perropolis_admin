from django.contrib import admin

# Register your models here.
from django.contrib.admin import register

from business_locations.forms import HotelRoomForm, LocationForm, ZoneForm
from business_locations.models import OpenSchedule, HotelRoom, Location, Employee, LocationService, ServiceCapacity, \
    Pricing, Zone, Webcam


class OpenScheduleInline(admin.TabularInline):
    model = OpenSchedule
    extra = 1
    readonly_fields = ('created_by', 'updated_by')

    def save_model(self, request, obj, form, change):
        user = request.user
        if not change:
            obj.created_by_id = user.pk
        obj.updated_by_id = user.pk
        super().save_model(request, obj, form, change)


class HotelRoomInline(admin.TabularInline):
    form = HotelRoomForm
    model = HotelRoom
    extra = 1
    readonly_fields = ('created_by', 'updated_by')

    def save_model(self, request, obj, form, change):
        user = request.user
        if not change:
            obj.created_by_id = user.pk
        obj.updated_by_id = user.pk
        super().save_model(request, obj, form, change)


@register(Location)
class LocationAdmin(admin.ModelAdmin):
    form = LocationForm
    list_display = ['name', 'phone_number', 'country', 'city', 'is_active', 'created_at', 'updated_at']
    list_display_links = list_display
    search_fields = ['name', 'country__name', 'city', 'phone_number']
    sortable_by = ['name', 'country', 'city', 'created_at']
    readonly_fields = ('created_by', 'updated_by')

    autocomplete_fields = ('country',)

    inlines = [OpenScheduleInline, HotelRoomInline]

    def save_model(self, request, obj, form, change):
        user = request.user
        if not change:
            obj.created_by_id = user.pk

        obj.updated_by_id = user.pk

        if getattr(obj, 'openschedule', None) is not None:
            if obj.openschedule.pk is None:
                obj.openschedule.created_by_id = user.pk
            obj.openschedule.updated_by_id = user.pk
        if getattr(obj, 'hotelroom', None) is not None:
            if obj.hotelroom.pk is None:
                obj.hotelroom.created_by_id = user.pk
            obj.hotelroom.updated_by_id = user.pk

        super().save_model(request, obj, form, change)


@register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_email', 'location', 'is_active', 'created_at', 'updated_at']
    list_display_links = list_display
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'location__name']
    sortable_by = ['user', 'location', 'created_at', 'updated_at']

    autocomplete_fields = ('user', 'location')

    def user_name(self, obj):
        return obj.user.get_full_name()

    def user_email(self, obj):
        return obj.user.email

    readonly_fields = ('created_by', 'updated_by')

    def save_model(self, request, obj, form, change):
        user = request.user
        if not change:
            obj.created_by_id = user.pk
        obj.updated_by_id = user.pk
        super().save_model(request, obj, form, change)

#
# class ServiceCapacityInline(admin.TabularInline):
#     model = ServiceCapacity
#     extra = 1


class PricingInline(admin.TabularInline):
    # TODO: Update created_by and updated_by fileds in background automatically
    model = Pricing
    extra = 1
    readonly_fields = ('created_by', 'updated_by')


@register(LocationService)
class LocationServiceAdmin(admin.ModelAdmin):
    list_display = ['service', 'location', 'is_active', 'created_at', 'updated_at']
    list_display_links = list_display
    search_fields = ['service__name', 'location__name']
    sortable_by = ['service', 'location', 'created_at', 'updated_at']

    autocomplete_fields = ['service', 'location']

    inlines = [PricingInline]

    readonly_fields = ('created_by', 'updated_by')

    def save_model(self, request, obj, form, change):
        user = request.user
        if not change:
            obj.created_by_id = user.pk
        obj.updated_by_id = user.pk

        super().save_model(request, obj, form, change)


@register(Pricing)
class PricingAdmin(admin.ModelAdmin):
    list_display = ['service', 'location', 'specie', 'pet_size', 'price', 'created_at', 'updated_at']
    list_display_links = list_display
    search_fields = ['searvice__name', 'location__name', 'specie__name']
    sortable_by = ['service', 'location', 'specie', 'created_at', 'updated_at']

    autocomplete_fields = ('service', 'location', 'specie')

    readonly_fields = ('created_by', 'updated_by')

    def save_model(self, request, obj, form, change):
        user = request.user
        if not change:
            obj.created_by_id = user.pk
        obj.updated_by_id = user.pk

        super().save_model(request, obj, form, change)


@register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    form = ZoneForm
    list_display = ['name', 'service', 'location', 'created_at', 'updated_at']
    list_display_links = list_display
    search_fields = ['name', 'service__name', 'location__name']
    sortable_by = ['name', 'service', 'location', 'created_at', 'updated_at']

    autocomplete_fields = ('service', 'location')

    readonly_fields = ['created_by', 'updated_by']

    def save_model(self, request, obj, form, change):
        user = request.user
        if not change:
            obj.created_by_id = user.pk
        obj.updated_by_id = user.pk

        super().save_model(request, obj, form, change)


@register(Webcam)
class WebcamAdmin(admin.ModelAdmin):
    list_display = ['alias', 'location', 'zone', 'livestream_available', 'is_active', 'created_at', 'updated_at']
    list_display_links = list_display
    search_fields = ['alias', 'code', 'location__name', 'zone__name']
    sortable_by = ['alias', 'code', 'location', 'zone', 'created_at', 'updated_at']

    autocomplete_fields = ('location', 'zone')

    readonly_fields = ('created_by', 'updated_by')

    def save_model(self, request, obj, form, change):
        user = request.user
        if not change:
            obj.created_by_id = user.pk
        obj.updated_by_id = user.pk

        super().save_model(request, obj, form, change)
