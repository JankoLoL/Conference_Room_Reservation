from django.shortcuts import render, redirect

# Create your views here.

from django.views import View

from Conference_Room_app.models import ConferenceRoom


class MainView(View):

    def get(self, request):
        return render(request, "index.html")


class AddRoomView(View):
    def get(self, request):
        return render(request, "add-room.html")


    def post(self, request):
        name = request.POST.get("room-name")
        capacity = request.POST.get("room-capacity")
        capacity = int(capacity) if capacity else 0
        projector = request.POST.get("projector") == "on"

        if not name:
            return render(request, "add-room.html", {"error": "Room name is required"})
        if capacity <= 0:
            return render(request, "add-room.html", {"error": "Room capacity must be greater than 0"})
        if ConferenceRoom.objects.filter(name=name).exists():
            return render(request, "add-room.html", {"error": "Room already exists"})

        ConferenceRoom.objects.create(name=name, capacity=capacity, projector_availability=projector)
        return redirect("rooms-list")
