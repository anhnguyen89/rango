from django.http import HttpResponse

# Create your views here.
def index(request):
	return HttpResponse("Polls says hello world!<br><a href='/rango/about'>Go to about page</a>")

def about(request):
	return HttpResponse("ABOUT POLLS")