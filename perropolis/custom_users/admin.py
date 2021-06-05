from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from custom_users.models import  *
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from import_export import resources, fields 
from import_export.admin import ImportExportModelAdmin 
from import_export.fields import Field
from SoCleanProject.constants import *
from django import forms
from webapp.filters import *

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.forms import ModelForm
from django.contrib.admin.widgets import FilteredSelectMultiple 
from django.contrib.auth.admin import GroupAdmin
from django.db.models.signals import post_save
from django.dispatch import receiver

#from 
# Register your models here.

class UserUpdateForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        #fields = '__all__'
        #, 'user_permissions'
        fields = ('name','password','last_name','phone', 'email', 'is_active','groups',)


    def __init__(self, *args, **kwargs):
        #self.request = kwargs.pop("request")
        #print(self)
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        #self.fields['name'].widget.attrs['disabled'] = True
        #print('entra siiiii',self)
        

    def clean_password(self):
        return self.initial["password"]

    def save(self, commit=True):

        user = super().save(commit=False)
        #print('acaaaaa',self.cleaned_data["groups"].first())
        user.is_admin = False
        #print(type(self.cleaned_data["groups"].first()))
        if self.cleaned_data["groups"].first().name != 'Colaboradores':
            #print("entra a validar")
            user.is_admin = True
        if commit:
            #pass
            user.save()
        return user
        #return user

class UserAddForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    #type_user = forms.CharField(widget=forms.HiddenInput({'value': PORTALUSER}))

    class Meta:
        model = CustomUser
        fields = ('name','last_name','phone', 'email', 'is_active','groups',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords no coinciden")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_admin = False

        if self.cleaned_data["groups"].first().name != 'Colaboradores':
            user.is_admin = True

        if commit:
            user.save()
        return user

class UserResource(resources.ModelResource):

    name_role = Field(column_name='Rol')
    name_active = Field(column_name='Activo')
    name_admin = Field(column_name='Admin')
    mail = Field(attribute='email',column_name="Correo Electronico")
    nombre = Field(attribute='name',column_name="Nombre")
    apellido = Field(attribute='last_name',column_name="Apellido") 
    telefono = Field(attribute='phone', column_name="Telefono")

    class Meta:
        
        fields = ('mail','nombre','apellido','telefono','name_role','name_active','name_admin',)
        export_order = fields
        model = CustomUser

    def dehydrate_name_role(self, user):
        return user.role

    def dehydrate_name_active(self, user):
        return "Si" if user.is_active == 1 else "No" 
         
    def dehydrate_name_admin(self, user):
        return "Si" if user.is_admin == 1 else "No" 


class PassRequestToFormViewMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class UserAdministrator(ImportExportModelAdmin):
    resource_class = UserResource
    readonly_fields = [
        'last_login',
    ]
    #groups_user = Field(column_name='Rol')
    list_display_links = ('full_name','email',)
    list_display = ('full_name','phone', 'email','groups_user','is_active','is_admin',)
    search_fields = ('name','phone', 'email',)
    list_filter = (UserFullNameFilter,UserRoleFilter,'is_active',)
    ordering = ()
    #fields = ['name','password','last_name','last_login','phone', 'email','role', 'is_active','is_admin','groups', 'user_permissions',]
    #filter_horizontal = ('groups', 'user_permissions',)

    fieldsets = ()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = CustomUser.objects.filter(groups__name__in=['Supervisor', 'Administrador','Colaboradores'])
        return qs


    def groups_user(self, user):
        groups = ''
        for g in user.groups.all():
            
            groups += "%s /" % g.name
        return groups
    groups_user.short_description = "Rol(es)"

    def get_form_kwargs(self):
        kwargs = super(UserAdministrator, self).get_form_kwargs()  # change to view name
        return dict(kwargs, groups=self.request.user.groups.values_list('name', flat=True))

    #def has_delete_permission(self, request, obj=None):
    #    return False

    #def has_add_permission(self, request, obj=None):
    #    return False


    def get_form(self, request, obj=None, **kwargs):
        self.form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if obj:
            #print("es super usuario",is_superuser)
            self.form = UserUpdateForm
        else:
            self.form = UserAddForm

        disabled_fields = set() 



        # Prevent non-superusers from editing their own permissions
        if (
            not is_superuser
            and obj is not None
            and obj == request.user
        ):
            disabled_fields |= {
                'is_staff',
                'is_superuser',
                'is_active',
                'groups',
                'user_permissions',
                'is_admin',
                'role',
            }

        for f in disabled_fields:
            if f in self.form.base_fields:
               self.form.base_fields[f].disabled = True

        #print(self.form)
        return self.form#super(UserAdministrator, self).get_form(request, obj, **kwargs)
    
    class Media:
        #this path may be any you want, 
        #just put it in your static folder
        js = ('js/admin/useradmin.js', )


class GroupForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        label='Users',
        queryset=CustomUser.objects.all(),
        required=False,
        widget=admin.widgets.FilteredSelectMultiple(
            "users", is_stacked=False))

    class Meta:
        model = Group
        exclude = ()  # since Django 1.8 this is needed
        widgets = {
            'permissions': admin.widgets.FilteredSelectMultiple(
                "permissions", is_stacked=False),
        }


class MyGroupAdmin(GroupAdmin):
    form = GroupForm

    def save_model(self, request, obj, form, change):
        # save first to obtain id
        super(GroupAdmin, self).save_model(request, obj, form, change)
        obj.user_set.clear()
        for user in form.cleaned_data['users']:
             obj.user_set.add(user)

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.form.base_fields['users'].initial = [o.pk for o in obj.user_set.all()]
        else:
            self.form.base_fields['users'].initial = []
        return GroupForm


# unregister and register again
admin.site.unregister(Group)
admin.site.register(Group, MyGroupAdmin)
