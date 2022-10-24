from email.mime import image
from re import X
from turtle import width
from django.shortcuts import render, redirect , get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
import csv
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,KeepTogether,tables, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.pagesizes import A4,landscape
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PIL import Image, ImageDraw
from reportlab.lib.units import inch
from django.templatetags.static import static
from reportlab.lib.colors import yellow, red, black,white


# Create your views here.


def football(request):

    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))

    PAGE_WIDTH  = defaultPageSize[0]
    PAGE_HEIGHT = defaultPageSize[1]

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
        player = {}
        #print(lines)

        for index,line in enumerate(lines):
            if line == '':
                continue
            if index == 0:
                continue
            line = line.split(',')
            if line[1] not in player:
                player[line[1]] = {}
                player[line[1]]['Sport'] = str(line[9])
            if line[2] not in player[line[1]]:
                player[line[1]][line[2]] = []
            player[line[1]][line[2]].append((line[5],line[6]))
        
        print(player)

        # for i in player.items():
        #     print(i[0])
        #     for j in i[1].items():
        #         print(j)

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.setTitle("Football Report")
        #iterate through all the players in excel file
        for i in player.items():
            #generate player name and place name on top center of pdf page
            p.setFont("Vera", 18)
            player_name = i[0] + "'s Statistics"
            y = 800
            text_width = stringWidth(player_name, "Vera", 18)
            p.drawString((PAGE_WIDTH - text_width) / 2.0, y, player_name)
            #p.drawImage('../pitch.jpg', 0.5*inch,7.7*inch, width=250,height=200)
            imageCount = 1
            oriHeight = 6.5
            textHeight = 0
            centerPoint = 9
            #width of pitch 105m, height of pitch is 68.5m
            #halfway line is (PAGE_WIDTH) / 4.0 - 125)
            for j in i[1].items():
                if j[0] == 'Sport':
                    continue
                p.setFillColor("black") #change color of the dots
                if imageCount == 7:
                    imageCount = 1
                    oriHeight = 6.5
                    textHeight = 0
                    p.showPage()
                    p.setFont("Vera", 18)
                if i[1]['Sport'] == 'Football\r':
                    image = '../pitch2.jpg'
                elif i[1]['Sport'] == 'Basketball\r':
                    image = '../court2.jpg'
                if imageCount % 2 != 0: # if imageCount is odd, means pitch on left side
                    p.drawImage(image, ((PAGE_WIDTH) / 4.0 - 125),(PAGE_HEIGHT / 10) * oriHeight, width=250,height=200)
                    text = j[0] # event name
                    text_width = stringWidth(text, "Vera", 15)
                    p.drawString(((PAGE_WIDTH ) / 4.0 - text_width/2 - 1.5),(PAGE_HEIGHT / 10.5) * (oriHeight - textHeight),text)
                    
                    for k in j[1]:
                        print(k)
                        p.setFillColor("yellow")
                        relative_x = (int(k[0]) / 105) * 250
                        relative_y = (int(k[1]) / 105) * 200
                        if relative_x <= 125:
                            x_pos = 125 - relative_x
                            x = ((PAGE_WIDTH) / 4.0 + x_pos)
                        else:
                            x_pos = relative_x - 125
                            x = ((PAGE_WIDTH) / 4.0 - x_pos)
                        p.circle(x,(PAGE_HEIGHT / 10) * oriHeight + relative_y,2,stroke=1,fill=1)
                        #print(x)
                else: 
                    p.setFillColor("black")
                    print(i[1]['Sport'])
                    p.drawImage(image, (((PAGE_WIDTH) / 4.0) * 3 - 125),(PAGE_HEIGHT / 10) * oriHeight, width=250,height=200)
                    text = j[0]
                    text_width = stringWidth(text, "Vera", 15)
                    p.drawString((((PAGE_WIDTH) / 4.0) * 3 - text_width/2 - 1.5),(PAGE_HEIGHT / 10.5) * (oriHeight - textHeight),text)

                    for k in j[1]:
                        p.setFillColor("yellow")
                        #print(k)
                        relative_x = (int(k[0]) / 105) * 250
                        relative_y = (int(k[1]) / 105) * 200
                        if relative_x <= 125:
                            x_pos = 125 - relative_x
                            x = (((PAGE_WIDTH) / 4.0) * 3 + x_pos)
                        else:
                            x_pos = relative_x - 125
                            x = (((PAGE_WIDTH) / 4.0) * 3 - x_pos)
                        p.circle(x,(PAGE_HEIGHT / 10) * oriHeight + relative_y,2,stroke=1,fill=1)
                        #print(x)

                imageCount += 1
                if imageCount % 2 != 0 and imageCount != 1:
                    oriHeight -= 3
                    textHeight += 0.12
                #print(j)

            #generate new pdf page for each player
            p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='Football Report.pdf')


    except Exception as e:
        # logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        # messages.error(request,"Unable to upload file. "+repr(e))
        print(e)



    


