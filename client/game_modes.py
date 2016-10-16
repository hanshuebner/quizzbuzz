class Relaxed:
    def description(self):
        return ('Entspannt',
                'Es gibt keine Zeitbeschränkung, Punkte für jede richtige Antwort')

    def question_complete(self, players, answered, answer_correct, remaining_time):
        return len(answered) == len(players)

    def score(self, answer_is_correct, remaining_time):
        if answer_is_correct:
            return 250
        else:
            return 0

class Timed:
    def description(self):
        return ('Gegen die Zeit',
                'Je schneller Du antwortest, desto mehr Punkte bekommst Du.  Nach 10 Sekunden ist alles vorbei!')

    def question_complete(self, players, answered, answer_correct, remaining_time):
        return remaining_time == 0 or len(answered) == len(players)

    def score(self, answer_is_correct, remaining_time):
        if answer_is_correct:
            return int(remaining_time / 40)
        else:
            return 0

class OneOnly:
    def description(self):
        return ('Einer kassiert',
                'Wer am schnellsten richtig antwortet, kassiert!')

    def question_complete(self, players, answered, answer_correct, remaining_time):
        return answer_correct or len(answered) == len(players)

    def score(self, answer_is_correct, remaining_time):
        if answer_is_correct:
            return 250
        else:
            return 0

class Final:
    def description(self):
        return ('Finale',
                'Jede richtige Antwort gibt Punkte, jede falsche Antwort Punktabzug!')

    def question_complete(self, players, answered, answer_correct, remaining_time):
        return len(answered) == len(players)

    def score(self, answer_is_correct, remaining_time):
        if answer_is_correct:
            return 250
        else:
            return -250

