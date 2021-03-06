
<div align='center'>
  <h1>Crypto Cap </h1>
  <img width="1772" alt="CryotoCap" src="https://user-images.githubusercontent.com/25966709/132071951-a715f692-34f5-4822-a4f6-12da13892620.png">
</div>

<div align="center">

**[PROJECT PHILOSOPHY](https://github.com/Alex-Reitz/Crypto-Cap#-project-philosophy) • 
[TECH STACK](https://github.com/Alex-Reitz/Crypto-Cap#-tech-stack)**
</div>

<br />

# 🧐 Project philosophy

- Crypto Cap is an app where users can signup or login and view data on hundreds of cryptocurrencies listed on the coin market cap API. 

- Once a user sign's up or logs in, the home page is displayed. When the home page loads it send an API request to the Coin Market Cap API, and displays the response. Users can then interact with the data, displayed in table format, by clicking on the Cryptocurrency's name. This takes a user to a separate page with a more detailed set of information about that specific crypto. Users can also add favorites by clicking on a star icon displayed in the table. 


# 👨‍💻 Tech stack

Here's a brief high-level overview of the tech stack the app uses:

- This project uses the [Flask Framework](https://flask.palletsprojects.com/en/2.0.x/). Flask is a Python web framework that lets you develop web applications easily. It has a small and easy-to-extend core which for this project was extended using the ORM SQL-Alchemy.
- For persistent storage (database), the app uses [PostgreSQL](https://www.postgresql.org/) which allows the app to create a custom storage schema and save it to a local database.
- For the front end the app uses jinga templates which inherit from a single base template. Additionally the project uses twitter bootstrap for dynamic rendering of data.
<br />

---

<br />



