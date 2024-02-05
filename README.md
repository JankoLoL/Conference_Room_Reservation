# Conference Rooms Reservation

## Overview
This Django web application is designed to manage the reservation of conference rooms. It allows users to view available rooms, add new rooms, delete and edit existing rooms, and make reservations for specific dates.

## Features
- **List Available Rooms**: Users can view rooms that are not reserved for the current day.
- **Add New Room**: Users can add new conference rooms with details such as room name, capacity, and projector availability.
- **Edit Room**: Users can edit the details of existing conference rooms.
- **Delete Room**: Users can remove conference rooms from the system.
- **Make a Reservation**: Users can reserve a room for a specific date, provided it is not already reserved.
- **Search Functionality**: Users can search for rooms based on name, capacity, projector availability, and reservation date.

## Models
- `ConferenceRoom`: Represents a conference room with fields for name, capacity, and projector availability.
- `RoomReservation`: Represents a reservation with a foreign key to `ConferenceRoom`, a date, and an optional comment field.

## Views
- `MainView`: Displays available rooms for the current date.
- `AddRoomView`: Form to add a new room.
- `RoomsListView`: Lists all rooms and their reservation status.
- `DeleteRoomView`: Handles the deletion of a room.
- `EditRoomView`: Form to edit the details of an existing room.
- `ReservationView`: Form to make a new reservation and list existing reservations for a room.
- `SearchView`: Handles the searching of rooms based on various criteria.

## Templates
HTML templates are used for rendering the views, utilizing Bootstrap for styling.


## Installation & Setup

### 1. Clone the repository
Clone the project repository to your local machine.

    git clone https://github.com/JankoLoL/Conference_Room_Reservation

### 2. Set up a virtual environment
Navigate to the project directory and create a virtual environment. Activate it and install the required packages.

    cd yourprojectname
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt

### 3. Configure Database Settings
Create a `local_settings.py` file in the same directory as `settings.py`. This file should contain your PostgreSQL database configuration and any other sensitive settings.

Example `local_settings.py` content:

    # local_settings.py
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'yourdbname',
            'USER': 'yourdbuser',
            'PASSWORD': 'yourdbpassword',
            'HOST': 'localhost',
            'PORT': '',
        }
    }

    SECRET_KEY = 'your-secret-key-here'
    DEBUG = True  # Turn to False in production

Make sure to add `local_settings.py` to your `.gitignore` file to prevent it from being tracked by Git.

## Configuring Django to Use local_settings.py

After setting up your `local_settings.py`, you need to ensure Django includes these settings. To do so, modify the `settings.py` file in your Django project to import the contents of `local_settings.py`. This allows you to override or extend the base configuration with your local settings securely.

### Modify settings.py

Open your `settings.py` file and add the following code at the very end of the file:

```python
# settings.py

# ... your existing settings ...

# Use local_settings.py if it exists
try:
    from .local_settings import *
except ImportError:
    pass
```


### 4. Initialize the Database
Run migrations to set up your database schema.

    python manage.py migrate

### 5. Start the Development Server
Run the server and navigate to the provided local address to start using the application.

    python manage.py runserver

Now, you can access the application in your browser, register an account, and begin shortening URLs!

## Author
- Adam Chrzanowski

## License
This project is open-source and free to use.

## Acknowledgements
Thanks to all the contributors and the Django community for support and guidance.

