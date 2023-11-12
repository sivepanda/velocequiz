# testbank-generation


## Running For the First Time
To run the bot, you need to use two different terminal instances. **If you are running this for the first time** follow these steps:
1. If you have not already, install [NodeJS](https://nodejs.org/en). This is the runtime that Svelte runs with.
2. Run `npm install`. This should install nescessary JS dependencies. 
3. For our API, we use [Flask](https://flask.palletsprojects.com/en/2.3.x/), you need to install the `flask`, `flask_cors`, `dotenv`, `os`, `pdfplumber`, `logging` and <*other libraries go here*> libraries using `pip install <library name>`.
4. To run, use one terminal instance to run `npm run dev`.
5. With the other terminal instance, run the `server.py` file. 
6. Everything should be working!

## Running
1. To run the frontend, use one terminal instance and cd into `/frontend` 
2. Run `npm run dev`.
3. With the other terminal instance, run the `server.py` file. 

# Technologies
This projects uses the following technologies:
- [Svelte](https://svelte.dev/), a framework whose syntax is extremely similar to standard HTML, CSS, and JS, but enables usage of things like components, which I used to create messages.
- [Flask](https://flask.palletsprojects.com/en/2.3.x/) hosts our API and does the heavy lifting in terms of AI.