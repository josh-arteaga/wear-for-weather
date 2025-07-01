# Wear for Weather
This is a standard Weather API application that also leverages a local LLM(Ollama) to generate a "What to wear" recommendation for the user

Vite + React
Deep Seek Generated Dark-mode palette in styles.css
I am using ChatGPT to structure the development phases of this plan. 

Had an issue getting the project initialized and the FastAPI server started. Used ChatGPT to help me out. I was admittedly "up a level" in my terminal window and had my venv stored a level up as well.

Fleshed out the weather and Ollama clients with ChatGPT's help generating and Copilot explaining parts I wasn't 100 on

Found out about JavaScript's Geolocation API for the frontend to send user geolocation data to FastAPI backend
Need to add this frontend logic in my index

Imported ollama and weather client's copilot renamed my client's to be uniquely named imports in main.py

Enable CORS in FastAPI

Had a .env hiccup. Found out an API key needs to be called using os.getenv() when a python file needs it
Found out about hardcoded parent[] parameters and how the location of your .env will affect the call

Realized I used weather API as my API endpoint and not Open Weather. Kept getting 401 errors when testing the endpoint.

The version control issues i had set me back, getting everything reconfigured.

Had ChatGPT help redo the package.json file

Having issues with getting front end properly configured with vite

Working geolocation in the frontend, trying to find out why LLM call isn't fully going through with dev console in browser and ChatGPT explaining. 

Removed geolocation from browser view into console log
