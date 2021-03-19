from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa


def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)

	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

# data is to come from database
data = {
	"company": "Ivanov Company",
	"address": "123 Street name",
	"city": "New Delhi",
	"state": "Delhi",
	"zipcode": "1100",

	"phone": "555-555-2345",
	"email": "youremail@gmail.com",
	"website": "htmltoPDF-Converter.com",
	}

# Opens up page as PDF
class ViewPDF(View):
	def get(self, request, *args, **kwargs):

		pdf = render_to_pdf('pdf_template.html', data)
		return HttpResponse(pdf, content_type='application/pdf')


# Automaticly downloads to PDF file
class DownloadPDF(View):
	def get(self, request, *args, **kwargs):
		
		pdf = render_to_pdf('pdf_template.html', data)

		response = HttpResponse(pdf, content_type='application/pdf')
		filename = "Invoice_%s.pdf" %("12341231")
		content = "attachment; filename='%s'" %(filename)
		response['Content-Disposition'] = content
		return response


def index(request):
	context = {}
	return render(request, 'index.html', context)