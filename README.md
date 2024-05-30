The Pokémon Database Project is a comprehensive database that aims to collect and organize data related to the Pokémon franchise. It includes information about Pokémon species, moves, abilities, regions, notable trainers, and more. The project utilized web scraping techniques to gather data from online sources and store it in a relational database management system. Once the data was gathered and organized work began on applications that would allow users to interact with the underlying database. 
\
My goal is to build a web application that gives users access to a variety of tools helpful to Pokemon trainers. See below for more.

## Features

- **Filter Pokemon**: Users can filter Pokemon based on type, region, abilities, stat information.
- **Stat Calculation**: Users can calculate the exact stats any Pokemon would have based on user provided EVs, IVs, and Nature.
- **Autocomplete Functionality**: Certain fields were provided with autocomplete functionality to improve the user experience.
- **(TBD) User Accounts**: Give Users the ability to create accounts, save their favorite Pokemon, team configurations (for competitive analysis), and interact with other users.
- **(TBD) Pokemon Comparison Tool**: Allow users to select multiple Pokemon to compare their stats side by side.
- **(TBD) Other Calculator Tools**: Damage calculator / team builder.
- **(TBD) Inclusion of Competitive Information**: To appeal to the more advanced user, include data regarding competitive strategies.
- **(TBD) Developed User Interface**: Plans to develop a user-friendly front end for easy browsing. 

## Technologies Used
- Django
- Python
- PostgreSQL
- HTML/CSS
- JavaScript
- (Eventually) React.js

\
\
Usage
\
\
Clone the repository to your local machine.\
Set up a PostgreSQL database and configure the connection parameters.\
Run the SQL scripts to create the necessary tables and populate them with data.\
Use the provided Python scripts for web scraping and data manipulation.\
(Optional) Develop the user interface and RESTful API using Django.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/rashadat1/Pokemon-Database.git
    cd pokemonDatabase
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database**:
    - Install PostgreSQL if not already installed.
    - Create a new PostgreSQL database and user.
    - Run the web scraping functions to populate your database: web scraper.py, abilityscraper.py, movelist_scraper.py, region_table.py, native_region_scraper.py, Trainer_Table.py.
    - Update the `DATABASES` settings in `pokemonDatabase/settings.py` with your database credentials.

5. **Apply the migrations**:
    ```bash
    1. python manage.py makemigrations
    2. python manage.py migrate
    ```

6. **Create a superuser**:
    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

9. **Open your web browser and navigate to**:
    ```
    http://127.0.0.1:8000/
    ```
