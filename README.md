# Diplomacy: Web and Mobile
Making a cross-platform Diplomacy app for web and mobile!

So far:
Frontend will be React (web) and ReactNative (mobile)
Backend will be Django

Using local databases for development

## Contributors
Ryanne Wilson

## Requirements
- Django
- PostgreSQL
- Python

## Setup
- Move to the ```backend``` directory
- run ```pip install -r backend/requirements.txt``` for backend dependencies
- run ```npm install``` for frontend dependencies
- Copy ```.env.example``` to ```.env``` and modify values to your desired values (backend)
- Make a PostgreSQL username and password same as DB_USER and DB_PASSWORD
- Create a PostgreSQL database with the same name as DB_DATABASE (diplomacy)
- run ```python manage.py makemigrations``` and ```python manage.py migrate```
- Move to the ```frontend``` directory
- Copy ```.env.example``` to ```.env``` and keep it the same (frontend)

# Good Practices
**Branches** should be short-lived for small features.
Merge changes through pull requests & code reviews.
Naming Conventions:
- feature/your-name/feature-name
- bugfix/bug-to-fix
- release/v#.#.#

# Goals (in no particular order)
- Colorblind settings
- AJAX updates for press/notifications
- Ability to upload, use, rate variants made by you and other players
- Sandboxes like Backstabbr
- Ability to see other user's stats
- Protections against people using multiple accounts (look at webDip)
- Reliability / Ranking system (look at Boardgamearena.com?)
- Pronoun tags / other public profile settings
- Warning that submitted moves are invalid(?)
- Spectator option?
- Ability to GM games:
    - Edit settings
    - Change deadlines during the game
    - Replace players as needed
    - Read comms
    - See orders and who has/n't entered them
    - See draw votes
    - End game early
    - CANT change orders/draw votes
- Vote buttons for drawing, ending the game early, pausing, extending...
- Different game settings/modes such as:
    - Classic first to 18
    - Game ends after X turns
    - Public Press
    - Gunboat
    - Fog of War
    - Anonymity settings
    - Minor powers (versailles style)