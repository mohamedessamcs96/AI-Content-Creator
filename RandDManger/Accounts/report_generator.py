from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from rtl import reshaper
from bidi.algorithm import get_display
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph,Spacer
from reportlab.lib.pagesizes import A4
from reportlab.graphics.shapes import Drawing, Line

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from rtl import reshaper
from bidi.algorithm import get_display
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Image
from arabic_reshaper import reshape
from django.conf import settings
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views import View

class CreateReportPdf():
    @method_decorator(csrf_exempt)  # This decorator is used to exempt the view from CSRF verification
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def generate_report(self,script):
        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Report.pdf"'

        # Create a PDF document object
        buffer = BytesIO()
        # Set the desired margin size (in this example, 1 inch)
        margin_size = 0.5 * inch
        # Create the PDF object
        doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=margin_size, rightMargin=margin_size,
                                topMargin=margin_size, bottomMargin=margin_size, showBoundary=True)

        # # Load custom font file for Arabic text
        font_path = settings.STATIC_ROOT + '/webfonts/22016-adobearabic.ttf'

        font_path = settings.STATIC_ROOT + '/webfonts/22016-adobearabic.ttf'  # Replace with the path to your font file
        pdfmetrics.registerFont(TTFont('22016-adobearabic', font_path))

        # Define styles
        custom_style = ParagraphStyle(
            name='CustomStyle',
            fontName='22016-adobearabic',
            fontSize=14,
            textColor=colors.black,
            alignment=1,
        )

        head_style = ParagraphStyle(
            name='head_style',
            fontName='22016-adobearabic',
            fontSize=20,
            textColor=colors.black,
            spaceBefore=12,
            spaceAfter=6,
            alignment=1
        )

        # Build story
        story = []
        spacer = Spacer(50, 50)
        story.append(spacer)

        # logo_path = settings.STATIC_ROOT + '/img/logo.jpg'
        # logo_image = Image(logo_path, width=2 * inch, height=1 * inch)
        # logo_image.hAlign = 'RIGHT'
        # story.append(logo_image)
        logo_path = settings.STATIC_ROOT + '/imgs/scriptforgelogo.png'
        logo_image = Image(logo_path, width=0.9 * inch, height=0.9 * inch)
        # logo_image.hAlign = 'LEFT'
        story.append(spacer)
        story.append(logo_image)

        story.append(Paragraph('Script Forge', head_style))
        story.append(spacer)
        import datetime
        now = datetime.datetime.now()
        # text_display = 'R and D Manager'

        title=script.split('\n')[0]
        story.append(Paragraph(title, head_style))
        story.append(spacer)
        story.append(Paragraph(script, custom_style))
        

        # info_table_data = [
        #     [Paragraph('arabic_text_display2', custom_style), Paragraph('arabic_text_display1', custom_style)],
        #     [Paragraph('arabic_text_display3', custom_style), Paragraph('arabic_text_display4', custom_style)],
        #     [Paragraph('arabic_text_display6', custom_style), Paragraph('arabic_text_display5', custom_style)],
        #     [Paragraph('arabic_text_display7', custom_style), Paragraph('arabic_text_display8', custom_style)]
        # ]
        # info_table_data = Table(info_table_data, colWidths=[2 * inch, 2 * inch])
        info_table_data_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), '#9DB2BF'),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), '22016-adobearabic'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), '#9DB2BF'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ])
        # info_table_data.setStyle(info_table_data_style)
        # story.append(info_table_data)

        story.append(spacer)
        story.append(spacer)
        story.append(spacer)
        story.append(spacer)

        # line_table_data = [['']]
        # line_table_style = TableStyle([
        #     ('BOTTOMPADDING', (0, 0), (-1, -1), 2, colors.black),
        #     ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.black)
        # ])
        # line_table = Table(line_table_data, colWidths=[doc.width])
        # line_table.setStyle(line_table_style)
        # story.append(line_table)

      

    # # Initialize variables to store scene details
    #     data = []

    #     scene_number = 0
    #     visual = ""
    #     voice_over = ""

    #     # Loop through each line in the script
    #     for line in script:
    #         # Check if the line contains visual description
    #         if line.startswith("Scene"):
    #             # If visual and voice_over are not empty, add them to the data list
    #             if visual and voice_over:
    #                 scene_number += 1
    #                 data.append([str(scene_number), visual, voice_over])
    #             # Reset visual and voice_over for the next scene
    #             visual = ""
    #             voice_over = ""
    #         elif line.startswith("Visual:"):
    #             visual = line.replace("Visual:", "").strip()
    #         elif line.startswith("Voice Over:"):
    #             voice_over = line.replace("Voice Over:", "").strip()

    #     # If visual and voice_over are not empty after the loop, add them to the data list
    #     if visual and voice_over:
    #         scene_number += 1
    #         data.append([str(scene_number), visual, voice_over])

        # Create the table object
        # t = Table(data)
        # t.setStyle(info_table_data_style)
            
    

        # # Convert HTML-like content to ReportLab paragraphs
        # table = Paragraph(t)
        # story.append(table)
        # story.append(t)
        # return story
        doc.build(story)

        # Get the value of the BytesIO buffer and write it to the response
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)

        return response



# def create_report_ar(request,pk):
    

#         # Create the HttpResponse object with the appropriate PDF headers.
#         response = HttpResponse(content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="Clinet Info Report-{client.clientname}.pdf"'

#         # Create a PDF document object
        
#         buffer = BytesIO()
#         # Set the desired margin size (in this example, 1 inch)
#         margin_size = 0.5 * inch
#         # Create the PDF object
#         doc = SimpleDocTemplate(buffer, pagesize=A4,leftMargin=margin_size, rightMargin=margin_size,
#                     topMargin=margin_size, bottomMargin=margin_size,showBoundary=True)
        

#         # Create a custom ParagraphStyle
#         custom_style = ParagraphStyle(
#             name='CustomStyle',
#             fontName='22016-adobearabic',  # Specify your custom font name
#             fontSize=14,  # Specify the font size
#             textColor=colors.black,  # Specify the font color
#             alignment=2,
        

#         )
#         # Create a custom ParagraphStyle
#         custom_style2 = ParagraphStyle(
#             name='CustomStyle',
#             fontName='22016-adobearabic',  # Specify your custom font name
#             fontSize=14,  # Specify the font size
#             textColor=colors.black,  # Specify the font color

#             alignment=1,


#         )
#         # Define a style for center-aligned paragraph
#         center_style = ParagraphStyle(
#             name='CustomStyle',
#             fontName='22016-adobearabic',  # Specify your custom font name
#             fontSize=16,  # Specify the font size
#             textColor=colors.blue,  # Specify the font color
#             spaceBefore=12,  # Specify the space before the paragraph
#             spaceAfter=6,  # Specify the space after the paragraph
#             alignment=1
#         )

#         # Define a style for center-aligned paragraph
#         # Define a style for center-aligned paragraph
#         head_style = ParagraphStyle(
#             name='head_style',
#             fontName='22016-adobearabic',  # Specify your custom font name
#             fontSize=20,  # Specify the font size
#             textColor=colors.black,  # Specify the font color
#             spaceBefore=12,  # Specify the space before the paragraph
#             spaceAfter=6,  # Specify the space after the paragraph
#             alignment=1
#         )  
        

#         # Load custom font file for Arabic text
#         font_path = settings.STATIC_ROOT + '/webfonts/22016-adobearabic.ttf'  # Replace with the path to your font file
#         print(font_path)
#         pdfmetrics.registerFont(TTFont('22016-adobearabic', font_path))










#         # Define a style for center-aligned paragraph
#         center_style = ParagraphStyle(
#             name='CustomStyle',
#             fontName='22016-adobearabic',  # Specify your custom font name
#             fontSize=14,  # Specify the font size
#             textColor=colors.blue,  # Specify the font color
#             spaceBefore=12,  # Specify the space before the paragraph
#             spaceAfter=6,  # Specify the space after the paragraph
#             alignment=1
#         )

        

#         # Add simple strings above the table
#         client=Client.objects.get(clientnumber=pk) 





#         # Add a spacer with horizontal space of 50 points
#         spacer = Spacer(50, 50)
        
#         # Build the story containing the table
#         story = []    
#         # Define the path to your logo image file
#         logo_path = settings.STATIC_ROOT + '/img/logo.jpg'
#         # Create an Image object with the logo image



#         # Set the logo's position to the left side of the page

#         logo_image = Image(logo_path, width=2 * inch, height=1 * inch)  # Adjust the width and height as per your requirement
#         logo_image.hAlign = 'RIGHT'
#         # Add the logo image to the story before the table
#         story.append(logo_image)     

#         arabic_text_display=reshaper.reshape('مختبر صحه الكائنات البيطريه')
#         arabic_text_display = get_display(arabic_text_display)
#         story.append(Paragraph(arabic_text_display,head_style))
        

#         story.append(Paragraph("Veterinary animal Health Laboratory",head_style))
#         story.append(spacer)
#         arabic_text_display=reshaper.reshape('  بيانات العميل ')
#         arabic_text_display = get_display(arabic_text_display)
#         story.append(Paragraph(arabic_text_display,head_style))
#         story.append(spacer)

#         arabic_text_display=reshaper.reshape(f"الآسم:{client.clientname}")
#         arabic_text_display1 = get_display(arabic_text_display)
#         arabic_text_display=reshaper.reshape(f"رقم العميل:{client.clientnumber}")
#         arabic_text_display2 = get_display(arabic_text_display)
#         arabic_text_display=reshaper.reshape(f"نوع الحيوان :{client.animaltype}")
#         arabic_text_display3 = get_display(arabic_text_display)

#         clientrow = Client.objects.get(pk=1)
#         field_label = clientrow.get_field_label(client.sampletype)
        
#         arabic_text_display4 = get_display(reshaper.reshape(f' نوع العينه: {field_label}'))
#         now=datetime.datetime.now()
#         arabic_text_display5 = get_display(reshaper.reshape(f' التاريخ:{now.year}/{now.month}/{now.day}'))
#         analysis_prices = AnalysisPrices.objects.get(pk=1)  # Assuming you have only one instance
#         field=str(field_label)
#         price = getattr(analysis_prices, field)

#         arabic_text_display6 = get_display(reshaper.reshape(f' السعر: {price} ريال'))
#         arabic_text_display7 = get_display(reshaper.reshape(f' عمر الحيوان: {client.age} سنه'))


#         arabic_text_display8 = get_display(reshaper.reshape(f' ملحوظه: {client.notes}'))

#         # Create a table with three rows and two cells
#         info_table_data = [
#             [Paragraph(arabic_text_display2, custom_style), Paragraph(arabic_text_display1, custom_style)],
#             [Paragraph(arabic_text_display3, custom_style), Paragraph(arabic_text_display4, custom_style)],
#             [Paragraph(arabic_text_display6, custom_style), Paragraph(arabic_text_display5, custom_style)],
#             [Paragraph(arabic_text_display7, custom_style), Paragraph(arabic_text_display8, custom_style)]

#         ]
#         info_table_data = Table(info_table_data,colWidths=[2 * inch,2 * inch])
#         info_table_data_style= TableStyle([
#                     ('BACKGROUND', (0, 0), (-1, 0), '#9DB2BF'),
#                     ('TEXTCOLOR', (0, 0), (-1, -1), colors.white) ,
#                     ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#                     ('FONTNAME', (0, 0), (-1, 0), '22016-adobearabic'),
#                     ('FONTSIZE', (0, 0), (-1, 0), 12),
#                     ('BACKGROUND', (0, 1), (-1, -1), '#9DB2BF'),
#                     ('GRID', (0, 0), (-1, -1), 1, colors.black),
#                     ('TOPPADDING', (0, 0), (-1, -1), 6),  # Top padding for all cells
#                     ('BOTTOMPADDING', (0, 0), (-1, -1), 6),  # Bottom padding for all cells
#                 ])
#         info_table_data.setStyle(info_table_data_style)
#         # Set the row heights

#         # Add the table to the story
#         story.append(info_table_data)
#         # Add the table to the story

#         story.append(spacer)
#         story.append(spacer)  
#         story.append(spacer)  
#         story.append(spacer)  
            


#         line_table_data = [['']]  # Empty cell content
#         line_table_style = TableStyle([
#             ('BOTTOMPADDING', (0, 0), (-1, -1), 2, colors.black),  # Bottom padding of 2 points
#             ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.black)  # Bottom border line with 0.5-point width
#         ])
#         line_table = Table(line_table_data, colWidths=[doc.width])  # Table with a single column spanning the width of the document
#         line_table.setStyle(line_table_style)  # Apply the table style
#         story.append(line_table)
    
#         logo_path = settings.STATIC_ROOT + '/img/qrlogo.png'
#         # Create an Image object with the logo image
#         # Set the logo's position to the left side of the page
        
#         story.append(spacer)  

#         logo_image = Image(logo_path, width=0.7 * inch, height=0.7 * inch)  # Adjust the width and height as per your requirement
#         # Add the logo image to the story before the table
#         story.append(logo_image)  




#         arabic_text_display=reshaper.reshape('المملكه العربية/ الرياض/طريق الجنادرية')
#         arabic_text_display = get_display(arabic_text_display)
#         story.append(Paragraph(arabic_text_display,center_style))
#         story.append(Paragraph('0503721656 / 0537308922',center_style))
#         # Build the PDF document
#         doc.build(story)



#         # Get the value of the BytesIO buffer and write it to the response
#         pdf = buffer.getvalue()
#         buffer.close()
#         response.write(pdf)
        
#         return response
