from .patient_record import PatientRecord


class Patient:
    def __init__(self, phn, name, birth_date, phone, email, address, autosave=False):
        #Setting all of the variables of Patient class
        self.phn = phn
        self.name = name
        self.birth_date = birth_date
        self.phone = phone
        self.email = email
        self.address = address
        self.autosave = autosave #Must have autosave for persistance
        #Patient record is the old way of storing patient data, kept for compiling/testing
        self.patient_record = PatientRecord(patient_phn=phn, autosave=autosave)

    #Both functions below are testing functions used earlier in development
    def __eq__(self, other):
        if not isinstance(other, Patient):
            return False
        return (
            self.phn == other.phn and
            self.name == other.name and
            self.birth_date == other.birth_date and
            self.phone == other.phone and
            self.email == other.email and
            self.address == other.address
        )
    
    def __repr__(self):
        """String representation of the Patient for debugging purposes."""
        return (f"Patient(phn={self.phn}, name={self.name}, birth_date={self.birth_date}, "
                f"phone={self.phone}, email={self.email}, address={self.address})")