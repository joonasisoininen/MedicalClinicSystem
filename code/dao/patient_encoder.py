#Some students are having trouble with phn being encoded as a JSON because of the conflict between numbers and strings.

#This is an extract of a JSON file using a solution that I coded. The data are mere examples that are different from the tests, but they illustrate the idea.

#{"__type__": "Patient", "phn": 4561230000, "name": "Mark Smith", "birth_date": "1980-12-01", "phone": "234 456 7689", "email": "mark@gmail.com", "address": "150 Quadra St, Victoria BC"}
#{"__type__": "Patient", "phn": 4564560000, "name": "Julia Smith", "birth_date": "1995-01-01", "phone": "250 345 6789", "email": "julia@gmail.com", "address": "300 Foul Bay Rd, Oak Bay, BC"}
#If you look at the "phn" key and value, you will see that the key is a string ("phn" is valid for a JSON key) and the value is a number (4561230000 is valid for a JSON value). 
#Do not convert the phn value into a string in the encoding, because that will lead to a problem when you reconstruct the patient (because phn values should be numbers, not strings).



#In the PatientEncoder, use: "phn": obj.phn

#PatientEncoder (inheriting from json.JSONEncoder)

#import from json.JSONEncoder

import json
from clinic.patient import Patient

class PatientEncoder(json.JSONEncoder):
    def default(self, obj):
        # Check if the object is an instance of the Patient class
        if isinstance(obj, Patient):
            # Return a dictionary representation of the Patient object
            return {
                "__type__": "Patient",
                "phn": obj.phn,
                "name": obj.name,
                "birth_date": obj.birth_date,
                "phone": obj.phone,
                "email": obj.email,
                "address": obj.address,
                "autosave": obj.autosave,  # Add autosave to encoder
            }
        # If the object is not a Patient, use the default JSON encoding
        return super().default(obj)

# The PatientEncoder ensures that Patient objects are serialized into a JSON format
# that retains all their attributes, including PHN as a number, and provides compatibility
# for decoding these objects back into Python objects later.