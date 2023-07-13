# Flask Web Application with MySQL Database

This repository contains a basic Flask web application that utilizes a MySQL database for storing user information. The application demonstrates CRUD (Create, Read, Update, Delete) operations and uses the SQLAlchemy library to interact with the database.

## Prerequisites
To run this application, make sure you have the following installed on your system:
- Python (version 3 or higher)
- Flask
- Flask SQLAlchemy
- MySQL database

## Setup
1. Install the necessary dependencies by running the following command:
   ```
   pip install flask flask_sqlalchemy
   ```

2. Create a MySQL database and update the `SQLALCHEMY_DATABASE_URI` configuration in the code to match your database connection details:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
   ```

## Usage
1. Run the Flask web application by executing the following command:
   ```
   python app.py
   ```

2. Access the application in your web browser at `http://localhost:5000/`.

3. The main page provides links to register new users and view a list of existing users.

4. Click on the "Cadastrar" link to navigate to the user registration form.

5. Fill in the required fields and submit the form to register a new user. The user's information will be stored in the MySQL database.

6. Return to the main page and click on the "Lista de Usuários" link to view a list of all registered users. The list will display the users' names, email addresses, and other details.

7. To update or delete a user, click on the corresponding buttons in the user list.

8. The "Mapa" link generates a dynamic HTML page that displays a Google Maps map with markers based on data from a JSON file. The map showcases user positions or any other data you choose to include in the JSON file.

## Customization
Feel free to modify the code to suit your specific requirements. You can extend the application's functionality by adding additional routes and views, incorporating authentication and authorization mechanisms, or enhancing the user interface with CSS and JavaScript.

Make sure to refer to the Flask and SQLAlchemy documentation for more information on how to leverage the frameworks' features and best practices.

Enjoy building your Flask web application with a MySQL database!
