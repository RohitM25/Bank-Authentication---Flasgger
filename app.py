import flask
from flask import Flask,render_template,request,url_for
import pickle
import pandas as pd
import flasgger
from flasgger import Swagger


model = pickle.load(open("bank_auth.pkl","rb"))

app = Flask('__name__')
Swagger(app)



@app.route("/")
def home():
    return "Welcome"


@app.route("/predict_note_auth", methods = ['GET'])  # Using GET Method
def predict_note_auth():
    variance = request.args.get("variance")
    skewness = request.args.get("skewness")
    kurtosis = request.args.get("kurtosis")
    entropy = request.args.get("entropy")
    predictions = model.predict([[variance,skewness,kurtosis,entropy]])
    return "The predicted class is" + str(predictions)


@app.route("/predict_file", methods=["POST", "GET"])  # Taking observation from a file
def predict_file():
    df_test = pd.read_csv(request.files.get("file"))
    predictions = model.predict(df_test)
    return "The predicted class is" + str(predictions)

# Lets use flasgger for creating the API


@app.route("/predict_note_auth_flasgger", methods=['GET'])  # Using GET Method
def predict_note_auth_flasgger():

    """ Lets Authenticate the bank note
    This is using docstrings for specification
    ---
    parameters:
      - name: variance
        in: query
        type: number
        required: true
      - name: skewness
        in: query
        type: number
        required: true
      - name: kurtosis
        in: query
        type: number
        required: true
      - name: entropy
        in: query
        type: number
        required: true
        
    responses:
        200:
            description: The output values

    """
    variance = request.args.get("variance")
    skewness = request.args.get("skewness")
    kurtosis = request.args.get("kurtosis")
    entropy = request.args.get("entropy")
    predictions = model.predict([[variance, skewness, kurtosis, entropy]])
    return "The predicted class is" + str(predictions)


@app.route("/predict_file_flasgger", methods=["POST"])  # Taking observation from a file
def predict_file_flasgger():
    """Lets authenticate the bank note
    ---
    parameters:
        - name: file
          in: formData
          type: file
          required: true
    responses:
        200:
            description: The output values
    """
    df_test = pd.read_csv(request.files.get("file"))
    predictions = model.predict(df_test)
    return str(list(predictions))


if __name__ == '__main__':
    app.run(debug=True)
