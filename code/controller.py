import os
import json
from datetime import datetime
from .patient import Patient
from .patient_record import PatientRecord
from .user import User
from .note import Note

# Updated exception imports
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException

#dao stuff
from clinic.dao.patient_dao_json import PatientDAOJSON
from clinic.dao.note_dao_pickle import NoteDAOPickle



class Controller:
    def __init__(self, autosave=False):
        self.autosave = autosave #For checking persistance
        self.logged_in_user = None  # Track the currently logged-in user
        self.current_patient = None  # Tracks the currently selected patient
        self.users = self._load_users_from_file('clinic/users.txt') if autosave else {
            "user": User("user", "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92"),
            "ali": User("ali", "6394ffec21517605c1b426d43e6fa7eb0cff606ded9c2956821c2c36bfee2810"),
            "kala": User("kala", "e5268ad137eec951a48a5e5da52558c7727aaa537c8b308b5e403e6b434e036e"),
        } #These are all necessary users for non autosave testing
        self.patient_dao = PatientDAOJSON(autosave)
        self.note_dao = NoteDAOPickle(autosave)

    def _load_users_from_file(self, file_path):
        #Loads users from the chosen file
        users = {}
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                for line in file:
                    username, password_hash = line.strip().split(',')
                    users[username] = User(username, password_hash)
        return users

    # --- User Management Methods ---
    def add_user(self, username, password):
        #Adds a user to the users array
        if username in self.users:
            raise DuplicateLoginException(f"User '{username}' already exists.")
        self.users[username] = User(username, password)

    def login(self, username, password):
        #Login a user with the corresponding username, if password is correct
        if self.logged_in_user:
            raise DuplicateLoginException("A user is already logged in.")

        if username not in self.users or not self.users[username].check_password(password):
            raise InvalidLoginException("Invalid username or password.")

        self.logged_in_user = self.users[username]
        return True


    def logout(self):
        #Logs out the currently logged in user if there is a currently logged in user, also reset current patient
        if not self.logged_in_user:
            raise InvalidLogoutException("No user is logged in to log out.")

        self.logged_in_user = None
        self.current_patient = None
        return True


    # --- Patient Management Methods ---
    def create_patient(self, phn, name, birth_date, phone, email, address):
        #Creates a new patient with the given information and stores it. Returns the patient
        if not self.logged_in_user:
            raise IllegalAccessException("Must be logged in to create a patient.")

        if self.patient_dao.search_patient(phn):
            raise IllegalOperationException(f"Patient with PHN {phn} already exists.")

        new_patient = Patient(phn, name, birth_date, phone, email, address, autosave=self.autosave)
        self.patient_dao.add_patient(new_patient)
        return new_patient

    def search_patient(self, phn):
        #Finds a patient from the records using phn, returns the patient
        if not self.logged_in_user:
            raise IllegalAccessException("You must be logged in to search for patients.")
        
        patient = self.patient_dao.read_patient(phn)
        if patient:
            #Ensure the patient's record respects the autosave flag
            patient.patient_record.autosave = self.autosave
        return patient

    def retrieve_patients(self, search_string):
        #Finds a patient from the records using the patient's name, returns the patient
        if not self.logged_in_user:
            raise IllegalAccessException("You must be logged in to retrieve patients.")
        return self.patient_dao.retrieve_patients(search_string)


    def choose_current_patient(self, phn):
        #Chooses a current patient for further actions
        if not self.logged_in_user:
            raise IllegalAccessException("You must be logged in to select a patient.")
        patient = self.search_patient(phn)
        if not patient:
            raise NoCurrentPatientException("No patient found with the given PHN.")
        self.current_patient = patient

    def unset_current_patient(self):
        #Unsets the current patient if there is one
        if not self.logged_in_user:
            raise IllegalAccessException("You must be logged in.")
        if not self.current_patient:
            raise NoCurrentPatientException("You must have a patient selected.")
        self.current_patient = None

    def update_patient(self, old_phn, new_phn, name, birth_date, phone, email, address):
        #Updates a patients information with new information
        if not self.logged_in_user:
            raise IllegalAccessException("You must log in first.")
        
        if self.current_patient and self.current_patient.phn == old_phn:
            raise IllegalOperationException("Cannot update the current patient. Please unset the current patient first.")

        patient = self.patient_dao.search_patient(old_phn)
        if not patient:
            raise IllegalOperationException(f"Patient with PHN {old_phn} does not exist.")

        #Check for conflicting PHN if PHN is being changed
        if old_phn != new_phn and self.patient_dao.search_patient(new_phn):
            raise IllegalOperationException(f"PHN {new_phn} is already registered.")

        #Update patient details
        patient.phn = new_phn
        patient.name = name
        patient.birth_date = birth_date
        patient.phone = phone
        patient.email = email
        patient.address = address

        #Save changes
        self.patient_dao.update_patient(old_phn, patient)
        return True



    def delete_patient(self, phn):
        #Deletes a patient from the records
        if not self.logged_in_user:
            raise IllegalAccessException("You must be logged in to delete a patient.")
        if self.current_patient and self.current_patient.phn == phn:
            raise IllegalOperationException("Cannot delete the current patient. Unset the current patient first.")
        self.patient_dao.delete_patient(phn)
        return True


    def list_patients(self):
        #Lists all patients in the records
        if not self.logged_in_user:
            raise IllegalAccessException("You must be logged in to list patients.")
        return self.patient_dao.list_patients()
    
    #Methods for setting and managing the current patient. They may be redundant
    def set_current_patient(self, phn):
        if not self.logged_in_user:
            raise IllegalAccessException("You must be logged in to set a patient.")
        patient = self.search_patient(phn)
        if not patient:
            raise IllegalOperationException("PHN does not exist.")
        self.current_patient = patient

    def get_current_patient(self):
        if not self.logged_in_user:
            raise IllegalAccessException("You must be logged in to get a patient.")
        return self.current_patient

    # --- Note Management Methods ---

    #Creates a note for the current patient.
    def create_note(self, text):
        if not self.logged_in_user:
            raise IllegalAccessException("You must be logged in to create a note.")
        if not self.current_patient:
            raise NoCurrentPatientException("No current patient set.")

        # Create the note through the patient's record
        note = self.current_patient.patient_record.add_note(text)
        
        # Ensure the note DAO is aware of autosave
        self.note_dao.autosave = self.autosave
        return note


    def update_note(self, note_code, new_text):
        #Updates a notes information
        if not self.logged_in_user:
            raise IllegalAccessException("You must be logged in to update a note.")
        if not self.current_patient:
            raise NoCurrentPatientException("No current patient set.")

        try:
            return self.current_patient.patient_record.update_note(note_code, new_text)
        except IllegalOperationException as e:
            return False

    #Deletes a note for the current patient. return: True if the note was successfully deleted, False otherwise
    def delete_note(self, note_id):
        if not self.logged_in_user:
            raise IllegalAccessException("You must be logged in to delete a note.")
        if not self.current_patient:
            raise NoCurrentPatientException("No current patient is selected.")
        # Attempt to delete the note through the patient's record
        return self.current_patient.patient_record.delete_note(note_id)


    #Lists all notes for the current patient.
    def list_notes(self):
        if not self.logged_in_user:
            raise IllegalAccessException("You must be logged in to list notes.")
        if not self.current_patient:
            raise NoCurrentPatientException("No current patient is set.")
        return self.current_patient.patient_record.list_notes()

    def retrieve_notes(self, search_text):
        #Gets and returns notes
        if not self.logged_in_user:
            raise IllegalAccessException("You must be logged in to retrieve notes.")
        if not self.current_patient:
            raise NoCurrentPatientException("No current patient is set.")
        
        notes = self.current_patient.patient_record.retrieve_notes(search_text)
        return notes if notes else []  # Ensure it always returns a list

    
    def search_note(self, note_id):
        #Finds a note withing the records
        if not self.logged_in_user:
            raise IllegalAccessException("You must be logged in to search notes.")
        if not self.current_patient:
            raise NoCurrentPatientException("No current patient is set.")

        return self.current_patient.patient_record.search_notes(note_id)


    def reset_persistence(self):
        #For persistence tests
        # Save the current patient's PHN if set
        current_patient_phn = self.current_patient.phn if self.current_patient else None

        # Reset DAOs
        self.patient_dao = PatientDAOJSON(autosave=self.autosave)
        self.note_dao = NoteDAOPickle(autosave=self.autosave)

        # Clear in-memory data
        self.note_dao.patient_notes.clear()
        self.note_dao.counter = 0

        # Restore current patient if applicable
        if current_patient_phn:
            self.set_current_patient(current_patient_phn)