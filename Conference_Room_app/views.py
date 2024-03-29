import datetime

from django.shortcuts import render, redirect
from django.views import View
from Conference_Room_app.models import ConferenceRoom, RoomReservation


class MainView(View):

    def get(self, request):
        current_date = datetime.date.today()
        reservations = RoomReservation.objects.filter(date=current_date)
        available_rooms = ConferenceRoom.objects.exclude(id__in=reservations.values('room_id'))
        return render(request, "index.html", {'available_rooms': available_rooms})


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
        for room in rooms:
            reservation_dates = [reservation.date for reservation in room.roomreservation_set.all()]
            room.reserved = datetime.date.today() in reservation_dates
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


class ReservationView(View):
    def get(self, request, room_id):
        room = ConferenceRoom.objects.get(id=room_id)
        reservations = room.roomreservation_set.filter(date__gte=str(datetime.date.today())).order_by('date')
        return render(request, "reservation.html", context={"room": room, "reservations": reservations})

    def post(self, request, room_id):
        room = ConferenceRoom.objects.get(id=room_id)
        date = request.POST.get("reservation-date")
        comment = request.POST.get("comment")

        reservations = room.roomreservation_set.filter(date__gte=str(datetime.date.today())).order_by('date')

        if RoomReservation.objects.filter(room=room, date=date):
            return render(request, "reservation.html", context={"room": room, "error": "Room is already reserved !"})
        if date < str(datetime.date.today()):
            return render(request, "reservation.html", context={"room": room, "error": "Date is in teh past"})

        RoomReservation.objects.create(room=room, date=date, comment=comment)
        return redirect("rooms-list")


class RoomDetailsView(View):
    def get(self, request, room_id):
        room = ConferenceRoom.objects.get(id=room_id)
        reservations = room.roomreservation_set.filter(date__gte=str(datetime.date.today())).order_by('date')
        return render(request, "room_details.html", context={"room": room, "reservations": reservations})


class SearchView(View):

    def get(self, request):
        return render(request, "search.html")
    def post(self, request):
        name = request.POST.get("room-name")
        capacity = request.POST.get("capacity")
        capacity = int(capacity) if capacity else 0
        projector = request.POST.get("projector") == "on"
        reservation_date = request.POST.get("date")

        rooms = ConferenceRoom.objects.all()
        if projector:
            rooms = rooms.filter(projector_availability=projector)
        if capacity:
            rooms = rooms.filter(capacity__gte=capacity)
        if name:
            rooms = rooms.filter(name__contains=name)
        if reservation_date:
            rooms = rooms.exclude(roomreservation__date=reservation_date)

        return render(request, "rooms.html", context={"rooms": rooms, "date": datetime.date.today()})
