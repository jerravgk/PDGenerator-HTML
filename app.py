# Importing the built-in 'os' module which provides a portable way of using operating system dependent functionality like reading or writing to the file system.
import os



# Importing the 'openai' module which is an API wrapper for OpenAI's GPT-3 language model.
import openai
# Importing necessary classes from Flask module.
from flask import Flask, redirect, render_template, request, url_for

# Creating a Flask instance and assigning it to the 'app' variable.
app = Flask(__name__)
# Setting the OpenAI API key from the environment variable 'OPENAI_API_KEY' using the built-in 'os' module.
openai.api_key = os.getenv("OPENAI_API_KEY")

# The decorator specifies that the 'index' function will handle the '/' route with both GET and POST requests.


@app.route("/", methods=("GET", "POST"))
def index():
    # Check if the request is POST request.
    if request.method == "POST":
        # Retrieve the submitted product_name name from the form using the 'request' object.
        product_name = request.form["product_name"]
        characteristics = request.form["characteristics"]
        # Call the OpenAI API and generate a chatbot response using the specified GPT-3 model and prompt.
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                  {"role": "user", "content": f"""As an expert product description writer, create a high-converting description for the following product, addressing:
1. Target audience
2. Product functionality
3. How it works
4. Unique value compared to competitors

Write the description in English and base it on the following:

Product Name: {product_name}
Product Characteristics: {characteristics}

Use emotions, scarcity, and urgency. Follow this layout:


Title: [Title] (one strong sentence highlighting benefits)

Text under title: [Text_under_title] (elaborate on Title, mention benefits and emotions)

Header 1: [Benefit_1]

Text under header 1: [Text_under_header_1] (short, precise explanation)

Header 2: [Benefit_2]

Text under header 2: [Text_under_header_2] (short, precise explanation)

Header 3: [Benefit_3]

Text under header 3: [Text_under_header_3] (short, precise explanation)

Product Page Name Title: [Product_page_name_title] (product name, main benefit)"""}
            ],
            temperature=0.6,
        )
        # Redirect to the same page with the generated response added to the query parameters.
        return redirect(url_for("index", result=response['choices'][0]['message']['content'].replace('\n', '<br>')))

    # Check if there is a 'result' query parameter in the URL, and assign its value to the 'result' variable.
    result = request.args.get("result")
    # Render the 'index.html' template with the 'result' variable passed as an argument.
    return render_template("index.html", result=result)
