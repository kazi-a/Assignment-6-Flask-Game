from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Define the trivia questions
questions = [
    {
        'question': 'What is the capital of France?',
        'choices': ['London', 'Paris', 'Berlin', 'Madrid'],
        'correct_answer': 'Paris'
    },
    {
        'question': 'Who wrote "Romeo and Juliet"?',
        'choices': ['William Shakespeare', 'Jane Austen', 'Charles Dickens', 'Mark Twain'],
        'correct_answer': 'William Shakespeare'
    },
    {
        'question': 'What is the largest mammal in the world?',
        'choices': ['Elephant', 'Blue Whale', 'Giraffe', 'Hippopotamus'],
        'correct_answer': 'Blue Whale'
    },
    {
        'question': 'What is the currency of Japan?',
        'choices': ['Dollar', 'Euro', 'Yen', 'Pound'],
        'correct_answer': 'Yen'
    },
    {
        'question': 'Who is the author of "To Kill a Mockingbird"?',
        'choices': ['Harper Lee', 'Ernest Hemingway', 'F. Scott Fitzgerald', 'John Steinbeck'],
        'correct_answer': 'Harper Lee'
    }
]

@app.route('/')
def index():
    # Clear session data and initialize quiz
    session.clear()
    session['questions'] = questions.copy()
    random.shuffle(session['questions'])
    session['score'] = 0
    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    # Redirect to index if no questions or session data
    if 'questions' not in session or len(session['questions']) == 0:
        return redirect(url_for('index'))

    if request.method == 'POST':
        selected_answer = request.form.get('choice')
        if not selected_answer:
            # Render quiz with error message if no answer selected
            return render_template('quiz.html', question=session['questions'][0], error="Please select an answer.")

        # Check if selected answer is correct and update score
        correct_answer = session['questions'][0]['correct_answer']
        if selected_answer == correct_answer:
            session['score'] += 1

        # Remove current question from list and redirect to result if no more questions
        session['questions'].pop(0)
        if len(session['questions']) == 0:
            return redirect(url_for('result'))

    # Render the quiz with current question
    current_question = session['questions'][0]
    return render_template('quiz.html', question=current_question)

@app.route('/result')
def result():
    # Redirect to index if score not in session (e.g., direct access)
    if 'score' not in session:
        return redirect(url_for('index'))

    # Get final score and clear session
    final_score = session['score']
    session.clear()
    return render_template('result.html', score=final_score)

if __name__ == '__main__':
    app.run(debug=True)
