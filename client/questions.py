from random import shuffle
import requests
import json
import raspi

class Question:
    def get_question(self):
        response = requests.post(self.server_url, headers={'X-Client-ID': raspi.get_serial()})
        return response.json()

    def __init__(self, server_url='http://paracetamol:3399/questions?category=Biologie'):
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
