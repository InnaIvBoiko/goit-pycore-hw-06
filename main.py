from collections import UserDict


class Field:
    """Basic class for record fields."""
    
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
    
class Name(Field):
    """Class for storing contact names. Required field."""
    
    def __init__(self, value):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty")
        super().__init__(value.strip())
        
        
class Phone(Field):
    """Class for storing and validating phone numbers."""
    
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Phone number must contain exactly 10 digits")
        super().__init__(value)

    @staticmethod
    def validate_phone(phone):
        # Remove any non-digit characters and check if it has exactly 10 digits
        digits_only = ''.join(filter(str.isdigit, phone))
        return len(digits_only) == 10
    
    
class Record:
    """Class for storing contact information, including name and list of phones."""

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        """Adding a phone number to the record."""
        phone_obj = Phone(phone)
        self.phones.append(phone_obj)
    
    def remove_phone(self, phone):
        """Removing a phone number from the record."""
        phone_to_remove = None
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                phone_to_remove = phone_obj
                break
        
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError(f"Phone {phone} not found")
    
    def edit_phone(self, old_phone, new_phone):
        """Editing a phone number in the record."""
        phone_found = False
        for phone_obj in self.phones:
            if phone_obj.value == old_phone:
                # Validate new phone before changing
                if not Phone.validate_phone(new_phone):
                    raise ValueError("New phone number must contain exactly 10 digits")
                phone_obj.value = new_phone
                phone_found = True
                break
        
        if not phone_found:
            raise ValueError(f"Phone {old_phone} not found")
    
    def find_phone(self, phone):
        """Searching for a phone number in the record."""
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(phone_obj.value for phone_obj in self.phones)}"


class AddressBook(UserDict):
    """Class for managing an address book."""
    
    def add_record(self, record):
        """Adding a record to the address book."""
        self.data[record.name.value] = record
    
    def find(self, name):
        """Searching for a record by name."""
        return self.data.get(name)
    
    def delete(self, name):
        """Removing a record by name."""
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError(f"Contact {name} not found")
        

# Example usage

if __name__ == "__main__":
    book = AddressBook()

    # Creating records for John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Adding records about John to the address book
    book.add_record(john_record)

    # Creating new records for Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Displaying all records in the address book
    for name, record in book.data.items():
        print(record)

    # Searching for John and editing his phone number
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Input: Contact name: John, phones: 1112223333; 5555555555

    # Searching for a specific phone number in John's record
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Output: 5555555555

    # Deleting Jane's record
    book.delete("Jane")    