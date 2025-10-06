# BookShelf - Personal Library Manager

**CS50W Capstone Project**

## Project Overview

BookShelf is a comprehensive Django-based web application designed to help users manage their personal reading libraries. The application provides a complete solution for tracking books across different reading stages—from planned future reads to currently reading to completed books—while offering visual statistics and progress tracking to motivate continued reading habits. Built with Django's robust framework and enhanced with modern web technologies including Bootstrap 5 and AJAX, BookShelf demonstrates a full-stack implementation of a database-driven web application with user authentication, dynamic content updates, and responsive design principles.

## Distinctiveness and Complexity

### Distinctiveness

BookShelf represents a distinctly different approach from the other projects completed throughout CS50W's curriculum. Unlike the e-commerce Project 2 (Commerce), which focuses on auction listings and bidding mechanisms, or Project 4 (Network), which emphasizes social interactions and post-based content sharing, BookShelf addresses the domain of personal library management and reading habit tracking. This project is not a social network—users maintain private, individual libraries without the ability to follow other users or interact with others' collections. It is not an e-commerce platform—there are no transactions, shopping carts, or product listings. Instead, BookShelf occupies its own unique niche as a personal productivity and tracking application.

The application's distinctiveness is further demonstrated through its focus on data visualization and progress metrics. While other course projects primarily display lists of items or posts, BookShelf goes beyond simple CRUD operations by calculating and displaying dynamic statistics, including completion percentages shown through visual progress bars, categorized book counts displayed in color-coded cards, and real-time filtering capabilities. The user experience centers around personal goal tracking and achievement visualization rather than content consumption or commercial transactions.

Additionally, BookShelf implements a unique user profile extension system using Django signals. When a new user registers, the application automatically creates an associated Profile model instance through post_save signals, demonstrating advanced Django patterns that were not required in previous course projects. This seamless integration of multiple related models showcases database design principles and Django's ORM capabilities in ways that extend beyond the course's previous requirements.

### Complexity

BookShelf demonstrates substantial technical complexity through multiple sophisticated features and implementation patterns that exceed the baseline requirements of a simple CRUD application.

**Authentication and Authorization System**: The project implements a complete user authentication system built upon Django's authentication framework. This includes custom user registration using an extended `UserCreationForm` with email validation, secure login and logout functionality with proper redirect handling, and comprehensive session management. The application employs login-required decorators to protect sensitive views, ensuring that book management operations are restricted to authenticated users. Furthermore, the implementation includes automatic profile creation through Django's signal system, where a `post_save` signal triggers the creation of a Profile instance whenever a new User is created, demonstrating advanced Django patterns for model relationships.

**AJAX-Powered Dynamic Updates**: One of the most significant complexity factors in BookShelf is its implementation of asynchronous JavaScript (AJAX) functionality. The dashboard allows users to update book statuses and delete books without requiring page reloads, providing a smooth, modern user experience. This feature required implementing multiple components: server-side JSON endpoints that handle POST requests and return structured responses, client-side JavaScript using the Fetch API to make asynchronous HTTP requests, CSRF token handling to maintain security in AJAX requests, and DOM manipulation to update the interface immediately upon successful operations. The JavaScript code includes error handling, loading states, confirmation dialogs for destructive actions, and smooth CSS animations for visual feedback.

**Database Architecture and Relationships**: The application's database design demonstrates complexity through its use of multiple related models with different relationship types. The Book model maintains a foreign key relationship to Django's User model, implementing proper ownership patterns where each book belongs to exactly one user. The Profile model uses a one-to-one relationship with User, extending the built-in authentication model with additional fields such as bio, location, and birth date. These relationships employ the `related_name` parameter to enable intuitive reverse queries (e.g., `user.books.all()` and `user.profile`), and the models include proper `__str__` methods, Meta class ordering, and field validators.

**Dynamic Statistics and Filtering**: The dashboard view performs complex database queries and calculations to present real-time statistics. The view function aggregates data across multiple book statuses, calculates completion percentages, and supports dynamic filtering through URL parameters. This required implementing: count queries using Django ORM's `filter()` and `count()` methods, conditional queryset building based on GET parameters, mathematical calculations for percentage completion with proper zero-division handling, and context dictionary construction to pass multiple calculated values to templates. The statistics update automatically when books are added, deleted, or their status changes, demonstrating reactive data presentation.

**Responsive Frontend Design**: The user interface showcases complexity in its responsive design implementation using Bootstrap 5's grid system and custom CSS. The application adapts seamlessly across device sizes from mobile phones to desktop displays. Custom CSS includes hover effects with transform animations, transitions for smooth state changes, a custom color palette applied consistently across components, and carefully designed card layouts that reflow appropriately at different breakpoints. The navigation bar collapses into a mobile-friendly hamburger menu on smaller screens, and touch targets are sized appropriately for mobile interaction.

**Form Handling and Validation**: BookShelf implements multiple custom Django forms with Bootstrap styling and comprehensive validation. The `RegisterForm` extends `UserCreationForm` to include email validation and custom widget attributes for styling. The `BookForm` uses ModelForm to generate fields from the Book model while adding custom CSS classes and placeholder text. The `ProfileForm` allows users to update their extended profile information with proper date input widgets. All forms include server-side validation, display error messages clearly to users, and maintain proper CSRF protection.

## File Contents and Structure

### Django Project Configuration

**BookShelf/settings.py**: Contains all project configuration including installed apps (with 'library' app registered), middleware configuration, template settings (specifying the library/templates directory), database configuration (using SQLite3 for development), static files settings, authentication redirects (LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL), and security settings including SECRET_KEY and DEBUG mode.

**BookShelf/urls.py**: Defines the main URL routing configuration, mapping '/admin/' to Django's admin interface and including all application URLs from library.urls using Django's `include()` function for modular URL management.

**BookShelf/wsgi.py** and **BookShelf/asgi.py**: Provide WSGI and ASGI application callables for deploying the Django project to production servers with support for both synchronous and asynchronous request handling.

### Application Core Files

**library/models.py**: Defines two Django models:
- `Book` model with fields for title (CharField, max 200 chars), author (CharField, max 100 chars), status (CharField with choices: Reading/Completed/Planned), date_added (auto-generated DateTimeField), and user (ForeignKey to User with CASCADE deletion). Includes Meta class for ordering by most recent first and a `__str__` method for readable representations.
- `Profile` model with a OneToOneField to User, bio (TextField, optional), location (CharField, optional), and birth_date (DateField, optional). Includes signal receivers for automatic profile creation and saving when User instances are created or updated.

**library/views.py**: Contains nine view functions implementing all application logic:
- `index`: Renders the homepage with welcome content
- `dashboard`: Displays user's books with calculated statistics (total, completed, reading, planned counts and completion percentage), supports filtering by status parameter
- `add_book`: Handles GET requests to display BookForm and POST requests to create new Book instances associated with the logged-in user
- `update_book`: AJAX endpoint accepting POST requests to update a book's status, returns JSON response with success status
- `delete_book`: AJAX endpoint accepting POST requests to delete a book, returns JSON response
- `register_view`: Handles user registration using RegisterForm, creates User and automatically triggers Profile creation
- `login_view`: Authenticates users using Django's AuthenticationForm
- `logout_view`: Logs out users and redirects to homepage
- `profile_view`: Allows users to view and update their Profile information

**library/forms.py**: Defines three custom Django forms:
- `BookForm`: ModelForm for Book model with custom widget attributes for Bootstrap styling
- `RegisterForm`: Extends UserCreationForm to add email field with validation and custom widget styling
- `ProfileForm`: ModelForm for Profile model with custom date input widget and Bootstrap classes

**library/urls.py**: Maps URL patterns to view functions including paths for homepage ('/'), dashboard ('/dashboard/'), add book ('/add/'), update book ('/update/<id>/'), delete book ('/delete/<id>/'), authentication URLs ('/auth/register/', '/auth/login/', '/auth/logout/'), and profile ('/profile/').

**library/admin.py**: Registers Book and Profile models with Django admin, configuring list displays, filters, and search fields for easy administration through Django's built-in admin interface.

**library/tests.py**: Contains unit tests for models and views, testing Book creation, Profile auto-creation, view access controls, and authentication requirements.

### Template Files

**library/templates/library/base.html**: Master template providing the overall HTML structure including Bootstrap CDN links, navigation bar with conditional content based on authentication status, messages display section for Django messages framework, main content block for child templates to override, footer section, and JavaScript includes. Uses Django template inheritance with `{% block %}` tags.

**library/templates/library/index.html**: Homepage template extending base.html, featuring a hero section with project description and call-to-action buttons, conditional display showing different options for authenticated vs. anonymous users, and a features showcase section highlighting key application capabilities with Bootstrap Icons.

**library/templates/library/dashboard.html**: Most complex template displaying the user's library, includes four statistics cards showing counts with color coding, a progress bar visualizing reading completion percentage, filter buttons for status-based filtering, a grid of book cards with dropdowns for status changes and delete buttons, and integration with dashboard.js for AJAX functionality.

**library/templates/library/add.html**: Form template for adding new books, uses Django form rendering with Bootstrap styling, includes field labels and error display, and provides submit and cancel buttons.

**library/templates/library/register.html**: User registration form with username, email, and password fields, displays Django form validation errors, includes password requirements help text, and provides a link to login page for existing users.

**library/templates/library/login.html**: Authentication form with username and password fields, handles form errors from Django's AuthenticationForm, and provides a link to registration page for new users.

**library/templates/library/profile.html**: Displays read-only account information (username, email, join date) and an editable form for Profile fields (bio, location, birth date) with save functionality.

### Static Files

**library/static/library/styles.css**: Custom stylesheet containing layout rules for responsive design, component styles for cards, buttons, and forms, animation definitions including hover effects and transitions, color scheme implementation maintaining visual consistency, mobile-specific media queries for responsive breakpoints, and utility classes for spacing and typography.

**library/static/library/dashboard.js**: JavaScript file implementing AJAX functionality including a getCookie function for retrieving CSRF tokens from cookies, event listeners for status update links that send POST requests and update UI elements, event listeners for delete buttons with confirmation dialogs, DOM manipulation functions to update badges and remove cards, error handling and user feedback with dynamically created alert messages, and page reload triggers after AJAX operations to refresh statistics.

### Supporting Files

**requirements.txt**: Lists Python package dependencies (currently only Django>=4.2,<5.0), used with `pip install -r requirements.txt` to set up the project environment.

**manage.py**: Django's command-line utility for administrative tasks including running the development server, creating migrations, applying migrations, creating superusers, and running tests.

**library/migrations/**: Directory containing database migration files generated by Django's migration system, including 0001_initial.py which creates the Book and Profile tables with proper field definitions and relationships.

## How to Run the Application

### Prerequisites

Before beginning, ensure you have Python 3.8 or higher installed on your system. You can verify your Python version by running `python --version` or `python3 --version` in your terminal. You will also need pip, Python's package installer, which typically comes bundled with Python installations.

### Installation Steps

**Step 1: Install Dependencies**

Navigate to the project directory in your terminal and install the required Python packages. The project uses Django as its primary dependency:

```bash
pip install -r requirements.txt
```

This command reads the requirements.txt file and installs Django version 4.2 or compatible versions. If you encounter permission errors, you may need to use `pip install --user -r requirements.txt` or create a virtual environment first.

**Step 2: Apply Database Migrations**

Django uses migrations to create and modify database tables. Run the following commands to create the necessary database schema:

```bash
python manage.py makemigrations
python manage.py migrate
```

The first command generates migration files based on your models (if any changes have been made), and the second command applies these migrations to create tables for User, Book, Profile, and Django's built-in models (sessions, admin, etc.) in the SQLite database file (db.sqlite3).

**Step 3: Create a Superuser (Optional but Recommended)**

To access Django's admin interface for managing users and books directly, create an administrator account:

```bash
python manage.py createsuperuser
```

Follow the interactive prompts to enter a username, email address, and password. This account will have full access to the admin panel at http://127.0.0.1:8000/admin/.

**Step 4: Run the Development Server**

Start Django's built-in development server:

```bash
python manage.py runserver
```

The server will start on port 8000 by default. You should see output indicating the server is running and watching for file changes. The server will automatically reload when you make changes to Python files.

**Step 5: Access the Application**

Open your web browser and navigate to:
- **Homepage**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/ (login with superuser credentials)

### Using the Application

1. **Register a New Account**: Click the "Register" link in the navigation bar, fill out the registration form with a username, email, and secure password (minimum 8 characters, not entirely numeric), and submit the form. You'll be redirected to the login page with a success message.

2. **Log In**: Enter your username and password on the login page. Upon successful authentication, you'll be redirected to your personal dashboard.

3. **Add Your First Book**: Click "Add Book" in the navigation menu, enter the book's title and author, select an initial status (Reading, Completed, or Planned), and submit the form. You'll be redirected to the dashboard where your book now appears.

4. **Manage Your Library**: On the dashboard, you can view all your books in a card-based grid layout, click the "Change Status" dropdown on any book card to update its status without reloading the page, click the filter buttons ("All Books", "Reading", "Completed", "Planned") to view specific subsets of your library, click the trash icon to delete a book after confirming the action, and monitor your reading progress through the statistics cards and progress bar at the top of the page.

5. **Update Your Profile**: Click your username in the navigation bar and select "Profile" from the dropdown menu, add or edit your bio, location, and birth date, and save your changes. This information is stored in your Profile model instance.

## Additional Information

### Technologies and Design Decisions

**Django Framework**: The project is built on Django 4.2, chosen for its robust ORM, built-in authentication system, template engine, and comprehensive security features. Django's MVT (Model-View-Template) architecture provides clear separation of concerns and maintainable code structure.

**Database**: SQLite3 is used as the default database for development purposes. It requires no separate server process and stores all data in a single file (db.sqlite3). For production deployment, the database can be easily switched to PostgreSQL or MySQL by modifying settings.py.

**Bootstrap Framework**: Bootstrap 5.3 provides responsive CSS components and JavaScript plugins, ensuring the application works seamlessly across devices from mobile phones to large desktop displays. The framework's grid system, navigation components, cards, buttons, and forms are used extensively throughout the interface.

**AJAX Implementation**: The application uses the modern Fetch API for asynchronous HTTP requests rather than older methods like XMLHttpRequest or jQuery.ajax(). This provides a cleaner, promise-based interface for handling asynchronous operations. All AJAX requests include proper CSRF token handling to maintain Django's security protections.

**User Experience Enhancements**: The application includes several features to improve user experience: Django's messages framework displays success and error notifications that auto-dismiss after 3 seconds, confirmation dialogs prevent accidental deletion of books, smooth CSS transitions and animations provide visual feedback for user actions, and loading states could be implemented for AJAX operations (future enhancement).

### Security Considerations

BookShelf implements multiple security best practices:
- **CSRF Protection**: All forms and AJAX requests include CSRF tokens to prevent cross-site request forgery attacks
- **Authentication Requirements**: Sensitive views use `@login_required` decorators to ensure only authenticated users can access book management features
- **Password Validation**: Django's built-in password validators enforce minimum length requirements, check for common passwords, and ensure passwords aren't too similar to user information
- **SQL Injection Prevention**: Django's ORM automatically parameterizes queries, preventing SQL injection vulnerabilities
- **Session Security**: Django manages sessions securely with httponly cookies

### Testing

The project includes unit tests in library/tests.py covering:
- Model creation and string representation
- Automatic profile creation via signals
- View access controls and authentication requirements
- URL routing and template rendering

Run tests with:
```bash
python manage.py test library
```

All tests should pass, confirming that core functionality works as expected.

### Future Enhancements

While BookShelf is fully functional for its intended purpose, several enhancements could further improve the application: implementing book cover image uploads using Django's ImageField and file storage system, integrating with the Google Books API or Open Library API to auto-populate book information from ISBN numbers, adding reading goals where users can set targets for books to complete in a time period, implementing a review and rating system where users can add personal notes and ratings for completed books, creating data visualization with charts showing reading trends over time using libraries like Chart.js, adding export functionality to download library data as CSV or PDF, implementing full-text search across titles and authors, allowing book categorization with user-defined genres or tags, and adding a dark mode toggle for improved accessibility in different lighting conditions.

## Conclusion

BookShelf represents a complete, production-ready Django web application that demonstrates mastery of full-stack web development concepts including database design, user authentication, dynamic content rendering, asynchronous JavaScript, responsive design, and secure coding practices. The project fulfills all requirements for CS50W's Capstone project while providing a genuinely useful tool for tracking personal reading habits.

---

**Author**: CS50W Student  
**Course**: Harvard CS50's Web Programming with Python and JavaScript  
**Project Type**: Capstone (Final Project)  
**Year**: 2024

This project is submitted as the Capstone requirement for CS50W and is created for educational purposes.
