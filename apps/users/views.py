from django.shortcuts import render

# Create your views here.
def users_list(request):
    users = [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25},
        {"name": "Charlie", "age": 35},
    ]
    return render(request, 'users/list.html', {'users': users})