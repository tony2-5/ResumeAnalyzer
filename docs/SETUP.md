## Project Setup
### Backend Setup
1. Setup python virtual environment using `python -m venv venv` from the main directory
2. Activate virtual environment with `source venv/bin/activate` (using mac may differ for other operating systems)
3. Install python backend dependencies using `pip install -r ./requirements.txt` from the main directory
4. Go to backend folder with `cd ./backend`
5. Create a file inside of the backend directory called `.env`
6. Within the .env file define a variable `JWT_KEY` and set it equal to the output of running `openssl rand -hex 32` in the terminal.
7. Run the backend using `fastapi dev main.py`
### Frontend Setup
1. Return to the main directory
2. From the main directory go to the frontend/src folder with `cd ./frontend/src`
3. Run `npm install` to install dependencies
4. Run the frontend using `npm start`

### Running Frontend Tests (After project initialization)
1. From the main directory go to the frontend/src folder with `cd ./frontend/src`
2. Run `npm test`

### Running Backend Tests (After project initialization)
1. From the main directory go to the tests folder `cd ./tests`
2. Run `pytest`