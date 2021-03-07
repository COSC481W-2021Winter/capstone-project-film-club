### Prerequisites

- [Python](https://www.python.org/)==3.8.2
- [Django](https://www.djangoproject.com/)==3.1.5
- Pip

### Installation

Run the following commands in the root directory:

1. Install virtualenv
      ```
      pip install virtualenv
      ```
2. Create a virtual environment
      ```
      virtualenv env
      ```
3. Start the virtual environment
      ```
      source env/bin/activate
4. Install requirements
      ```
      pip install -r requirements.txt
      ```
5. Install SQLITEN (Optional on Most Systens)
      ```
      On some sytems SQLITE is not installed with the python.
      Please check if SQLITE is on your system.
      Please check waht you need to do to get SQLITE on your system.  
      ```
7. Migrate any changes
      ```
      python manage.py migrate
      ```
7. Run the server
      ```
      python manage.py runserver
      ```

After starting the server, you can access it at localhost:8000
