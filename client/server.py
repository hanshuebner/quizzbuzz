from random import shuffle
import requests
import json
import raspi

class ServerException(BaseException):
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

class Server:
    def headers(self):
        return {'X-Client-ID': raspi.get_serial()}

    def questions(self, category='Biologie', max_level=10, question_count=10):
        response = requests.post(self.server_url + 'questions',
                                 headers=self.headers(),
                                 params={'category': category,
                                         'max-level': max_level,
                                         'question-count': question_count})
        if response.status_code != 200:
            raise ServerException('Cannot retrieve questions, status %d: %s' % (response.status_code, response.text))
        questions = response.json()
        return list(map(lambda data: Question(data), questions))

    def categories(self, max_level=10, question_count=10):
        response = requests.get(self.server_url + 'categories',
                                headers=self.headers(),
                                params={'max-level': max_level,
                                        'question-count': question_count})
        if response.status_code != 200:
            raise ServerException('Cannot retrieve categories, status %d: %s' % (response.status_code, response.text))
        return response.json()

    def players(self):
        response = requests.get(self.server_url + 'players',
                                headers=self.headers())

    def __init__(self, server_url='http://localhost:3399/'):
        self.server_url = server_url
