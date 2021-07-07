from cloudinary.models import CloudinaryField
from django.contrib import admin, messages

from django.contrib.admin import register
from django.contrib.admin.utils import unquote
from django.contrib.admin.widgets import AdminFileWidget
from django.contrib.auth.admin import sensitive_post_parameters_m
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _, gettext

from customers_and_pets.forms import PetFeedingForm, PetMedicationForm, PetBelongingForm, PetMedicalRecordsForm, \
    CustomerCreationForm, CustomerChangeForm, CustomerPasswordChangeForm
from customers_and_pets.models import Customer, Pet, PetImage, PetVideo, PetFeeding, PetMedication, PetBelonging, \
    PetMedicalRecords, UserPet
from shared.admin import ModelAdminWithSaveOverrideForCreationAndUpdate, ModelAdminChangeDisabled


@register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None
    formfield_overrides = {
        CloudinaryField: {'widget': AdminFileWidget},
    }

    list_display = ['name', 'email', 'country', 'is_active', 'is_blocked', 'created_at', 'updated_at']
    list_display_links = list_display
    search_fields = ['name', 'email', 'country__name']
    sortable_by = ['name', 'country', 'created_at', 'updated_at']

    fieldsets = (
        (None, {'fields': ('name', 'email', 'password', 'country', 'email_validated', 'phone_number',
                           'phone_validated', 'profile_pic_url', 'is_active', 'is_blocked', 'profile_pic')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'country', 'password1', 'password2'),
        }),
    )

    readonly_fields = ('profile_pic',)

    form = CustomerChangeForm
    add_form = CustomerCreationForm

    change_password_form = CustomerPasswordChangeForm

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    def get_urls(self):
        return [
            path(
                '<id>/password/',
                self.admin_site.admin_view(self.user_change_password),
                name='auth_user_password_change',
            ),
        ] + super().get_urls()

    def response_add(self, request, obj, post_url_continue=None):
        if '_addanother' not in request.POST and '_popup' not in request.POST:
            request.POST = request.POST.copy()
            request.POST['_continue'] = 1
        return super().response_add(request, obj, post_url_continue)

    @sensitive_post_parameters_m
    def user_change_password(self, request, id, form_url=''):
        customer = self.get_object(request, unquote(id))
        if not self.has_change_permission(request, request.user):
            raise PermissionDenied
        if customer is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {
                'name': self.model._meta.verbose_name,
                'key': escape(id),
            })
        if request.method == 'POST':
            form = self.change_password_form(customer, request.POST)
            if form.is_valid():
                form.save()
                change_message = self.construct_change_message(request, form, None)
                self.log_change(request, customer, change_message)
                msg = gettext('Password changed successfully.')
                messages.success(request, msg)
                return HttpResponseRedirect(
                    reverse(
                        '%s:%s_%s_change' % (
                            self.admin_site.name,
                            customer._meta.app_label,
                            customer._meta.model_name,
                        ),
                        args=(customer.pk,),
                    )
                )
        else:
            form = self.change_password_form(customer)

        fieldsets = [(None, {'fields': list(form.base_fields)})]
        adminForm = admin.helpers.AdminForm(form, fieldsets, {})

        context = {
            'title': _('Change password: %s') % escape(customer.name),
            'adminForm': adminForm,
            'form_url': form_url,
            'form': form,
            'is_popup': ('_popup' in request.POST or
                         '_popup' in request.GET),
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'original': customer,
            'save_as': False,
            'show_save': True,
            **self.admin_site.each_context(request),
        }

        request.current_app = self.admin_site.name

        return TemplateResponse(
            request,
            self.change_user_password_template or
            'admin/auth/user/change_password.html',
            context,
        )

    def save_model(self,  request, obj, form, change):
        if 'profile_pic_url' in form.changed_data:
            profile_pic = Customer.objects.values_list('profile_pic_url', flat=True).filter(pk=obj.pk).first()
            if profile_pic is not None:
                Customer.delete_profile_pic_from_cloudnary(profile_pic.public_id)
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        profile_pic = Customer.objects.values_list('profile_pic_url', flat=True).filter(pk=obj.pk).first()
        if profile_pic is not None:
            Customer.delete_logo_from_cloudnary(profile_pic.public_id)
        super().delete_model(request, obj)


class PetFeedingInline(admin.TabularInline):
    form = PetFeedingForm
    model = PetFeeding
    extra = 1
    readonly_fields = ('created_by', 'admin_created', 'updated_by', 'admin_updated')


class PetMedicationInline(admin.TabularInline):
    form = PetMedicationForm
    model = PetMedication
    extra = 1
    readonly_fields = ('created_by', 'admin_created', 'updated_by', 'admin_updated')


class PetBelongingInline(admin.TabularInline):
    form = PetBelongingForm
    model = PetBelonging
    extra = 1


class PetImageInline(admin.TabularInline):
    model = PetImage
    readonly_fields = ('version', 'image_small')
    extra = 1

    def has_change_permission(self, request, obj=None):
        return False


class PetVideoInline(admin.TabularInline):
    model = PetVideo
    readonly_fields = ('version',)
    extra = 1

    def has_change_permission(self, request, obj=None):
        return False


class PetMedicalRecordsInline(admin.TabularInline):
    form = PetMedicalRecordsForm
    model = PetMedicalRecords
    extra = 1
    readonly_fields = ('event', 'created_by', 'admin_created', 'updated_by', 'admin_updated')
    autocomplete_fields = ('action', )


class UserPetInline(admin.TabularInline):
    model = UserPet
    extra = 1
    readonly_fields = ('created_by', 'admin_created', 'updated_by', 'admin_updated')


@register(Pet)
class PetAdmin(ModelAdminWithSaveOverrideForCreationAndUpdate):
    list_display = ['name', 'breed', 'birth_date', 'created_at', 'updated_at']
    list_display_links = list_display
    search_fields = ['name', 'breed_name', 'birth_date']
    sortable_by = ['name', 'breed', 'birth_date', 'created_at']

    readonly_fields = ('created_by', 'admin_created', 'updated_by', 'admin_updated', 'last_service', 'profile_pic')

    inlines = [PetFeedingInline, PetMedicationInline, PetBelongingInline, PetMedicalRecordsInline, PetImageInline,
               PetVideoInline, UserPetInline]

    def save_model(self,  request, obj, form, change):
        """
        Override Pet's save method.
        Delete image from cloudinary when it is removed from the system!
        """
        if 'profile_pic_url' in form.changed_data:
            profile_pic = Customer.objects.values_list('profile_pic_url', flat=True).filter(pk=obj.pk).first()
            if profile_pic is not None:
                Customer.delete_profile_pic_from_cloudnary(profile_pic.public_id)

        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        """
        Override Pet's delete method.
        Delete image from cloudinary when Pet is removed from the system!
        """
        profile_pic = Pet.objects.values_list('profile_pic_url', flat=True).filter(pk=obj.pk).first()
        if profile_pic is not None:
            Pet.delete_profile_pic_from_cloudnary(profile_pic.public_id)
        super().delete_model(request, obj)

    def save_formset(self, request, form, formset, change):
        """
        Given an inline formset save it to the database.
        """
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            if instance.pk is None:
                instance.created_by = request.user
                instance.admin_created = request.user.is_superuser
            instance.updated_by = request.user
            instance.admin_updated = request.user.is_superuser
            instance.save()
        formset.save_m2m()


@register(PetImage)
class PetImageAdmin(ModelAdminChangeDisabled):
    list_display = ['image_small', 'pet', 'created_at']
    list_display_links = list_display
    search_fields = ['pet__name']
    sortable_by = ['pet', 'created_at']

    readonly_fields = ('version', 'image')


@register(PetVideo)
class PetVideoAdmin(ModelAdminChangeDisabled):
    list_display = ['name', 'pet', 'created_at']
    list_display_links = list_display
    search_fields = ['name', 'pet__name']
    sortable_by = ['name', 'pet', 'created_at']

    readonly_fields = ('version',)


@register(PetFeeding)
class PetFeedingAdmin(ModelAdminWithSaveOverrideForCreationAndUpdate):
    list_display = ['pet', 'food', 'times_per_day', 'is_active', 'created_at', 'updated_at']
    list_display_links = list_display
    search_fields = ['pet__name', 'food__name']
    sortable_by = ['pet', 'food', 'is_active', 'created_at', 'updated_at']

    readonly_fields = ('created_by', 'admin_created', 'updated_by', 'admin_updated')


@register(PetMedication)
class PetMedicationAdmin(ModelAdminWithSaveOverrideForCreationAndUpdate):
    list_display = ['pet', 'drug', 'dose', 'start_date', 'end_date', 'is_active', 'created_at', 'updated_at']
    list_display_links = list_display
    search_fields = ['pet__name', 'drug__name']
    sortable_by = ['pet', 'drug', 'created_at', 'is_active', 'updated_at']

    readonly_fields = ('created_by', 'admin_created', 'updated_by', 'admin_updated')


@register(PetBelonging)
class PetBelongingAdmin(admin.ModelAdmin):
    list_display = ['pet', 'name', 'belongings_type', 'favorite', 'created_at', 'updated_at']
    list_display_links = list_display
    search_fields = ['pet__name', 'name']
    sortable_by = ['pet', 'name', 'created_at', 'updated_at']


@register(PetMedicalRecords)
class PetMedicalRecordsAdmin(ModelAdminWithSaveOverrideForCreationAndUpdate):
    list_display = ['pet', 'event', 'action', 'event_date', 'created_at', 'updated_at']
    list_display_links = list_display
    search_fields = ['pet__name', 'event__name', 'action__name']
    sortable_by = ['pet', 'event', 'action', 'created_at', 'updated_at']

    readonly_fields = ('created_by', 'admin_created', 'updated_by', 'admin_updated')



