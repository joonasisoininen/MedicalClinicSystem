#Some classes such as Patient and Note are simpler, so you may want to just test
#your objects for equality (__eq__(self, other)) as well their string representation (__str__(self))

from unittest import TestCase
from unittest import main
from clinic.controller import Controller
from clinic.patient import Patient
from clinic.patient_record import PatientRecord
from clinic.note import Note

#__eq__(self, other):

#__str__(self);

class TestNote(unittest.TestCase):
    def test_note_creation(self):
        note = Note(1, "Test note")
        self.assertEqual(note.code, 1)
        self.assertEqual(note.details, "Test note")

