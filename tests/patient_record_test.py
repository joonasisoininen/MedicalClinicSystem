import unittest
from clinic.patient_record import PatientRecord

class TestPatientRecord(unittest.TestCase):
    def test_add_note(self):
        record = PatientRecord()()
        note = record.add_note("Patient's first note")
        self.assertEqual(note.code, 1)
        self.assertIn(note, record.notes)



