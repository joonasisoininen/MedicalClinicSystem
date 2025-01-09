from datetime import datetime

class Note:
    def __init__(self, id=None, text=" ",timestamp=None):
        self.id = id # Unique ID for the note, not supposed to be phn
        self.text = text # Content of the note

        #Timestamp not really necessary anymore
        self.timestamp = timestamp or datetime.now() #The time when the note was created or last modified (default is now)

    #Convert to string for testing
    def __str__(self):
        return f"Note[id={self.id}, Text={self.text}, Timestamp={self.timestamp}]"

    #Compares two Note objects for equality based on their code and text.
    def __eq__(self, other):
        if not isinstance(other, Note):
            return False
        return self.id == other.id and self.text == other.text

    #String representation of the Note for debugging purposes.
    def __repr__(self):
        return f"Note(id={self.id}, text={self.text})"
