# Blogging Platform API

## Overview
The Blogging Platform API is a RESTful API built using Django and Django REST Framework. It allows users to manage blog posts, including creating, updating, deleting, and viewing posts. The API supports user authentication and provides features for categorization and author-based filtering.

## Features
- **Blog Post Management**: Create, Read, Update, and Delete (CRUD) blog posts with attributes such as Title, Content, Author, Category, Published Date, Tags, and Created Date.
- **User Management**: Manage users with unique Username, Email, and Password. Only authenticated users can manage their own posts.
- **Filtering**: View posts by Category or Author, with optional filtering by Published Date or Tags.
- **Search Functionality**: Search for blog posts by Title, Content, Tags, or Author, with additional filters available.
- **Pagination and Sorting**: Implement pagination for blog post listings and sorting options by Published Date or Category.

## Technical Requirements
- **Database**: Utilizes Django ORM for database interactions with models for Blog Posts, Users, Categories, and Tags.
- **Authentication**: Implements user authentication using Django’s built-in system, with optional JWT for enhanced security.
- **API Design**: Built with Django Rest Framework, following RESTful principles and proper error handling.

## Deployment
The API can be deployed on platforms like Heroku or PythonAnywhere, ensuring accessibility and security in the deployed environment.

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd blogging-platform-api
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```
   python manage.py migrate
   ```
5. Run the development server:
   ```
   python manage.py runserver
   ```

## Usage
- Access the API endpoints as defined in the `urls.py` files within the `blog` and `users` applications.
- Use tools like Postman or curl to interact with the API.

## Stretch Goals (Optional)
- User Comments
- Post Likes and Ratings
- Drafts and Publishing
- Post Sharing
- User Profiles
- Subscription System
- Markdown Support

## License
This project is licensed under the MIT License.