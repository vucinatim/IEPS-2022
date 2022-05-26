class Posting:
    def __init__(self, file, word, indexes):
        self.path = file
        self.document_name = file.split("/")[-1].replace("\\", "/")
        self.word = word
        self.frequency = len(indexes)
        self.indexes = indexes
        self.indexes_str = ",".join(map(str, indexes))

    def __str__(self):
        p1 = f"Word: {self.word} \n"
        p2 = f"Document: {self.document_name} \n"
        p3 = f"Frequency: {self.frequency} \n"
        p4 = f"Indexes: {self.indexes_str}"
        return p1 + p2 + p3 + p4

    def to_tuple(self):
        return (self.word, self.document_name, self.frequency, self.indexes_str)