from django.shortcuts import render, redirect
from .models import GalleryImage
from .forms import GalleryImageForm


# Create your views here.
def gallery(request):
    images = GalleryImage.objects.all()
    return render(request, "gallery/index.html", {"images": images})


def upload(request):
    if request.method == 'POST':
        form = GalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gallery')
    form = GalleryImageForm()
    return render(request, "gallery/upload.html", {'form': form})
