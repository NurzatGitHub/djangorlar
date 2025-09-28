from django.shortcuts import render

# Create your views here.
couter_value = 0

def counter(request):
    global couter_value
    if 'inc' in request.GET:
        couter_value += 1
    elif 'reset' in request.GET:
        couter_value = 0
    return render(request, 'counter/index.html', {'counter': couter_value})