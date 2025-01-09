from .note import Note  # Assuming 'note.py' is in the same package as 'patient_record.py'
from clinic.dao.note_dao_pickle import NoteDAOPickle  # Assuming 'note_dao_pickle.py' is in the same package
from clinic.exception.illegal_operation_exception import IllegalOperationException

class PatientRecord:
    def __init__(self, patient_phn, autosave=False):
        self.patient_phn = patient_phn
        self.note_dao = NoteDAOPickle(patient_phn, autosave)

    #Adds a new note for the patient. takes in content of the note, returns the created note object
    def add_note(self, text):
        new_note = Note(None, text)# Note ID will be assigned by DAO
        self.note_dao.create_note(new_note, self.patient_phn)
        return new_note

    #Retrieves all notes for the patient. returns a list of note objects
    def list_notes(self):
        return list(reversed(self.note_dao.read_notes(self.patient_phn)))

    #retrieves notes containing the specified search text, returns a list of note objects mathcing
    def retrieve_notes(self, search_text):
        return self.note_dao.search_note(self.patient_phn, search_text)

    # updates the text of a note, take id of note and new text, returns true is successful update
    def update_note(self, note_id, new_text):
        return self.note_dao.update_note(self.patient_phn, note_id, new_text)

    #Deletes a note by its ID. returns true if successful deletion
    def delete_note(self, note_id):
        try:
            self.note_dao.delete_note(self.patient_phn, note_id)
            return True
        except IllegalOperationException:
            return False

    #Searches the patient's notes for a id,
    def search_notes(self, note_id):
        return self.note_dao.find_note_by_id(self.patient_phn, note_id)