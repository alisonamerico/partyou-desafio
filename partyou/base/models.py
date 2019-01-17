from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:  # pragma: no cover
            raise ValueError('The given username must be set')  # pragma: no cover
        email = self.normalize_email(email)  # pragma: no cover
        username = self.model.normalize_username(username)  # pragma: no cover
        user = self.model(username=username, email=email, **extra_fields)  # pragma: no cover
        user.set_password(password)  # pragma: no cover
        user.save(using=self._db)  # pragma: no cover
        return user  # pragma: no cover

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)  # pragma: no cover
        extra_fields.setdefault('is_superuser', False)  # pragma: no cover
        return self._create_user(username, email, password, **extra_fields)  # pragma: no cover

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)  # pragma: no cover
        extra_fields.setdefault('is_superuser', True)  # pragma: no cover

        if extra_fields.get('is_staff') is not True:  # pragma: no cover
            raise ValueError('Superuser must have is_staff=True.')  # pragma: no cover
        if extra_fields.get('is_superuser') is not True:  # pragma: no cover
            raise ValueError('Superuser must have is_superuser=True.')  # pragma: no cover

        return self._create_user(username, email, password, **extra_fields)  # pragma: no cover


class User(AbstractBaseUser, PermissionsMixin):
    """
    App base User class.

    Email and password are required. Other fields are optional.
    """

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s' % (self.first_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
