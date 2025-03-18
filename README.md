
---

# Smart Home Data Management System

## Overview

The **Smart Home Data Management System** is a platform designed to efficiently manage users, houses, residents, appliances, and data in a smart home environment. The system enables secure role-based access control and ensures structured data management through a robust backend. 

## Features

- **User Roles & Authentication**
  - Owners manage their properties.
  - Residents access features specific to their homes.
  - Admins oversee system-wide operations.
  - Secure authentication using JSON Web Tokens (JWT).

- **House & Resident Management**
  - CRUD operations for houses and residents.
  - Ownership and residency relationships managed efficiently.

- **Appliance & Notification Management**
  - Residents can customize notifications for appliances.
  - Real-time or scheduled alerts via email/SMS.

- **Billing & Correspondence System**
  - Admins generate bills for residents.
  - Private and public correspondence management.
  - Redis caching for real-time billing operations.

- **Database Architecture**
  - **PostgreSQL** for structured user, house, and resident data.
  - **MongoDB** for time-series sensor data and correspondence.
  - **Redis** for caching and fast access to billing information.

- **Implementation Stack**
  - Backend: **Flask (Python)**
  - Database: **PostgreSQL, MongoDB, Redis**
  - ORM: **SQLAlchemy**
  - API Testing: **Postman**
  - Deployment: **Docker**

## Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.9+
- PostgreSQL
- MongoDB
- Redis
- Docker (for containerized deployment)

### Setup Instructions

1. Clone this repository:

   ```bash
   git clone <repo_url>
   cd smart-home-data-management
   ```

2. Set up a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables (e.g., `.env` file):

   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/smart_home_db
   MONGO_URI=mongodb://localhost:27017/smart_home_db
   REDIS_URL=redis://localhost:6379/0
   SECRET_KEY=your-secret-key
   ```

5. Run database migrations:

   ```bash
   flask db upgrade
   ```

6. Start the application:

   ```bash
   flask run
   ```




## Future Enhancements

- Integration of AI-based appliance control.
- Enhanced visualization of energy consumption.
- Support for IoT device connectivity.

---

Let me know if you need modifications or additional details! 🚀
