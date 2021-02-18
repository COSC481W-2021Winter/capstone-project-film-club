# **FILM CLUB**

# Getting Started

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

# File Structure Standard

Django is built to make the jump from installation to development as quick as possible. In doing this, Django does a lot of the work for you. For example, it organizes the entire project by default. The [Django tutorial](https://docs.djangoproject.com/en/3.1/intro/tutorial01/#creating-a-project) gives a brief overview of the file structure.

# Description of Prototype

1. Landing Screen - A screen with the film club logo and information about the product
2. Login Screen - A screen where the user will enter their login credentials or select create account 
3. New Account Screen - A screen where new users will enter information about  themselves and create a profile. The user will go through a new user process where they enter media categories they like to help create their profile. 
4. Home Screen - The screen users are directed to this page on sign in, this is where the recommendation feed lives. For the prototype the recommendations will be based on the users media selections. It will also show friends and watch history.  
5. Movie Profile Screen - The users data on media they have viewed  and reviewed can be viewed, edited and deleted here.
6. Upload Data Screen - the user can add new media to their profile here
7. User Profile Screen - the user can view/edit/delete information from their personal profile
8. Reset Password/Email Screen - users who forgot their passwords/emails can reset them here.

# ABOUT ME: *THE PERSONA*

![alt text](https://img.freepik.com/free-photo/a-man-in-a-bedroom-at-home-in-front-of-a-laptop-watching-movies-at-night_163305-16739.jpg?size=664&ext=jpg)

- Name              |   Tyler Durdem
- Sex               |   Male
- Age               |   28
- Economic Status   |   Middle Class ($50,000 - $74,999)
- Employment Status |   Employed
- Educational Level |   University
- Marital Status   |   Single
- Hobbies/Interests |   Movies, Anime, and Television Watching

Tyler is a movie enthusiast.  But because he has viewed so many films on his streaming services he has run out of new material.  He also wishes to have a more honest opinion on what he might like given the corporate bias the streaming services have when they recommend their new material to him.  He also wants to connect with a growing social media community that shares similar interests and become part of a larger community. Tyler values his family members and close friends who like to spend time watching movies on a regular basis. He also values the recommendations/suggestions he receives from other users so that they can discuss/have friendly conversations about various topics relating to film and television.  

# SCREENING QUESTIONS
- What kind of movies are they watching?
- How do you feel about sharing your movie recommendations with others?
- Why did you decide to join our community?
- Top five movies
- What are your favorite genres?
- What are your least favorite genres?
- What languages do you watch films in?
- How much time do you spend watching movies?
- Do you currently have(or had in the past) a subscription to a streaming service?
- What makes you want to watch a film?

# APP VALUES
- We formulate relationships that make a fun and positive difference in our customers' lives.
- We deliver an outstanding product and service that, together, brings premium value to our customers.
- We work together collaboratively and cooperatively to meet the needs of our customers.
- We hope to establish a safe and interactive space for our customers to help share their thoughts and ideas.
- We value our people and their uniqueness across boundaries. 

Our film recommendation app will allow our customers to enjoy movie recommendations from friends and family. It fills their need of finding new film recommendations.  Our application will provide the recomendations based off of a calculated rating using their previous viewing habits and those of other users.    
