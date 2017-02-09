from django.shortcuts import render

# Create your views here.
def students_list(request):
    return render(request, 'students/students_list.html', {})