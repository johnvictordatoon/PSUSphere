# PSUSphere

PSUSphere is a web-based application designed to manage and organize student-related data for universities. It provides features for managing organizations, organization members, students, colleges, and academic programs.

## Features

- **Organization Management** - add, edit, delete, and view organizations.
- **Organization Members** - manage members of organizations, including their roles and joining dates.
- **Student Management** - add, edit, delete, and view student information.
- **College Management** - manage colleges and their associated programs.
- **Program Management** -  add, edit, delete, and view academic programs.

## Technologies Used

- Django (Python)
- HTML, CSS, JavaScript
- SQLite (default Django database)
- Faker (for generating fake data)

## Installation & Use

1. Clone the repository
2. Navigate to the project directory (`cd PSUSphere`)
3. Create a virtual environment (`python -m venv psuenv`)
4. Activate the virtual environment

    - Windows - (`psuenv\Scripts\activate`)

    - macOS/Linux - (`source psuenv/bin/activate`)

5. Install the **requirements.txt** using `pip install -r requirements.txt`
6. Run database migrations (`python manage.py migrate`)
7. Start the server (`python manage.py runserver`)

## Usage
1. Open your browser and navigate to the provided URL (example: `http://127.0.0.1:8000/`).
2. Use the navigation menu to manage organizations, students, colleges, and programs.

## Folder Structure
- `projectsite/` - contains the main Django project settings and configurations.
- `studentorg/` - contains the app for managing organizations, students, colleges, and programs.
- `templates/` - contains HTML templates for the frontend.
- `static/` - contains static files like CSS, JavaScript, and images.

<br>
<br>

# Contributors

<img src="img/johnvictor.png" alt="John Victor" style="border-radius:50%;" width="150"> 

### John Victor Dato-on 
Repository Owner

<img src="img/cristel.jpg" alt="Marie Cristel" style="border-radius:50%;" width="150"> 

### Marie Cristel Bugayong
Collaborator