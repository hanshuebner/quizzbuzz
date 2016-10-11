from random import shuffle
from urllib.request import urlopen
from urllib.parse import urlencode
import json

class Question:
    def get_question(self):
        nothing = urlencode('').encode('utf-8')
        s = urlopen(self.server_url, data=nothing).read().decode('utf-8')
        return json.loads(s)

    def __init__(self, server_url='http://paracetamol:3399/question'):
        self.server_url = server_url
        data = self.get_question()
        self.question = data['question']
        self.answers = [data['answer-correct'],
                        data['answer-incorrect-1'],
                        data['answer-incorrect-2'],
                        data['answer-incorrect-3']]
        shuffle(self.answers)
        self.correct_answer = data['answer-correct']
        self.level = data['level']
        self.category = data['category']
