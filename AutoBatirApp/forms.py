from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Permit, User, Registration
# The bellow models are imported as (IC & AB) These ase just variable classes to hold both
# Registration and UPI models to user them to filter permitform dropdown 

from .models import Registration as IC
from .models import UPI as AB





class RegistrationForm(UserCreationForm):
    National_ID = forms.CharField(required=True)
    FirstName = forms.CharField(required=True)
    LastName = forms.CharField(required=True)
    email= forms.EmailField(required = True)
    # profile_Picture = forms.ImageField(required=True)
    phone = forms.CharField(required=True)
    Districts = forms.CharField(required=True)
    Sectors = forms.CharField(required=True)
    Cells = forms.CharField(required=True)
    villages = forms.CharField(required=True)
    Address_street = forms.CharField(required=True)
    gender= forms.CharField(required=True)
    
    class Meta(UserCreationForm.Meta):
        model = User

  
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_client = True
        user.is_staff = True
        user.save()
        registration = Registration.objects.create(user=user)
        registration.National_ID= self.cleaned_data.get('National_ID')
        registration.FirstName = self.cleaned_data.get('FirstName')
        registration.LastName = self.cleaned_data.get('LastName')
        registration.email  = self.cleaned_data.get('email')
        # registration.profile_Picture = self.cleaned_data.get('profile_Picture')
        registration.phone = self.cleaned_data.get('phone')
        registration.Districts = self.cleaned_data.get('Districts')
        registration.Sectors = self.cleaned_data.get('Sectors')
        registration.Cells = self.cleaned_data.get('Cells') 
        registration.villages = self.cleaned_data.get('villages')
        registration.Address_street = self.cleaned_data.get('Address_street')
        registration.gender = self.cleaned_data.get('gender')
 
        registration.save()
        return user
    

        

      

class  PermitForm(forms.ModelForm):
    class Meta:
        model = Permit
        fields = ('registration', 'UPI', 'ConstructionPlan', 'LandOwnerShipDoc','Paymentproof', 'OtherDoc', 'MainZonecode',)
        labels  = {
        'registration':'Username', 
        'UPI':'Land UPI', 
        'Paymentproof':'Payment-proof',
        'OtherDoc':'OtherDoc ex: pdf attachement letter and National ID copy', 
        }
    def __init__(self,*args, user=None, **kwargs):
        super(PermitForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['registration'].queryset = IC.objects.filter(user=user)
            self.fields['UPI'].queryset = AB.objects.filter(user=user)
    

        

    
   












# class EmployeeSignUpForm(UserCreationForm):
#     first_name = forms.CharField(required=True)
#     last_name = forms.CharField(required=True)
#     phone_number = forms.CharField(required=True)
#     designation = forms.CharField(required=True)

#     class Meta(UserCreationForm.Meta):
#         model = User

#     @transaction.atomic
#     def save(self):
#         user = super().save(commit=False)
#         user.is_employee = True
#         user.is_staff = True
#         user.first_name = self.cleaned_data.get('first_name')
#         user.last_name = self.cleaned_data.get('last_name')
#         user.save()
#         employee = Employee.objects.create(user=user)
#         employee.phone_number=self.cleaned_data.get('phone_number')
#         employee.designation=self.cleaned_data.get('designation')
#         employee.save()
#         return user
