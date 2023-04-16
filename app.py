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
                  {"role": "user", "content": f"""Act as an expert product description writer, you are known for writing the highest converting product descriptions in the world. You use emotions, scarcity and urgency. You also comply to always incorporate the answers on these questions in your description:
Who is it for?
What does the product do?
How does it work?
What is the unique value of the product when compared to competitors in your niche?

You are known for always writing in the following layout:

Title (one strong sentence that converts using emotions and shows the good benefits of the product)

Text under title (Elaborate on the Title and go deeper, be precise, name all the relevant benefits which convert using emotion and which feeling it will give you or others.)

Header 1 (Here you state the first benefit)

Text under header 1 (Explain benefit, in detail, short but precise.)

Header 2 (Here you state the second benefit)

Text under header 2 (Explain benefit, in detail, short but precise.)

Header 3 (Here you state the third benefit)

Text under header 3 (Explain benefit, in detail, short but precise.)

And you also give the product page name title, this is the product name, followed by a - and then the main benefit in a few words.

                   Please write in English language.
                   Write a description for the following product:
                   The product name is: {product_name}
                   The product characteristics are: {characteristics}"""}
            ],
            temperature=0.6,
        )
        # Redirect to the same page with the generated response added to the query parameters.
        return redirect(url_for("index", result=response['choices'][0]['message']['content'].replace('\n', '<br>')))

    # Check if there is a 'result' query parameter in the URL, and assign its value to the 'result' variable.
    result = request.args.get("result")
    # Render the 'index.html' template with the 'result' variable passed as an argument.
    return render_template("index.html", result=result)
