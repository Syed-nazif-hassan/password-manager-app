# Password Manager

This is a password manager application built using `PySide`, a `Python` framework. It allows you to save, retrieve, and manage your passwords securely. The application uses `PyCryptodome` for encrypting all data to ensure your passwords are kept safe. Your passwords are stored locally in a JSON file with the data encrypted for security.

## Features

- Save and manage multiple passwords under a single identifier.
- Retrieve password using identifier.
- Encrypts all data for security.
- Handles empty input and incorrect identifiers by showing error messages.
- Copy or delete individual passwords.
- View all saved identifiers and passwords.

## Pages

### Save Password
- Allows you to save an identifier and its associated password.
- The data is encrypted and stored securely.

### Retrieve Password
- Enter an identifier to retrieve all associated passwords.
- A popup will display the identifier and all the passwords under it.
- Buttons available in the popup:
  - `Copy`: Copy the selected password.
  - `Delete`: Delete the selected password.
  - `Show All Passwords`: View all identifiers and their associated passwords in another popup.
