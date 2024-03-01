import jwt
from django.db import models
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class Cities(models.Model):
    city_id = models.IntegerField(primary_key=True)
    city_name = models.CharField(max_length=256)


class Organization(models.Model):
    org_id = models.IntegerField(primary_key=True)
    org_name = models.CharField(max_length=256)
    org_code = models.CharField(max_length=128)


class TicketType(models.Model):
    type_id = models.IntegerField(primary_key=True)
    type_name = models.CharField(max_length=256)


class User(AbstractBaseUser, PermissionsMixin):
    fio = models.CharField(max_length=256, null=False)
    username = models.CharField(db_index=True, max_length=255, unique=True)
    password = models.CharField(max_length=128, null=False)
    active_status = models.BooleanField(default=False)
    city_id = models.ForeignKey(Cities.city_id, on_delete=models.CASCADE())
    email = models.EmailField(db_index=True, unique=True)
    phone = models.CharField(max_length=11)
    org_id = models.ForeignKey(Organization.org_id, on_delete=models)

    DoesNotExist = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': str(int(dt.timestamp()))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.encode('utf-8')


class Ticket(models.Model):
    ticket_id = models.IntegerField(primary_key=True)
    staff_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    org_id = models.ForeignKey(Organization.org_id, on_delete=models.CASCADE, null=False)
    ticket_type = models.ForeignKey(TicketType.type_id, on_delete=models.CASCADE, null=False)
    created_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def create_ticket(self, ticket_type, staff_id, org_id):
        if not ticket_type and not staff_id and not org_id:
            raise Exception('Незаполнены обязательные поля')



class Document(models.Model):
    ticket_id = models.ForeignKey(Ticket, on_delete=models)
    html_result_link = models.CharField(max_length=256)
    pdf_result_link = models.CharField(max_length=256)
    created_date = models.DateTimeField()