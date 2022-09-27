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

        for index,line in enumerate(lines):
            if index == 0:
                continue
            line = line.split(',')
            if line[1] not in player:
                player[line[1]] = {}
            if line[2] not in player[line[1]]:
                player[line[1]][line[2]] = []
            player[line[1]][line[2]].append((line[5],line[6]))

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
            oriHeight = 7.7
            textHeight = 7.3
            for j in i[1].items():
                if imageCount % 2 != 0:
                    p.drawImage('../pitch2.jpg', ((PAGE_WIDTH) / 4.0 - 125),oriHeight*inch, width=260,height=200)
                    text = j[0]
                    text_width = stringWidth(text, "Vera", 18)
                    p.drawString(((PAGE_WIDTH ) / 4.0 - text_width/2),textHeight*inch,text)
                    if imageCount != 1:
                        oriHeight -= 2
                    
                    for k in j[1]:
                        print(k)
                else:
                    p.drawImage('../pitch2.jpg', (((PAGE_WIDTH) / 4.0) * 3 - 125),oriHeight*inch,width=260,height=200)
                    text = j[0]
                    text_width = stringWidth(text, "Vera", 18)
                    p.drawString((((PAGE_WIDTH) / 4.0) * 3 - text_width/2),textHeight*inch,text)
                imageCount += 1
                print(j)

            #generate new pdf page for each player
            p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='Football Report.pdf')


    except Exception as e:
        # logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        # messages.error(request,"Unable to upload file. "+repr(e))
        print(e)



    


