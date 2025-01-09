import pickle
import os
from .note_dao import NoteDAO
from ..note import Note
from clinic.exception.illegal_operation_exception import IllegalOperationException


class NoteDAOPickle:
    def __init__(self, patient_phn=None, autosave=False):
        # Initialize the NoteDAO with optional autosave and a specific patient PHN
        self.patient_notes = {}  # Dictionary to hold notes for each patient, keyed by PHN
        self.counter = 0  # Counter for generating unique note IDs
        self.patient_phn = patient_phn  # The PHN of the patient associated with this DAO
        self.autosave = autosave  # Flag to indicate if changes should be saved automatically

        # Load notes from file if autosave is enabled and a PHN is provided
        if autosave and patient_phn:
            self.load_notes()

    def create_note(self, note, patient_phn):
        # Add a new note for a specific patient
        if patient_phn not in self.patient_notes:
            self.patient_notes[patient_phn] = []  # Initialize the list if the patient has no notes
        self.counter += 1
        note.id = self.counter  # Assign a unique ID to the note
        self.patient_notes[patient_phn].append(note)

        # Save the updated notes to a file if autosave is enabled
        if self.autosave:
            self.save_notes(patient_phn)

    def read_notes(self, patient_phn):
        # Retrieve all notes for a specific patient
        return self.patient_notes.get(patient_phn, [])

    def update_note(self, patient_phn, note_id, new_text):
        # Update the text of a specific note for the given patient PHN
        note = self.find_note_by_id(patient_phn, note_id)
        if not note:
            raise IllegalOperationException(f"Note with ID {note_id} not found for patient {patient_phn}.")
        
        note.text = new_text  # Update the note text
        if self.autosave:
            self.save_notes(patient_phn)  # Save the updated notes to a file
        return True

    def delete_note(self, patient_phn, note_id):
        # Delete a note for a specific patient
        if patient_phn not in self.patient_notes or not self.patient_notes[patient_phn]:
            raise IllegalOperationException(f"No notes found for patient {patient_phn}.")

        # Search for the note and delete it if found
        for note in self.patient_notes[patient_phn]:
            if note.id == note_id:
                self.patient_notes[patient_phn].remove(note)
                if self.autosave:
                    self.save_notes(patient_phn)  # Save changes after deletion
                return True

        raise IllegalOperationException(f"Note with ID {note_id} not found for patient {patient_phn}.")

    def find_note_by_id(self, patient_phn, note_id):
        # Find a specific note by its ID for the given patient PHN
        for note in self.patient_notes.get(patient_phn, []):
            if note.id == note_id:
                return note
        return None

    def search_note(self, patient_phn, search_text):
        # Search for notes containing the specified text for a given patient PHN
        return [
            note for note in self.patient_notes.get(patient_phn, [])
            if search_text.lower() in note.text.lower()
        ]

    def list_notes(self, patient_phn):
        # List all notes for a specific patient PHN
        return self.read_notes(patient_phn)

    def retrieve_notes(self, patient_phn):
        # Retrieve all notes for a specific patient PHN
        return self.read_notes(patient_phn)

    def save_notes(self, patient_phn):
        # Save the notes for a specific patient to a file
        file_path = self.get_file_path(patient_phn)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure the directory exists
        try:
            with open(file_path, 'wb') as f:
                pickle.dump(self.patient_notes.get(patient_phn, []), f)
        except Exception as e:
            raise IOError(f"Failed to save notes for patient {patient_phn}: {e}")

    def load_notes(self):
        # Load notes from a file for the current patient
        if not self.patient_phn:
            return

        file_path = self.get_file_path(self.patient_phn)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as f:
                    self.patient_notes[self.patient_phn] = pickle.load(f)
            except Exception as e:
                raise IOError(f"Failed to load notes for patient {self.patient_phn}: {e}")
        else:
            self.patient_notes[self.patient_phn] = []

        # Update the counter to reflect the highest existing note ID
        self.counter = max((note.id for note in self.patient_notes[self.patient_phn]), default=0)

    def get_file_path(self, patient_phn):
        # Get the file path for a specific patient's notes
        return f'clinic/records/{patient_phn}.dat'
