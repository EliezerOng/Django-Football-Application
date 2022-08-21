from django.shortcuts import render, redirect , get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
import csv

# Create your views here.

def football(request):

    data = {}
    if "GET" == request.method:
        return render(request, 'football/football.html', data)

    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            return HttpResponseRedirect(reverse("football:football"))


        file_data = csv_file.read().decode("utf-8")	
        lines = file_data.split("\n")
        #lines = lines.split(",")
        event = {}

        for index,line in enumerate(lines):
            if index == 0:
                continue
            line = line.split(',')
            if line[2] not in event:
                event[line[2]] = []
            event[line[2]].append((line[5],line[6]))

        print(event)

    except Exception as e:
        # logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        # messages.error(request,"Unable to upload file. "+repr(e))
        pass


    


