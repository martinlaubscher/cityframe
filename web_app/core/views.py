from django.shortcuts import render


def front_page(request):
    context = {}
    return render(request, "index.html", context)
