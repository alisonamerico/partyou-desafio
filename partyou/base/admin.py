from django.conf import settings
from django.contrib import admin, messages
from django.contrib.admin.options import IS_POPUP_VAR
from django.contrib.admin.utils import unquote
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import (
    AdminPasswordChangeForm, UserChangeForm, UserCreationForm,
)
from django.core.exceptions import PermissionDenied
from django.db import router, transaction
from django.http import Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.utils.translation import gettext, gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from partyou.base.models import User

csrf_protect_m = method_decorator(csrf_protect)
sensitive_post_parameters_m = method_decorator(sensitive_post_parameters())


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None
    fieldsets = (
        (None, {'fields': ('first_name', 'email', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'email', 'password1', 'password2'),
        }),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('email', 'first_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'email')
    ordering = ('first_name',)
    filter_horizontal = ('groups', 'user_permissions',)

    def get_fieldsets(self, request, obj=None):
        if not obj:  # pragma: no cover
            return self.add_fieldsets  # pragma: no cover
        return super().get_fieldsets(request, obj)  # pragma: no cover

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}  # pragma: no cover
        if obj is None:  # pragma: no cover
            defaults['form'] = self.add_form  # pragma: no cover
        defaults.update(kwargs)  # pragma: no cover
        return super().get_form(request, obj, **defaults)  # pragma: no cover

    def get_urls(self):
        return [
            path(
                '<id>/password/',
                self.admin_site.admin_view(self.user_change_password),
                name='auth_user_password_change',
            ),
        ] + super().get_urls()

    def lookup_allowed(self, lookup, value):
        # Don't allow lookups involving passwords.
        return not lookup.startswith('password') and super().lookup_allowed(lookup, value)  # pragma: no cover

    @sensitive_post_parameters_m
    @csrf_protect_m
    def add_view(self, request, form_url='', extra_context=None):
        with transaction.atomic(using=router.db_for_write(self.model)):  # pragma: no cover
            return self._add_view(request, form_url, extra_context)  # pragma: no cover

    def _add_view(self, request, form_url='', extra_context=None):
        # It's an error for a user to have add permission but NOT change
        # permission for users. If we allowed such users to add users, they
        # could create superusers, which would mean they would essentially have
        # the permission to change users. To avoid the problem entirely, we
        # disallow users from adding users if they don't have change
        # permission.
        if not self.has_change_permission(request):  # pragma: no cover
            if self.has_add_permission(request) and settings.DEBUG:  # pragma: no cover
                # Raise Http404 in debug mode so that the user gets a helpful
                # error message.
                raise Http404(  # pragma: no cover
                    'Your user does not have the "Change user" permission. In '
                    'order to add users, Django requires that your user '
                    'account have both the "Add user" and "Change user" '
                    'permissions set.')
            raise PermissionDenied  # pragma: no cover
        if extra_context is None:  # pragma: no cover
            extra_context = {}  # pragma: no cover
        username_field = self.model._meta.get_field(self.model.USERNAME_FIELD)  # pragma: no cover
        defaults = {  # pragma: no cover
            'auto_populated_fields': (),
            'username_help_text': username_field.help_text,
        }
        extra_context.update(defaults)  # pragma: no cover
        return super().add_view(request, form_url, extra_context)  # pragma: no cover

    @sensitive_post_parameters_m
    def user_change_password(self, request, id, form_url=''):
        if not self.has_change_permission(request):  # pragma: no cover
            raise PermissionDenied  # pragma: no cover
        user = self.get_object(request, unquote(id))  # pragma: no cover
        if user is None:  # pragma: no cover
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {  # pragma: no cover
                'name': self.model._meta.verbose_name,  # pragma: no cover
                'key': escape(id),
            })
        if request.method == 'POST':  # pragma: no cover
            form = self.change_password_form(user, request.POST)   # pragma: no cover
            if form.is_valid():  # pragma: no cover
                form.save()  # pragma: no cover
                change_message = self.construct_change_message(request, form, None)  # pragma: no cover
                self.log_change(request, user, change_message)  # pragma: no cover
                msg = gettext('Password changed successfully.')  # pragma: no cover
                messages.success(request, msg)  # pragma: no cover
                update_session_auth_hash(request, form.user)  # pragma: no cover
                return HttpResponseRedirect(  # pragma: no cover
                    reverse(
                        '%s:%s_%s_change' % (
                            self.admin_site.name,
                            user._meta.app_label,
                            user._meta.model_name,
                        ),
                        args=(user.pk,),
                    )
                )
        else:
            form = self.change_password_form(user)  # pragma: no cover

        fieldsets = [(None, {'fields': list(form.base_fields)})]  # pragma: no cover
        adminForm = admin.helpers.AdminForm(form, fieldsets, {})  # pragma: no cover

        context = {  # pragma: no cover
            'title': _('Change password: %s') % escape(user.get_username()),
            'adminForm': adminForm,
            'form_url': form_url,
            'form': form,
            'is_popup': (IS_POPUP_VAR in request.POST or
                         IS_POPUP_VAR in request.GET),
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'original': user,
            'save_as': False,
            'show_save': True,
            **self.admin_site.each_context(request),
        }

        request.current_app = self.admin_site.name  # pragma: no cover

        return TemplateResponse(  # pragma: no cover
            request,
            self.change_user_password_template or
            'admin/auth/user/change_password.html',
            context,
        )

    def response_add(self, request, obj, post_url_continue=None):
        """
        Determine the HttpResponse for the add_view stage. It mostly defers to
        its superclass implementation but is customized because the User model
        has a slightly different workflow.
        """
        # We should allow further modification of the user just added i.e. the
        # 'Save' button should behave like the 'Save and continue editing'
        # button except in two scenarios:
        # * The user has pressed the 'Save and add another' button
        # * We are adding a user in a popup
        if '_addanother' not in request.POST and IS_POPUP_VAR not in request.POST:  # pragma: no cover
            request.POST = request.POST.copy()  # pragma: no cover
            request.POST['_continue'] = 1  # pragma: no cover
        return super().response_add(request, obj, post_url_continue)  # pragma: no cover
