from flask import Flask, request
import gensim

app = Flask(__name__)

html_form_with_message = '''
<!DOCTYPE html>
<html>
<head>
<title>Opposite Word App</title>
</head>
<body>
    <h2>Enter A Word</h2>
    <p>A Gensim model will estimate the opposite of that word.</p>
    <form method="post" action="/">
        <label for="text">Word:</label><br>
        <input type="word" name="my_input_value"><br><br>
        <input type="submit" value="My Button">
    </form>
    <p>put_data_here</p>
</body>
</html>
'''

model = gensim.models.Word2Vec.load("./opposite_word_model")

def get_opposite(input):
    reference_pair = ("man", "woman")
    target_word = input
    
    result_vector = model.wv[target_word] - model.wv[reference_pair[0]] + model.wv[reference_pair[1]]
    opposite_words = model.wv.similar_by_vector(result_vector)
    
    return opposite_words[0][0]

@app.route('/', methods=['GET', 'POST'])
def home():
    user_input = ''
    opposite_word = ""
    error = False
    
    calculated_value = 0
    if request.method == 'POST':
        user_input = request.form['my_input_value'].lower()

        try:
            opposite_word = get_opposite(user_input)
        except:
            error = True
    
    if error:
        display_text = "That word is not known to the model, please try again."
    else:
        display_text = "The opposite of " + user_input + " is " + opposite_word

    return html_form_with_message.replace("put_data_here", display_text)

app.run()
