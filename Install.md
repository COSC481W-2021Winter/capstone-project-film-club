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
      ```
4. Install requirements
      ```
      pip install -r requirements.txt
      ```
5. Migrate any changes
      ```
      python manage.py migrate
      ```
6. Run the server
      ```
      python manage.py runserver
      ```

After starting the server, you can access it at localhost:8000
