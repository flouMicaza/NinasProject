class Test():

    def __init__(self, input, output, comment, type):
        self.input = input
        self.output = output
        self.comment = comment
        self.type = type

    def get_comment(self):
        return self.comment

    def get_type(self):
        return self.type