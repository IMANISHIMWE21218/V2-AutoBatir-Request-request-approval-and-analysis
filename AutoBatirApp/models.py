from django.db import models

# Create your models here.

from tkinter import CASCADE
from django.db import models
from django.forms import EmailField, ImageField
import uuid
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.

class User(AbstractUser):
    is_engineer = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    
    


class NationalID(models.Model):
    GENDER=(
            ('male','male'),
            ('female','female'),
            )
    id = models.AutoField(primary_key=True, default=None)
    National_id = models.IntegerField(unique= True,  null=True, blank=True)
    NIDphoto = models.ImageField(upload_to='docs_other/id_photo/', null=True, blank=True)
    FirstName = models.CharField(max_length=35, null=True, blank=True) 
    LastName = models.CharField(max_length=35, null=True, blank=True)
    Districts = models.CharField(max_length=35, null=True, blank=True)
    Sectors = models.CharField(max_length=35, null=True, blank=True)
    Cells = models.CharField(max_length=35, null=True, blank=True)
    villages = models.CharField(max_length=35, null=True, blank=True)
    Address_street = models.CharField(max_length=1000, null=True, blank=True)
    gender= models.CharField(max_length=10, null=True, blank=True, choices=GENDER)
    dob = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        db_table = "National_ID"

    def __str__(self):
        return str(self.National_id) +' '+ self.FirstName + ' '+ self.LastName


class  UPI(models.Model):
    id = models.AutoField(primary_key=True, default=None)
    user= models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True)
    UPI_id = models.CharField(max_length=25, unique= True, null=True, blank=True)
    parcel_ID=models.IntegerField(null=True, blank=True)
    NationalID = models.ForeignKey(NationalID, on_delete=models.SET_NULL, null=True, blank=True)
    Districts = models.CharField(max_length=35, null=True, blank=True)
    Sectors = models.CharField(max_length=35, null=True, blank=True)
    Cells = models.CharField(max_length=35, null=True, blank=True)
    villages = models.CharField(max_length=35, null=True, blank=True)
    MainZonecode= models.CharField(max_length=25, null=True, blank=True)
    MainZoning= models.CharField(max_length=50, null=True, blank=True)
    Phase= models.CharField(max_length=25, null=True, blank=True)
    Year_of_Implementation=models.DateTimeField(null=True)
    Area_in_square_meters= models.IntegerField(null=True, blank=True)
    Zoning_with_Areas =  models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = "UPI"

    def __str__(self):
        return str(self.UPI_id) +' '+self.Districts + ' '+ str(self.NationalID.National_id)


class Registration(models.Model):
    GENDER=(
            ('male','male'),
            ('female','female'),
            )
    id = models.AutoField(primary_key=True, default=None)
    user= models.OneToOneField(User,on_delete=models.CASCADE, null=True, blank=True)
    NationalID = models.IntegerField(unique= True,  null=True, blank=True)
    FirstName = models.CharField(max_length=35, null=True, blank=True) 
    LastName = models.CharField(max_length=35, null=True, blank=True)
    email = models.EmailField(null=True, blank=False)
    # profile_Picture = models.ImageField(upload_to='docs_other/profiles/', null=True, blank=True)
    phone = models.CharField(max_length=13, blank=True, null=True)
    Districts = models.CharField(max_length=35, null=True, blank=True)
    Sectors = models.CharField(max_length=35, null=True, blank=True)
    Cells = models.CharField(max_length=35, null=True, blank=True)
    villages = models.CharField(max_length=35, null=True, blank=True)
    Address_street = models.CharField(max_length=1000, null=True, blank=True)
    gender= models.CharField(max_length=10, null=True, blank=True, choices=GENDER)
    RegistrationDate = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "Registration"

    def __str__(self):
        return  self.FirstName +' '+self.LastName
        # str(self.NationalID)+' '+
         
        # 

class Permit(models.Model):
    id = models.UUIDField( default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE, null=True, blank=True)
    UPI = models.ForeignKey(UPI, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="UPI related to permit")
    ConstructionPlan = models.FileField(upload_to='docs_const_plan/pdfs/', null=True, blank=False)
    LandOwnerShipDoc = models.FileField(upload_to='docs_landownership/pdfs/', null=True, blank=False)
    Paymentproof = models.FileField(upload_to='Bankslip/pdfs/',  null=True, blank=True)
    OtherDoc = models.FileField(upload_to='docs_other/pdfs/',  null=True, blank=True)
    MainZonecode= models.CharField(max_length=25, null=True, blank=False)
    Date = models.DateTimeField(auto_now_add=True)
    Status = models.CharField( max_length=10, null=True, blank=True, default='pending')
    ApprovedBy = models.CharField( max_length=35, null=True, blank=True)
    updated_at_issuedDate = models.DateTimeField(auto_now=True)
    comment = models.TextField(null=True, blank=True)


    class Meta:
        db_table = "Permit"

    def __str__(self):
        return self.MainZonecode +' '+ str(self.Date) +' '+ str(self.UPI.UPI_id)

class ArchivedPermit(models.Model):
    id = models.UUIDField( default=uuid.uuid4, primary_key=True,  editable=False)
    Archivedid = models.CharField(max_length=25, null=True, blank=True)
    # registration = models.OneToOneField(Registration, on_delete=models.CASCADE, null=True, blank=True)
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, null=True, blank=True)
    UPI = models.ForeignKey(UPI, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="UPI related to permit")
    ConstructionPlan = models.FileField(upload_to='docs_const_plan/pdfs/')
    LandOwnerShipDoc = models.FileField(upload_to='docs_landownership/pdfs/', null=True, blank=True)
    Paymentproof = models.FileField(upload_to='Bankslip/pdfs/',  null=True, blank=True)
    OtherDoc = models.FileField(upload_to='docs_other/pdfs/',  null=True, blank=True)
    MainZonecode= models.CharField(max_length=25, null=True, blank=True)
    Date = models.DateTimeField()
    Status = models.CharField( max_length=10, null=True, blank=True, default='pending')
    ApprovedBy = models.CharField( max_length=35, null=True, blank=True)
    updated_at_issuedDate = models.DateTimeField()
    comment = models.TextField(null=True, blank=True)


class  Engineer(models.Model):
    GENDER=(
    ('male','male'),
    ('female','female'),
    )
    id = models.AutoField(primary_key=True, default=None)
    user= models.OneToOneField(User,on_delete=models.CASCADE, null=True, blank=True,)
    NationalID = models.IntegerField(unique= True,  null=True, blank=True)
    FirstName = models.CharField(max_length=35, null=True, blank=True) 
    LastName = models.CharField(max_length=35, null=True, blank=True)
    email = models.EmailField(null=True, blank=False)
    phone = models.CharField(max_length=13, blank=True, null=True)
    Districts = models.CharField(max_length=35, null=True, blank=True)
    Sectors = models.CharField(max_length=35, null=True, blank=True)
    Cells = models.CharField(max_length=35, null=True, blank=True)
    villages = models.CharField(max_length=35, null=True, blank=True)
    Address_street = models.CharField(max_length=1000, null=True, blank=True)
    gender= models.CharField(max_length=10, null=True, blank=True, choices=GENDER)

    class Meta:
        db_table = "Engineer"

    def __str__(self):
        return str(self.NationalID )+' '+ self.FirstName +' '+ self.LastName


class Notifications(models.Model):
    id = models.AutoField(primary_key=True, default=None)
    RegistrationID=models.ForeignKey(Registration, on_delete=models.CASCADE, null=True, blank=True)
    message=models.CharField( max_length=1000, null=True, blank=True)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now_add=True)

    class Meta:
        db_table = "Notifications"

    def __str__(self):
        return self.message
