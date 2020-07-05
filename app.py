from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)



#responses = []

@app.route("/")
def show_survey():
    """Shows the user the title of the survey, the instructions, and a button to start the survey.
    """
    return render_template("survey.html", survey=survey)


@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear session of responses
    """
    session[RESPONSES_KEY] = []
    
    return redirect("/questions/0")



@app.route("/questions/<int:qid>")
def show_question(qid):
    """Display current question

    Args:
        qid ([int]): [question number]
    """
    responses = session.get(RESPONSES_KEY)
    
    
    
    if (responses is None):
        #trying to access question page too soon
        return redirect("/")
    
    if (len(responses) == len(survey.questions)):
        # scenario where the user has answered all of the questions
        return redirect("/complete")
    
    if (len(responses) != qid):
        # if user accesses questions out of order. 
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")
    
    question = survey.questions[qid]
    return render_template("question.html", question_id=qid, question=question)

@app.route("/answer", methods=['POST'])
def handle_response():
    """Save the response and redirect to the next question

    Returns:
        redirects to next question page/route
    """
    
    
    #get the answer to the question and save it to variable choice
    choice = request.form['answer']
    
    #add this response to the session
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses
    
    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    
    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/complete")
def complete():
    """Survey completed
    """
    return render_template("completion.html")