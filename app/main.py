# Run by typing python3 main.py

# **IMPORTANT:** only collaborators on the project where you run
# this can access this web server!

"""
    Bonus points if you want to have internship at AI Camp
    1. How can we save what user built? And if we can save them, like allow them to publish, can we load the saved results back on the home page? 
    2. Can you add a button for each generated item at the frontend to just allow that item to be added to the story that the user is building? 
    3. What other features you'd like to develop to help AI write better with a user? 
    4. How to speed up the model run? Quantize the model? Using a GPU to run the model? 
"""

# import basics
import os
from utils import stringMinus
# import stuff for our web server
from flask import Flask, request, redirect, url_for, render_template, session
from utils import get_base_url
# import stuff for our models
from aitextgen import aitextgen
import nltk as nk
#nk.download('punkt')

# load up a model from memory. Note you may not need all of these options.
ai_cons = aitextgen(model_folder="model_cons_v2", to_gpu = False)
ai_lib = aitextgen(model_folder="liberal_model", to_gpu = False)
#ai = aitextgen(model="distilgpt2", to_gpu=False)

# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
port = 12345
base_url = get_base_url(port)


# if the base url is not empty, then the server is running in development, and we need to specify the static folder so that the static files are served
if base_url == '/':
    app = Flask(__name__)
else:
    app = Flask(__name__, static_url_path=base_url+'static')

app.secret_key = os.urandom(64)

# set up the routes and logic for the webserver
# list of liberal and coservative bot responses
responses = []

@app.route(f'{base_url}')
def home():
    return render_template('writer_home.html', generated=None)


@app.route(f'{base_url}', methods=['POST'])
def home_post():
    return redirect(url_for('results'))


@app.route(f'{base_url}/results/')
def results():
    if 'data' in session:
        data = session['data']
        return render_template('Write-your-story-with-AI.html', generated=data)
    else:
        return render_template('Write-your-story-with-AI.html', generated=None)


def generate_text_lib(prompt):
    
    #prompt = input("Input some text for the liberal bot to respond to")
    if prompt is not None:
        generated = ai_lib.generate(n=1, prompt=str(prompt), max_length=100, temperature=1, return_as_list=True, repetition_penalty = 1.5)
        generated = generated[0]
        generated = nk.sent_tokenize(generated)
        generated = "".join(generated[:2])
#         print("Liberal:" + str(generated))
    #responses.append("Liberal:" + str(generated))
    return generated

def generate_text_cons(prompt):
#     prompt = input("Input some text for the conservartive bot to respond to")
    
    if prompt is not None:
        generated = ai_cons.generate(n=1, prompt=str(prompt), max_length=100, temperature=1, return_as_list=True, repetition_penalty = 1.5)
        generated = generated[0]
        generated = nk.sent_tokenize(generated)
        generated = "".join(generated[:2])
#         print("Conservative:" + str(generated))
    # adds generated response to list
    #responses.append("Conservative:" + str(generated))
    return generated


def conservative_response(input):
    
    
    gen_cons = ai_cons.generate(n=1, prompt=str(input), max_length=100, temperature=1, return_as_list=True, repetition_penalty = 1.5)
        #gen_cons = nk.sent_tokenize(gen_cons[0])
    gen_cons=gen_cons[0]
    gen_cons=gen_cons[len(input):].strip()
    output=gen_cons
        #output = stringMinus(gen_cons[0], input)
    generated_cons = nk.sent_tokenize(output)
    generated_cons = "".join(generated_cons[:2])
#     print("Conservative:" + generated_cons)
   # responses.append("Conservative:" + generated_cons)
    return generated_cons
  # print("Conservative:" + generated[0])

def liberal_response(input):

    gen_lib = ai_lib.generate(n=1, prompt=str(input), max_length=100, temperature=1, return_as_list=True, repetition_penalty = 1.5)
    gen_lib=gen_lib[0]
    gen_lib=gen_lib[len(input):].strip()
    output=gen_lib
 
        #output = stringMinus(gen_lib[0], input)
    generated_lib = nk.sent_tokenize(output)
    generated_lib = "".join(generated_lib[:2])
    #responses.append("Liberal:" + generated_lib)
    return generated_lib



# print("Conservative:" + generated[0])
# define additional routes here
# for example:
# @app.route(f'{base_url}/team_members')
# def team_members():
#     return render_template('team_members.html') # would need to actually make this page



def text_clean (text):
    import random
    string_list=['Hmmm....','Depends.','Let us agree to disagree.','Its all a conspiracy','Interesting....']
    if text.strip()=='':
        return random.choice(string_list)
    else :
        return text.capitalize()

@app.route(f'{base_url}/generate_text/', methods=["POST"])



def generate_text():
    prompt = request.form['prompt']
    opinion= request.form['opinion']
    result=[]
    #responses=""
    if opinion == 'liberal':
        x = generate_text_lib(prompt)
        result.append('<font color="#00AEF3">Liberal : '+text_clean(x)+'</font><br><br>')
        for i in range(2):
            z = conservative_response(x)
            result.append('<font color="#E81B23">Conservative : '+text_clean(z)+'</font><br><br>')
            x = liberal_response(z)
            result.append('<font color="#00AEF3">Liberal : '+text_clean(x)+'</font><br><br>')
    elif opinion == 'conservative':
        z = generate_text_cons(prompt)
        result.append('<font color="#E81B23">Conservative : '+text_clean(z)+'</font><br><br>')
        for i in range(2):
            x = liberal_response(z)
            result.append('<font color="#00AEF3">Liberal : '+text_clean(x)+'</font><br><br>')
            z = conservative_response(x)
            result.append('<font color="#E81B23">Conservative : '+text_clean(z)+'</font><br><br>')
    #reponses = "".join(str(x) for x in responses)
    responses =" ".join(result)
    session['data'] = responses
    return redirect(url_for('results'))
    


if __name__ == '__main__':
    # IMPORTANT: change url to the site where you are editing this file.
    website_url = 'cocalc3.ai-camp.dev'

    print(f'Try to open\n\n    https://{website_url}' + base_url + '\n\n')
    app.run(host='0.0.0.0', port=port, debug=True)
