#!/bin/bash

# Exit on error
set -o errexit

# Create a virtual environment
python3 -m venv env

# Activate the virtual environment
# Use appropriate command for your operating system
if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
    source env/bin/activate
elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source env/Scripts/activate
else
    echo "Unsupported OS type: $OSTYPE"
    exit 1
fi

# Install the required packages
pip install -r requirements.txt

# Create the database and tables
psql -U postgres -f schema.sql

# Inform the user the setup is complete
echo "Setup complete. Virtual environment created and packages installed."
echo "To deactivate the virtual environment, run 'deactivate'."

# Inform the user to activate the virtual environment
echo "source env/bin/activate"

# Run the Flask project
flask run
