import imp
from multiprocessing import context
from urllib import response
from django.db.models import Avg, Count, Min, Sum
from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render, HttpResponse
from django.contrib import messages
from django.views.generic import CreateView
from django.db.models.functions import ExtractMonth

from django.contrib.auth.forms import AuthenticationForm
from .models import User, Permit, ArchivedPermit, Registration

from .forms import RegistrationForm, PermitForm
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa  
import xhtml2pdf.pisa as pisa

from django.contrib.staticfiles import finders
from .decorators import unauthenticated_user, allowed_users

from django.db.models import Q
import csv

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404



# Create your views here.
# def homepage(request):
#     return render(request, 'homepage.html')
def landingpage(request):
    return render(request, 'landingpage.html')
def footer(request):
    return render(request, 'footer.html')
def navbar(request):
    return render(request, 'Navbar.html')



# class client_registration(CreateView):
#     model = User
#     form_class = RegistrationForm
#     template_name = '../templates/client_registration.html'

#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('/')


class signup(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = '../templates/pages/examples/sign-up.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

@unauthenticated_user
def signin(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_client:
                login(request,user)
                return redirect('/homepage')
            elif user is not None and user.is_engineer:
                login(request,user)
                return redirect('/dashboard')    
            else:
                messages.error(request,"Invalid username or password")
        else:
                messages.error(request,"Invalid username or password")
    return render(request, '../templates/pages/examples/sign-in.html',
    context={'form':AuthenticationForm()})

   





def logout_view(request):
    logout(request)
    return redirect('/')



# New view ------------------------

# Engineer's Dashboard

import calendar
@login_required(login_url='signin')
@allowed_users(allowed_roles=['engineer'])
def eng_dashboard(request):
    permits = Permit.objects.all()
    if 'q' in request.GET:
        q = request.GET['q']
        permits = Permit.objects.filter(Q(Status__icontains=q) | Q(ApprovedBy__icontains=q) | Q(id__icontains=q))

    chart = Permit.objects.annotate(month=ExtractMonth('Date')).values('month').annotate(count=Count('id')).values('month', 'count')
    monthNumber = []
    totalPermits = []
    permitscount = Permit.objects.all().count()

    if permitscount != 0:
        for i in chart:
            monthNumber.append(calendar.month_name[i['month']])
            totalPermits.append(i['count'])
        
        totalpercentage = permitscount * 100 / permitscount
        permitcountpeding = Permit.objects.filter(Status='pending').count()
        permitcountdeclined = Permit.objects.filter(Status='declined').count()
        permitcountapproved = Permit.objects.filter(Status='approved').count()
        
        pendingpermitpercent = permitcountpeding * 100 / permitscount
        declinedpermitpercent = permitcountdeclined * 100 / permitscount
        approvedpermitpercent = permitcountapproved * 100 / permitscount
    else:
        totalpercentage = 0
        permitcountpeding = 0
        permitcountdeclined = 0
        permitcountapproved = 0
        pendingpermitpercent = 0
        declinedpermitpercent = 0
        approvedpermitpercent = 0

    context = {
        'permits': permits,
        'monthNumber': monthNumber,
        'totalPermits': totalPermits,
        'permitscount': permitscount,
        'permitcountpeding': permitcountpeding,
        'totalpercentage': totalpercentage,
        'pendingpermitpercent': pendingpermitpercent,
        'permitcountdeclined': permitcountdeclined,
        'declinedpermitpercent': declinedpermitpercent,
        'permitcountapproved': permitcountapproved,
        'approvedpermitpercent': approvedpermitpercent,
    }
    return render(request, '../templates/pages/dashboard/dashboard.html', context)




# Approving & Declining permit

def approve_permit(request, UUID):
    permit = Permit.objects.get(id = UUID)
    permit.Status = 'approved'
    permit.ApprovedBy = str(request.user)
    permit.save()
    savingArchives = ArchivedPermit(
            Archivedid=permit.id,
            registration=permit.registration,
            UPI=permit.UPI,
            ConstructionPlan=permit.ConstructionPlan,
            LandOwnerShipDoc=permit.LandOwnerShipDoc,
            OtherDoc=permit.OtherDoc,
            MainZonecode=permit.MainZonecode,
            Date=permit.Date,
            Status=permit.Status,
            ApprovedBy=permit.ApprovedBy,
            updated_at_issuedDate=permit.updated_at_issuedDate,
            comment=permit.comment  # Assign the comment field properly
        )
    savingArchives.save()
    messages.success(request, 'The Permit is successfuly Approved')
    return redirect('dashboard')




# def decline_permit(request, UUID):
#     permit = Permit.objects.get(id = UUID)
#     permit.Status = 'declined'
#     permit.ApprovedBy = str(request.user)
#     permit.save()
#     savingArchives = ArchivedPermit(
#         id = permit.id,
#         registration_id = permit.registration_id,
#         UPI_id = permit.UPI_id,
#         ConstructionPlan = permit.ConstructionPlan,
#         LandOwnerShipDoc = permit.LandOwnerShipDoc,
#         OtherDoc = permit.OtherDoc,
#         MainZonecode = permit.MainZonecode,
#         Date = permit.Date,
#         Status = permit.Status,
#         ApprovedBy = permit.ApprovedBy,
#         updated_at_issuedDate = permit.updated_at_issuedDate
#         comment = permit.comment
#     )
#     savingArchives.save()
#     messages.warning(request, 'The Permit is Declined !')
#     return redirect('dashboard')
def decline_permit(request, UUID):
    permit = Permit.objects.get(id=UUID)
    permit.Status = 'declined'
    permit.ApprovedBy = str(request.user)
    permit.save()

    savingArchives = ArchivedPermit(
            Archivedid=permit.id,
            registration=permit.registration,
            UPI=permit.UPI,
            ConstructionPlan=permit.ConstructionPlan,
            LandOwnerShipDoc=permit.LandOwnerShipDoc,
            OtherDoc=permit.OtherDoc,
            MainZonecode=permit.MainZonecode,
            Date=permit.Date,
            Status=permit.Status,
            ApprovedBy=permit.ApprovedBy,
            updated_at_issuedDate=permit.updated_at_issuedDate,
            comment=permit.comment  # Assign the comment field properly
        )
    savingArchives.save()

    messages.warning(request, 'The Permit is Declined!')
    return redirect('dashboard')




# @login_required(login_url='signin')
# @allowed_users(allowed_roles=['engineer'])
# def save_comment(request, permit_id):
#     if request.method == 'POST':
#         permit = get_object_or_404(Permit, id=permit_id)
#         comment = request.POST.get('comment')
#         permit.comment = comment
#         permit.save()

#         savingArchives = ArchivedPermit(
#         id=permit.id,
#         registration=permit.registration,
#         UPI=permit.UPI,
#         ConstructionPlan=permit.ConstructionPlan,
#         LandOwnerShipDoc=permit.LandOwnerShipDoc,
#         OtherDoc=permit.OtherDoc,
#         MainZonecode=permit.MainZonecode,
#         Date=permit.Date,
#         Status=permit.Status,
#         ApprovedBy=permit.ApprovedBy,
#         updated_at_issuedDate=permit.updated_at_issuedDate,
#         comment=permit.comment  # Assign the comment field properly
#     )
#     savingArchives.save()
#     return JsonResponse({'message': 'Invalid request'}, status=400)




@login_required(login_url='signin')
@allowed_users(allowed_roles=['engineer'])
def save_comment(request, permit_id):
    if request.method == 'POST':
        permit = get_object_or_404(Permit, id=permit_id)
        comment = request.POST.get('comment')
        permit.comment = comment
        permit.save()

        savingArchives = ArchivedPermit(
            Archivedid=permit.id,
            registration=permit.registration,
            UPI=permit.UPI,
            ConstructionPlan=permit.ConstructionPlan,
            LandOwnerShipDoc=permit.LandOwnerShipDoc,
            OtherDoc=permit.OtherDoc,
            MainZonecode=permit.MainZonecode,
            Date=permit.Date,
            Status=permit.Status,
            ApprovedBy=permit.ApprovedBy,
            updated_at_issuedDate=permit.updated_at_issuedDate,
            comment=permit.comment  # Assign the comment field properly
        )
        savingArchives.save()

        messages.success(request, 'Comment saved successfully.')
        return redirect('dashboard')

    # If the request method is not POST
    messages.error(request, 'Invalid request.')
    return redirect('dashboard')






@login_required(login_url='signin')
def request_permit(request):
  
    if request.method =="POST":
        form = PermitForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'The permit is requested')
            return redirect('/request_permitForm')
    else:
        form =  PermitForm(request.POST or None,request.FILES , user=request.user)
    return render(request, '../templates/request_permitForm.html',  {
        'form': form
    })

    
@login_required(login_url='signin')
def homepage(request):
    clientUser = Registration.objects.filter(user = request.user.id)

    for i in  clientUser:
        print(i)
        registration_id = i.id
        permited = Permit.objects.filter( registration = registration_id)
        context ={
            'permited': permited,
        }
    
        
    return render(request,'../templates/homepage.html', context )


@login_required(login_url='signin')
@allowed_users(allowed_roles=['engineer'])
def archivedpermit(request):
    archive = ArchivedPermit.objects.all()
    if 'q' in request.GET:
        q=request.GET['q']
        archive=ArchivedPermit.objects.filter(Q(Status__icontains=q)|Q(ApprovedBy__icontains=q)|Q(id__icontains=q))
    context ={
            'archive': archive,
        }
    return render(request, '../templates/pages/tables/archivedpermit.html', context)


    

def about(request):

    return render(request, '../templates/about.html')



# DEMO........ permit report below
@login_required(login_url='signin')
def permiting(request):
    clientUser = Registration.objects.filter(user = request.user.id)

    for i in  clientUser:
        print(i)
        registration_id = i.id
        permit = Permit.objects.filter( registration = registration_id)
        context ={
            'permit': permit,
        }
    
        
    return render(request,'../templates/pdf_report/permit.html', context )


# -------- end report -----------

def pdf_report_create(request):
    clientUser = Registration.objects.filter(user = request.user.id)

    for i in  clientUser:
        print(i)
        registration_id = i.id
        permit = Permit.objects.filter( registration = registration_id)
        
        template_path = 'pdf_report/permit.html'
        context = {'permit': permit}
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="permit_report.pdf"'
        
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        pisa_status = pisa.CreatePDF(
        html, dest=response)
        # if error then show some funny view
        if pisa_status.err:

          return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response

    
# permit csv file 

def permit_list_csv(request):
    permitcsv = Permit.objects.all()
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=all_permits_report.csv'
    writer = csv.writer(response)
    writer.writerow(['__________________________Autobatir request approval and analysis______________________________'])
    writer.writerow(['PERMIT ID', 'USERNAMES', 'UPI', 'CONSTRUCTION PLAN','LAND OWNERSHIP DOC', 'PAYMENTPROOF', 'OTHER DOC', 'MAIN ZONE CODE', 'DATE', 'STATUS', 'APPROVED BY', 'UPDATED TIME'])
  
    for permit in permitcsv:
        writer.writerow([permit.id, permit.registration, permit.UPI, permit.ConstructionPlan, permit.LandOwnerShipDoc, permit.Paymentproof, permit.OtherDoc, permit.MainZonecode,  permit.Date, permit.Status , permit.ApprovedBy,permit.updated_at_issuedDate])
    return response

# permit Archive csv file 

def archive_list_csv(request):
    archivecsv = ArchivedPermit.objects.all()
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=all_Archive_report.csv'
    writer = csv.writer(response)
    writer.writerow(['__________________________Autobatir request approval and analysis______________________________'])
    writer.writerow(['PERMIT ID', 'USERNAMES', 'UPI', 'CONSTRUCTION PLAN','LAND OWNERSHIP DOC', 'PAYMENTPROOF', 'OTHER DOC', 'MAIN ZONE CODE', 'DATE', 'STATUS', 'APPROVED BY', 'UPDATED TIME'])
  
    for permit in archivecsv:
        writer.writerow([permit.id, permit.registration, permit.UPI, permit.ConstructionPlan, permit.LandOwnerShipDoc, permit.Paymentproof, permit.OtherDoc, permit.MainZonecode,  permit.Date, permit.Status , permit.ApprovedBy,permit.updated_at_issuedDate])
    return response