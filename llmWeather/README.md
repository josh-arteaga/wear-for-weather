# Wear for Weather
This is a standard Weather API application that also leverages a local LLM(Ollama) to generate a "What to wear" recommendation for the user

Vite + React
Deep Seek Generated Dark-mode palette in styles.css
I am using ChatGPT to structure the development phases of this plan. 

Had an issue getting the project initialized and the FastAPI server started. Used ChatGPT to help me out. I was admittedly "up a level" in my terminal window and had my venv stored a level up as well.

Fleshed out the weather and Ollama clients with ChatGPT's help generating and Copilot explaining parts I wasn't 100 on

Found out about JavaScript's Geolocation API for the frontend to send user geolocation data to FastAPI backend
Need to add this frontend logic in my very basic HTML file.

Imported ollama and weather client's copilot renamed my client's to be uniquely named imports in main.py

Enable CORS in FastAPI

Had a .env hiccup. Found out an API key needs to be called using os.getenv() when a python file needs it
Found out about hardcoded parent[] parameters and how the location of your .env will affect the call

Realized I used weather API as my API endpoint and not Open Weather. Kept getting 401 errors when testing the endpoint.

ChatGPT provided new index.jsx file, forgot to commit project before resetting sytem to run WSL

Used ChatGPT and Copilot to create  src/components/WeatherOutfit.jsx, index.css for tailwind

Another git issue, I had my .gitignore file saved as ..gitignore, might need to increase zoom😅

Having another API issue with OpenWeather. Not sure if it's URL endpoint or the API key as I'm getting both 404 and 401 errors when messing with OpenWeather's "One Call" endpoint versions. Not sure why this is happening, since the test commands I ran with my current credentials tested true last time I tried. Consulting with ChatGPT again.

Downloaded Postman for a better visual of API testing.

Used new API key, for some reason the one I had set wasn't working anymore. Tested Austin,TX coordinates and got back full forecast respsonse. 