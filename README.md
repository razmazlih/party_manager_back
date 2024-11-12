
# Party Manager Backend

This project is a backend API for managing party-related events, built using Django.

## Project Structure

- **models.py**: Defines the database models representing the main entities in the application.
- **views.py**: Contains the logic for handling HTTP requests and providing responses for various endpoints.
- **serializers.py**: Used to convert models to JSON format and vice versa for API communication.
- **urls.py**: Maps URL endpoints to view functions.
- **settings.py**: Configures the Django project settings.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/razmazlih/party_manager_back.git
    ```

2. Navigate to the project directory:
    ```bash
    cd party_manager_back
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables as per `settings.py` requirements.

## Usage

To start the server:
```bash
python manage.py runserver
```

## API Endpoints

The API includes the following endpoints:

- **Registration and Authentication**:
  - `POST /api/register/` - Register a new user.
  - `POST /api/token/` - Obtain JWT access token.
  - `POST /api/token/refresh/` - Refresh the access token.

- **Event Management**:
  - `GET /api/events/` - Retrieve a list of all events.
  - `POST /api/events/` - Create a new event.
  - `GET /api/events/{id}/` - Retrieve details of a specific event by ID.
  - `PUT /api/events/{id}/` - Update an existing event.
  - `DELETE /api/events/{id}/` - Delete an existing event.
  - `GET /api/events/name-date/` - Get a list of events with name and date only.

- **Reservation Management**:
  - `GET /api/reservations/` - Retrieve a list of all reservations.
  - `POST /api/reservations/` - Create a new reservation.
  - `GET /api/reservations/{id}/` - Retrieve details of a specific reservation.
  - `PUT /api/reservations/{id}/` - Update an existing reservation.
  - `DELETE /api/reservations/{id}/` - Delete a reservation.

- **Comment Management**:
  - `GET /api/comments/` - Retrieve a list of all comments.
  - `POST /api/comments/` - Create a new comment.
  - `GET /api/comments/{id}/` - Retrieve details of a specific comment.
  - `PUT /api/comments/{id}/` - Update an existing comment.
  - `DELETE /api/comments/{id}/` - Delete a comment.

- **Notification Management**:
  - `GET /api/notifications/` - Retrieve a list of all notifications.
  - `POST /api/notifications/` - Create a new notification.
  - `GET /api/notifications/{id}/` - Retrieve details of a specific notification.
  - `PUT /api/notifications/{id}/` - Update an existing notification.
  - `DELETE /api/notifications/{id}/` - Delete a notification.

- **Additional Services**:
  - `GET /api/user/is_organizer/` - Check if the user is an event organizer.

## License

This project is licensed under the MIT License.
