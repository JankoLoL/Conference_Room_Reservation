from django.shortcuts import render, redirect
from django.views import View
from Conference_Room_app.models import ConferenceRoom


class MainView(View):

    def get(self, request):
        return render(request, "index.html")


class AddRoomView(View):
    def get(self, request):
        return render(request, "add_room.html")

    def post(self, request):
        name = request.POST.get("room-name")
        capacity = request.POST.get("capacity")
        capacity = int(capacity) if capacity else 0
        projector = request.POST.get("projector") == "on"

        if not name:
            return render(request, "add_room.html", {"error": "Room name is required"})
        if capacity <= 0:
            return render(request, "add_room.html", {"error": "Room capacity must be greater than 0"})
        if ConferenceRoom.objects.filter(name=name).exists():
            return render(request, "add_room.html", {"error": "Room already exists"})

        ConferenceRoom.objects.create(name=name, capacity=capacity, projector_availability=projector)
        return redirect("rooms-list")


class RoomsListView(View):
    def get(self, request):
        rooms = ConferenceRoom.objects.all()
        return render(request, "rooms.html", context={"rooms": rooms})


class DeleteRoomView(View):
    def get(self, request, room_id):
        room = ConferenceRoom.objects.get(id=room_id)
        room.delete()
        return redirect("rooms-list")


class EditRoomView(View):
    def get(self, request, room_id):
        room = ConferenceRoom.objects.get(id=room_id)
        return render(request, "edit_room.html", context={"room": room})

    def post(self, request, room_id):
        room = ConferenceRoom.objects.get(id=room_id)
        name = request.POST.get("room-name")
        capacity = request.POST.get("capacity")
        capacity = int(capacity) if capacity else 0
        projector = request.POST.get("projector") == "on"

        if not name:
            return render(request, "edit_room.html", {"room": room,
                                                      "error": "Room name is required"})
        if capacity <= 0:
            return render(request, "edit_room.html", {"room": room,
                                                      "error": "Room capacity must be greater than 0"})
        if ConferenceRoom.objects.filter(name=name).exclude(id=room_id).exists():
            return render(request, "edit_room.html", {"error": "Room with this name already exists"})

        room.name = name
        room.capacity = capacity
        room.projector_availability = projector
        room.save()
        return redirect("rooms-list")