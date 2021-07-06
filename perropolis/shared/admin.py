from django.contrib import admin


class ModelAdminWithSaveOverrideForCreationAndUpdate(admin.ModelAdmin):
    def save_model(self,  request, obj, form, change):
        """
        Override Admin's save method.
        Update created_by, updated_by, admin_created and admin_updated fields
        """
        user = request.user
        if not change:
            obj.created_by_id = user.pk
            obj.admin_created = user.is_superuser

        obj.updated_by_id = user.pk
        obj.admin_updated = user.is_superuser
        super().save_model(request, obj, form, change)


class ModelAdminChangeDisabled(admin.ModelAdmin):
    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        extra_context['show_save_and_add_another'] = False

        return super().change_view(request, object_id, extra_context=extra_context)
