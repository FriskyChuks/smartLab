from django.db.models import Q
from django.db.models.expressions import F
from django.urls import reverse
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class PatientQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)

	def search(self, query):
		lookups = ( 
					Q(id__iexact=query)|
					Q(first_name__icontains=query)| 
					Q(last_name__icontains=query) |
					Q(date_of_birth__iexact=query)|
					Q(phone_1__iexact=query)
				  )
		return self.filter(lookups).distinct()


class PatientManager(models.Manager):
	def search(self, query):
		return self.get_queryset().active().search(query)

	def get_queryset(self):
		return PatientQuerySet(self.model, using=self._db)


MARITAL_STATUS = (
		('single', 'Single'),
		('married', 'Married'),
		('divorced', 'Divorced'),
	)

GENDER = (
		('male', 'Male'),
		('female', 'Female'),
	)

class Patient(models.Model):
	foto			= models.ImageField(null=True, blank=True, upload_to="patients/")
	first_name      = models.CharField(max_length=50)
	last_name       = models.CharField(max_length=50)
	other_names     = models.CharField(max_length=50)
	gender          = models.CharField(max_length=10, choices=GENDER)
	date_of_birth   = models.DateField()
	marital_status  = models.CharField(max_length=10, choices=MARITAL_STATUS, null=True, blank=True)
	phone_1         = models.CharField(max_length=11, unique=True)
	phone_2         = models.CharField(max_length=11, null=True, blank=True)
	address         = models.TextField(null=True, blank=True)
	date_created    = models.DateTimeField(auto_now_add=True, auto_now=False)
	last_updated    = models.DateTimeField(auto_now_add=False, auto_now=True)
	active          = models.BooleanField(default=True)
	created_by      = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

	objects = PatientManager()

	def __str__(self):
		return f"{self.first_name} {self.last_name}"


	def get_absolute_url(self):
		return reverse("patient_detail", kwargs={"id": self.id})

	class Meta:
		unique_together = ('first_name', 'last_name', 'date_of_birth')