#Some students are having trouble with phn being encoded as a JSON because of the conflict between numbers and strings.

#This is an extract of a JSON file using a solution that I coded. The data are mere examples that are different from the tests, but they illustrate the idea.

#{"__type__": "Patient", "phn": 4561230000, "name": "Mark Smith", "birth_date": "1980-12-01", "phone": "234 456 7689", "email": "mark@gmail.com", "address": "150 Quadra St, Victoria BC"}
#{"__type__": "Patient", "phn": 4564560000, "name": "Julia Smith", "birth_date": "1995-01-01", "phone": "250 345 6789", "email": "julia@gmail.com", "address": "300 Foul Bay Rd, Oak Bay, BC"}
#If you look at the "phn" key and value, you will see that the key is a string ("phn" is valid for a JSON key) and the value is a number (4561230000 is valid for a JSON value). 
#Do not convert the phn value into a string in the encoding, because that will lead to a problem when you reconstruct the patient (because phn values should be numbers, not strings).


#In the PatientDecoder, use: dct["phn"]

#When recreating the patient from the Decoder, add a final parameter (which will be autosave) with value True;

#PatientDecoder (inheriting from json.JSONDecoder)



#custom decoder used for reconstructing Patient objects from JSON
#interprets the JSON object and creates a Patient instance if the "__type__" key matches "Patient".


import json
from clinic.patient import Patient

def patient_decoder(dct):
    # Check if the dictionary represents a Patient object
    if "__type__" in dct and dct["__type__"] == "Patient":
        # Return a Patient object with attributes extracted from the dictionary
        return Patient(
            phn=dct["phn"],
            name=dct["name"],
            birth_date=dct["birth_date"],
            phone=dct["phone"],
            email=dct["email"],
            address=dct["address"],
            autosave=dct.get("autosave", True),  # Default to autosave=True 
        )
    #If the dictionary does not represent a Patient, return it unchanged
    return dct
# This decoder ensures that JSON data representing a Patient can be properly reconstructed as a Patient object.
# It handles the preservation of numerical PHN values, ensures compatibility with JSON, and sets default parameters like autosave.