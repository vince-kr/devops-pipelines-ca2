# Speak To Data

*your personal homesteading assistant*

## Minimum viable product

This project verifies that the basic principles of the application are viable.
To that end, it will contain:

- Sample data representing typical events recorded over a year of keeping a
  homestead
- A simple Flask app that defines a single route, supporting GET and POST
- An index page which contains:
    - An input field for the user's query
    - Space underneath the input field for the response from TaPas

The application should:

- Accept queries from the user
- Call the deployed TaPas model on HuggingFace with the query + sample data
- Present the response to the user

For now the page will not involve any JavaScript. The page will simply use a
POST request as a signal to query the TaPas API, and call its own GET routine
after a response from TaPas is received, reloading the page in the user's
browser.
