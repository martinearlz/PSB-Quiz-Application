from gui import QuestionPage
from pathlib import Path
import pytest
import sys
# Ensures that we can import stuff from the root folder.
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)
import logic

def test_mark_correct_answer():
    '''
    Gherkin Test Format:
    * Scenario: Answering Questions Correctly
    * Given: I am currently attempting a quiz.
    * When: I click the correct answer for a specific question.
    * And: My previous number of correct answers is 0.
    * Then: The number of correct answers that I have should be 1.
    '''
    quiz = logic.Quiz()
    # Answers question 1 with the first option.
    quiz.mark_answer(1, 0)
    # Assert that the amount of correct answers is only 1.
    assert quiz.get_correct_answers() == 1


def test_mark_wrong_answer():
    '''
    Gherkin Test Format:
    * Scenario: Answering Questions Wrongly
    * Given: I am currently attempting a quiz.
    * When: I click the wrong answer for a specific question.
    * And: My previous number of correct answers is 0.
    * Then: The number of correct answers that I have should still be 0.
    * But: It should not be any other number than 0.
    '''
    quiz = logic.Quiz()
    # Answers question 1 with the second option.
    quiz.mark_answer(2, 0)
    # Assert that the amount of correct answers is 0.
    assert quiz.get_correct_answers() == 0


def test_get_all_correct_results():
    '''
    Gherkin Test Format:
    * Scenario: Answering All Questions Correctly
    * Given: I am currently attempting a quiz.
    * When: I click on the correct answers for all of the questions displayed.
    * And: My previous score is 0, my wrong answers 0, and number of correct answers is 0.
    * Then: The number of correct answers that I have should be 10, the number of wrong answers 0, and the score 100.
    '''
    quiz = logic.Quiz()
    # Answer all questions with correct answers.
    quiz.mark_answer(1, 0)
    quiz.mark_answer(1, 1)
    quiz.mark_answer(2, 2)
    quiz.mark_answer(4, 3)
    quiz.mark_answer(2, 4)
    quiz.mark_answer(1, 5)
    quiz.mark_answer(1, 6)
    quiz.mark_answer(1, 7)
    quiz.mark_answer(3, 8)
    quiz.mark_answer(2, 9)
    correct, wrong, score = quiz.get_results()
    # Assert that the amount of correct answers is 10, wrong is 0, score = 100
    assert correct == 10
    assert wrong == 0
    assert score == 100


def test_get_all_wrong_results():
    '''
    Gherkin Test Format:
    * Scenario: Answering All Questions Wrongly
    * Given: I am currently attempting a quiz.
    * When: I click on the wrong answers for all of the questions displayed.
    * And: My previous score is 0, my wrong answers 0, and number of correct answers is 0.
    * Then: The number of correct answers that I have should still be 0, the number of wrong answers 10, and the score 0.
    '''
    quiz = logic.Quiz()
    # Answer all questions with incorrect answers.
    quiz.mark_answer(4, 0)
    quiz.mark_answer(4, 1)
    quiz.mark_answer(4, 2)
    quiz.mark_answer(1, 3)
    quiz.mark_answer(4, 4)
    quiz.mark_answer(4, 5)
    quiz.mark_answer(4, 6)
    quiz.mark_answer(4, 7)
    quiz.mark_answer(4, 8)
    quiz.mark_answer(4, 9)
    correct, wrong, score = quiz.get_results()
    # Assert that the amount of correct answers is 10, wrong is 0, score = 100
    assert correct == 0
    assert wrong == 10
    assert score == 0

    
def test_is_end_of_quiz():
    '''
    Gherkin Test Format:
    * Scenario: It's the end of the quiz
    * Given: I am currently at the end of the quiz.
    * When: It is the last question 
    * And: I have clicked next question.
    * Then: the result pop up will show.
    '''
    quiz = logic.Quiz() 
    assert quiz. is_end_of_quiz(q_no=10)
def test_get_current_question():
    '''
    Gherkin Test Format:
    * Scenario: Returns the current question text for the given question number.
    * Given:I am currently attempting a quiz.
    * When: My current question is number 1
    * And: My current question is number 1
    * Then: Tt should show question number 1
    '''
    quiz = logic.Quiz()
    question: "Q1. What is technology will be used for project?"
    assert quiz.get_current_question(q_no=0) == question