# EventEase: Your Event Management Hub

## Overview

EventEase is a desktop application designed to streamline the management of event ticketing systems. It provides a comprehensive suite of tools to handle user registration, event creation, ticket sales, and venue details, all within an intuitive GUI powered by Python and PyQt6.

The application seamlessly integrates with a PostgreSQL database for efficient data storage and retrieval, ensuring reliability and scalability.

## Features

- **User Management**
  - Secure user registration and login with password hashing.
  - Easy account management with role-specific features.
- **Event Management**
  - Create, update, and delete events with comprehensive details:
    Event name, category, venue, date, time, ticket pricing, and availability.
  - View upcoming events and manage bookings.
- **Ticket Booking**
  - Book tickets for events, with real-time updates on availability.
  - Cancel bookings and view purchase history.
- **Data Filtering and Search**
  - Apply filters by category, venue, date range, time range, and price range.
  - Search events by name for quick access.

## Installation

1. Clone this repository:
   ```bash
   git clone git@github.com:abdomody35/eventease.git
   ```
2. Navigate to the project directory:
   ```bash
   cd eventease
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the PostgreSQL database:
   - Configure the .env file with your database credentials:
     ```
     DB_NAME=<your-database-name>
     DB_USER=<your-database-username>
     DB_PASSWORD=<your-database-password>
     DB_HOST=localhost
     DB_PORT=5432
     ```
   - Start the database container using Docker Compose:
     ```bash
     docker-compose up -d
     ```
   - Apply the schema and seed data:
     ```bash
     psql -U <DB_USER> -d <DB_NAME> -f schema.sql
     psql -U <DB_USER> -d <DB_NAME> -f seed.sql
     ```
5. Run the application:
   ```bash
   python main.py
   ```

## Usage

1. Launch the application by running main.py.
2. Register or log in as a user.
3. Navigate through the intuitive interface to create events, book tickets, or manage venues.
4. Use filters and search options to explore events effortlessly.

## Dependencies

- Python 3.x: Core programming language.
- PyQt6: For the graphical user interface.
- psycopg2-binary: PostgreSQL database connectivity.
- python-dotenv: Manage environment variables.
- bcrypt: Secure password hashing.

## Project Structure

```
project-root/
├── main.py               # Entry point of the application
├── requirements.txt      # List of required Python packages
├── docker-compose.yml    # Docker configuration for PostgreSQL
├── schema.sql            # Database schema
├── seed.sql              # Initial database data
├── src/                  # Source code
│   ├── auth/             # Authentication-related modules
│   ├── database/         # Database connection and operations
│   ├── models/           # Data models for users, events, venues, etc.
│   ├── ui/               # User interface components
└── .env                  # Environment variable configuration
```

## Author

**Abdelrahman Mostafa**  
📧 **[abdomody35@gmail.com](mailto:abdomody35@gmail.com)**
