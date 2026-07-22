# Rentify

> **Rentify** is a web application for renting and managing real estate listings.

The platform allows **tenants** to search for properties, view detailed information, create booking requests, and leave reviews.
**Landlords** can create and manage their own property listings and process incoming booking requests.

---

## Features

### Authentication and Authorization

* User registration and login
* Custom user model with role-based access
* Two user roles:

  * **Tenant**
  * **Landlord**
* Protected routes and API endpoints
* Permission-based access control

### Property Management

Landlords can:

* Create property listings
* Edit existing listings
* Soft-delete their own properties
* Temporarily activate or deactivate listings
* Upload multiple property images
* Manage their own properties through a dedicated cabinet

Each property can contain:

* Title
* Description
* Location
* Price per night
* Number of rooms
* Property type
* Multiple images
* Reviews and rating information

### Search, Filtering and Sorting

The property list supports:

* Keyword search
* Search by title, description, and location
* Filtering by:

  * Property type
  * Location
  * Number of rooms
  * Price range
* Sorting by:

  * Price
  * Creation date

### Booking System

Tenants can:

* Select a property
* Choose check-in and check-out dates
* Create booking requests
* View their bookings
* Cancel bookings when allowed

Landlords can:

* View incoming booking requests
* Approve bookings
* Reject bookings

The system also prevents invalid booking situations such as overlapping reservations.

### Reviews and Ratings

Users who have completed a booking can:

* Leave a rating
* Write a review

Property pages display:

* Average rating
* Number of reviews
* Recent reviews

### Search and View History

The application tracks user activity such as:

* Search queries
* Property views

This data can be used to identify popular searches and popular properties.

---

## Technology Stack

| Layer                 | Technologies                                                 |
| --------------------- | ------------------------------------------------------------ |
| **Backend**           | Python, Django, Django REST Framework, Django Filter, SQLite |
| **Frontend**          | HTML, CSS, JavaScript, Bootstrap                             |
| **Development Tools** | Git, GitHub, REST API, Docker                                |

---

## Project Structure

```text
Rentify/
│
├── bookings/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── properties/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── filters.py
│   └── urls.py
│
├── reviews/
│   ├── models.py
│   ├── serializers.py
│   └── views.py
│
├── users/
│   ├── models.py
│   ├── serializers.py
│   └── views.py
│
├── templates/
│
├── static/
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## API

The application uses a REST API for communication between the frontend and backend.

### Example endpoints

```text
/api/properties/
/api/properties/{id}/
/api/bookings/
/api/reviews/
/api/users/
```

### Property API functionality includes:

* Listing properties
* Creating properties
* Updating properties
* Deleting properties
* Activating and deactivating properties
* Uploading property images

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd Rentify
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment on Windows

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Start the development server

```bash
python manage.py runserver
```

The application will be available at:

```text
http://127.0.0.1:8000/
```

---

## Environment Variables

Sensitive configuration should be stored in environment variables.

### Example development configuration

```env
SECRET_KEY=your-secret-key
DEBUG=True
```

### Example production configuration

```env
DEBUG=False
```

---

## Database

The project currently uses **SQLite** for development.

The database structure is managed through Django migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Docker

Docker support is planned as the next deployment step.

The goal is to run the application in an isolated containerized environment using:

* Docker
* Docker Compose
* Environment variables
* A production-ready application server

---

## Project Goals

The main goal of Rentify is to provide a complete rental platform with:

* Role-based access control
* Property management
* Search and filtering
* Booking management
* Reviews and ratings
* User activity history
* Containerized deployment

---

## License

This project was created for educational and development purposes.
