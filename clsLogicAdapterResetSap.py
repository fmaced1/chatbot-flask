from chatterbot.logic import LogicAdapter

class LogicAdapterResetSap(LogicAdapter):
    def __init__(self, **kwargs):
        super(LogicAdapterResetSap, self).__init__(**kwargs)

    def can_process(self, statement):
        words = ["reset", "bloqueou", "senha", "resetar", "sap"]
        if any(word in statement.text.lower().split() for word in words):
            return True
        else:
            return False

    def process(self, statement):
        import random

        # Randomly select a confidence between 0 and 1
        confidence = random.uniform(0, 1)

        # For this example, we will just return the input as output
        selected_statement = statement
        selected_statement.confidence = confidence

        return selected_statement
