# pyfast
## Python backend project using FastAPI framework

### Step by step on running this project

* Creates a virtual environment:
python -m venv ./venv/

* Activate the virtual environment:
 * Windows : .\venv\Scripts\Activate.bat
 * Linux : source venv/bin/activate

* Install the required library for this project:
pip install -r requirements.txt

### Run the application:

* Go to folder app then run
uvicorn main:myapp --reload --port 8081

* Open browser or use postman to test the app
http://localhost:8081/
