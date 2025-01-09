#Some classes such as Patient and Note are simpler, so you may want to just test
#your objects for equality (__eq__(self, other)) as well their string representation (__str__(self))

from unittest import TestCase
from unittest import main
from clinic.controller import Controller
from clinic.patient import Patient
from clinic.patient_record import PatientRecord
from clinic.note import Note

class TestPatient(unittest.TestCase):
    def test_patient_creation(self):
        patient = Patient("12345", "John Doe", 20, "123 St")
        self.assertEqual(patient.phn, "12345")
        self.assertEqual(patient.name, "John Doe")
        self.assertEqual(patient.age, "20")
        self.assertEqual(patient.address, "123 St")

