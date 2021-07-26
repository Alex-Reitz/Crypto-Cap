
# Crypto Cap

This project allows users to monitor metrics for the top 200 most popular cryptocurrencies.

Users can
  - Signup or Login
  - View the top 200 cryptocurrencies by market cap
  - Click on a crypto to view more detailed information
  - Add a cryptocurrency to their favorites and view their favorites in a separate tab


The tech stack for this project is Python, Flask, PostgreSQL, SQL-Alchemy, Bootstrap, Jinga Templates, and HTML.

Once a user sign's up or logs in, the home page is displayed. When the home page loads it send an API request to the Coin Market Cap API, and displays the response.
Users can then interact with the data, displayed in table format, by clicking on the Cryptocurrency's name. This takes a user to a separate page with a more detailed set of information about that specific crypto. Users can also add favorites by clicking on a star icon displayed in the table. A separate tab is linked in the navbar for viewing favorites.
