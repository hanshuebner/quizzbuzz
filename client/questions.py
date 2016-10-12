from random import shuffle
import requests
import json
import raspi

class QuestionsException(BaseException):
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message

class Question:
    def __init__(self, data):
        self.question = data['question']
        self.answers = [data['answer-correct'],
                        data['answer-incorrect-1'],
                        data['answer-incorrect-2'],
                        data['answer-incorrect-3']]
        shuffle(self.answers)
        self.correct_answer = data['answer-correct']
        self.level = data['level']
        self.category = data['category']

class QuestionsServer:
    def get_questions(self, category='Biologie', max_level=10):
        response = requests.post(self.server_url,
                                 headers={'X-Client-ID': raspi.get_serial()})
        if response.status_code != 200:
            raise QuestionsException('Cannot retrieve questions, status %d: %s' % (response.status_code, response.text))
        questions = response.json()
        return list(map(lambda data: Question(data), questions))

    def __init__(self, server_url='http://paracetamol:3399/questions?category=Biologie'):
        self.server_url = server_url
