import json  # Importing the JSON library for handling JSON data
import os  # Importing the OS library for file operations
from clinic.patient import Patient  # Importing the Patient class for handling patient objects
from clinic.dao.patient_encoder import PatientEncoder  # Importing a custom JSON encoder for Patient objects
from clinic.dao.patient_decoder import patient_decoder  # Importing a custom JSON decoder for Patient objects
from clinic.exception.illegal_operation_exception import IllegalOperationException  # Importing custom exception

class PatientDAOJSON:
    def __init__(self, autosave=False):
        # Initialize the PatientDAOJSON with optional autosave functionality
        self.patients = {}  # Dictionary to store patients, keyed by their PHN
        self.autosave = autosave  # Flag to enable automatic saving of patients to a JSON file

        # Automatically load patients from the file if autosave is enabled
        if self.autosave:
            self.load_patients()

    def save_patients(self):
        # Save the current patients dictionary to a JSON file
        # The custom PatientEncoder ensures that Patient objects are correctly serialized
        with open('clinic/patients.json', 'w') as f:
            json.dump(list(self.patients.values()), f, cls=PatientEncoder)

    def load_patients(self):
        # Load patients from a JSON file and populate the patients dictionary
        if os.path.exists('clinic/patients.json'):  # Check if the file exists
            with open('clinic/patients.json', 'r') as f:
                # Deserialize the file content into Patient objects using the custom decoder
                patients_list = json.load(f, object_hook=patient_decoder)
                # Rebuild the dictionary with PHNs as keys
                self.patients = {patient.phn: patient for patient in patients_list}

    def add_patient(self, patient):
        # Add a new patient to the dictionary
        # Raise an error if the patient with the given PHN already exists
        if patient.phn in self.patients:
            raise ValueError(f"Patient with PHN {patient.phn} already exists.")
        self.patients[patient.phn] = patient  # Add the patient to the dictionary

        # Save the patients to the file if autosave is enabled
        if self.autosave:
            self.save_patients()

    def search_patient(self, phn):
        # Search for a patient by their PHN and return the corresponding Patient object or None
        return self.patients.get(phn)

    def read_patient(self, phn):
        # Retrieve a patient by PHN; similar to search_patient
        return self.patients.get(phn)

    def retrieve_patients(self, search_string):
        # Retrieve patients whose attributes match the given search string
        # Convert the search string to lowercase for case-insensitive comparison
        search_string = search_string.lower()
        # Return a list of patients whose name, email, or address contains the search string
        return [
            patient for patient in self.patients.values()
            if search_string in patient.name.lower() or
               search_string in patient.email.lower() or
               search_string in patient.address.lower()
        ]

    def update_patient(self, old_phn, updated_patient):
        # Update an existing patient's information
        # Raise an error if the patient with the old PHN does not exist
        if old_phn not in self.patients:
            raise ValueError(f"Patient with PHN {old_phn} does not exist.")

        # If the PHN is being changed, remove the old entry
        if old_phn != updated_patient.phn:
            del self.patients[old_phn]

        # Add or update the patient with the new PHN
        self.patients[updated_patient.phn] = updated_patient

        # Save the updated patients to the file if autosave is enabled
        if self.autosave:
            self.save_patients()

    def delete_patient(self, phn):
        # Delete a patient by their PHN
        # Raise an error if the patient does not exist
        if phn not in self.patients:
            raise IllegalOperationException(f"Patient with PHN {phn} does not exist.")
        del self.patients[phn]  # Remove the patient from the dictionary

        # Save the updated patients to the file if autosave is enabled
        if self.autosave:
            self.save_patients()

    def list_patients(self):
        # Return a list of all Patient objects in the dictionary
        return list(self.patients.values())
