from typing import Any
from django import http
import pandas as pd
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from .models import *
from django.urls import reverse
from django.views.decorators.http import require_GET
import csv

# Create your views here.
class Registration_View(generic.FormView):
    def get(self, request):
        if not request.GET.get('phone'):
            return render(request, "Register.html")
        else:
            participants_object = Participant.objects.filter(Phone=request.GET.get('phone'))
            return render(request, "Details.html", {"participants": participants_object})
        
class ParticipantList_View(generic.FormView):
    template_name = "ParticipantList.html"
    def get(self, request):
        participant_list = Participant.objects.all()
        phone = request.GET.get('phone')
        event = request.GET.get('event')
        name = request.GET.get('name')
        registered = request.GET.get('registered')

        if phone is None: phone  = ''
        if event is None: event  = ''
        if name is None: name  = ''
        if registered is None: registered  = ''

        if phone != '':
            participant_list = participant_list.filter(Phone=phone)
        if event != '':
            participant_list = participant_list.filter(Event=event)
        if name != '':
            participant_list = participant_list.filter(Teammate1__icontains=name)
        if registered != '':
            participant_list = participant_list.filter(Registered=registered)
        
        return render(request, self.template_name, {"participant_list": participant_list, "count": len(participant_list), "phone": phone, "event": event, "name": name, "registered": registered})
        
class SpotRegistration_View(generic.FormView):
    template_name = 'SpotRegistration.html'
    def get(self, request):
        print (request.GET.get('event'))
        if request.GET.get('event'):
            return render(request, self.template_name, {"event": request.GET.get('event')})
        else:
            return render(request, self.template_name)
    def post(self, request):
        Phone = request.POST.get('phone')
        Event = request.GET.get('event')
        Teammate1 = request.POST.get('participant1')
        if (request.POST.get('participant2')): Teammate2 = request.POST.get('participant2')
        else: Teammate2 = "nan - nan"
        if (request.POST.get('participant3')): Teammate3 = request.POST.get('participant3')
        else: Teammate3 = "nan - nan"
        if (request.POST.get('participant4')): Teammate4 = request.POST.get('participant4')
        else: Teammate4 = "nan - nan"
        if (request.POST.get('participant5')): Teammate5 = request.POST.get('participant5')
        else: Teammate5 = "nan - nan"
        if (request.POST.get('participant6')): Teammate6 = request.POST.get('participant6')
        else: Teammate6 = "nan - nan"
        if (request.POST.get('participant7')): Teammate7 = request.POST.get('participant7')
        else: Teammate7 = "nan - nan"
        if (request.POST.get('participant8')): Teammate8 = request.POST.get('participant8')
        else: Teammate8 = "nan - nan"
        if (request.POST.get('participant9')): Teammate9 = request.POST.get('participant9')
        else: Teammate9 = "nan - nan"
        if (request.POST.get('participant10')): Teammate10 = request.POST.get('participant10')
        else: Teammate10 = "nan - nan"
        College = request.POST.get('college')
        Degree = request.POST.get('degree')
        Year = request.POST.get('year')
        Registered = "SPOT"
        if (request.POST.get('transaction_id')): Transaction_ID = request.POST.get('transaction_id')
        else: Transaction_ID = "N/A"

        Participant.objects.create(
            Phone = Phone,
            Event = Event,
            Teammate1 = Teammate1,
            Teammate2 = Teammate2,
            Teammate3 = Teammate3,
            Teammate4 = Teammate4,
            Teammate5 = Teammate5,
            Teammate6 = Teammate6,
            Teammate7 = Teammate7,
            Teammate8 = Teammate8,
            Teammate9 = Teammate9,
            Teammate10 = Teammate10,
            College = College,
            Degree = Degree,
            Year = Year,
            Registered = Registered,
            Transaction_ID = Transaction_ID,
        )
        return redirect('registration')


class RegisterParticipant(generic.RedirectView):
    def get(self, request):
        phone = request.GET.get('phone')
        participant_object = Participant.objects.filter(Phone=phone)
        if participant_object.filter(Event__istartswith="byte battle").exists():
            return render(request, "Transaction.html", {"phone": phone})
        participant_object.update(Registered="YES")
        return redirect('registration')
    def post(self, request):
        participant_objects_to_delete = Participant.objects.filter(Phone=request.GET.get('phone')).exclude(Event__istartswith="byte battle")
        participant_objects_to_delete.delete()
        Participant.objects.filter(Phone=request.GET.get('phone')).update(Registered="YES", Transaction_ID=request.POST.get('transaction_id'))
        return redirect('registration')
    
def import_csv_view(request):
    # Change the path to your CSV file
    csv_path = '/Users/barath/Documents/Django/Event Management/eventmanagementsystem/app/Form Response.csv'

    try:
        # Read the CSV file into a pandas DataFrame
        csv_data = pd.read_csv(csv_path)

        # Iterate through the rows and create AMI1 instances
        for index, row in csv_data.iterrows():
            participant_instance = Participant(
                Event = row['Event'],
                College = row['College name'],
                Teammate1 = str(row['Team member name (1)']) + " - " + str(row['Register no (1)']),
                Teammate2 = str(row['Team member name (2)']) + " - " + str(row['Register no (2)']),
                Teammate3 = str(row['Team member name (3)']) + " - " + str(row['Register no (3)']),
                Teammate4 = str(row['Team member name (4)']) + " - " + str(row['Register no (4)']),
                Teammate5 = str(row['Team member name (5)']) + " - " + str(row['Register no (5)']),
                Teammate6 = str(row['Team member name (6)']) + " - " + str(row['Register no (6)']),
                Teammate7 = str(row['Team member name (7)']) + " - " + str(row['Register no (7)']),
                Teammate8 = str(row['Team member name (8)']) + " - " + str(row['Register no (8)']),
                Teammate9 = str(row['Team member name (9)']) + " - " + str(row['Register no (9)']),
                Teammate10 = str(row['Team member name (10)']) + " - " + str(row['Register no (10)']),
                Degree = row['Degree'],
                Year = row['Year'],
                Phone = row['Phone number'],
                Registered = "NO"
            )
            if not Participant.objects.filter(Event=participant_instance.Event, Phone=participant_instance.Phone).exists():
                participant_instance.save()

        message = "Data imported successfully."
    except Exception as e:
        message = f"Error importing data: {str(e)}"

    return HttpResponse(message)

@require_GET
def download_csv(request):
    participant_list = Participant.objects.all()
    phone = request.GET.get('phone')
    event = request.GET.get('event')
    name = request.GET.get('name')
    registered = request.GET.get('registered')

    if phone is None: phone  = ''
    if event is None: event  = ''
    if name is None: name  = ''
    if registered is None: registered  = ''

    if phone != '':
        participant_list = participant_list.filter(Phone=phone)
    if event != '':
        participant_list = participant_list.filter(Event=event)
    if name != '':
        participant_list = participant_list.filter(Teammate1__icontains=name)
    if registered != '':
        participant_list = participant_list.filter(Registered=registered)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="participant details.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "Phone",
        "Event",
        "Teammate1",
        "Teammate2",
        "Teammate3",
        "Teammate4",
        "Teammate5",
        "Teammate6",
        "Teammate7",
        "Teammate8",
        "Teammate9",
        "Teammate10",
        "College",
        "Degree",
        "Year",
        "Registered",
])

    for participant in participant_list:
        writer.writerow([
            participant.Phone,
            participant.Event,
            participant.Teammate1,
            participant.Teammate2,
            participant.Teammate3,
            participant.Teammate4,
            participant.Teammate5,
            participant.Teammate6,
            participant.Teammate7,
            participant.Teammate8,
            participant.Teammate9,
            participant.Teammate10,
            participant.College,
            participant.Degree,
            participant.Year,
            participant.Registered,
        ])
    return response

def BB_Unregister(request):
    Participant.objects.filter(Phone=request.GET.get('phone'), Event__startswith = "byte battle").delete()
    Participant.objects.filter(Phone=request.GET.get('phone')).update(Registered="YES")
    return redirect('registration')