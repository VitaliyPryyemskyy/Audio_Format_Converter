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

# Apply patch to pytube
patch $(python -c "import pytube; import os; print(os.path.join(os.path.dirname(pytube.__file__), 'cipher.py'))") << 'EOF'
--- /usr/lib/python3.12/site-packages/pytube/cipher.py	2024-04-05 16:22:49.000000000 -0500
+++ ./cipher.py	2024-07-09 12:34:40.705106637 -0500
@@ -271,6 +271,7 @@
         # In the above case, `iha` is the relevant function name
         r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&.*?\|\|\s*([a-z]+)',
         r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])?\([a-z]\)',
+        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])\([a-z]\)',
     ]
     logger.debug('Finding throttling function name')
     for pattern in function_patterns:
EOF

# Create the database and tables
psql -U postgres -f schema.sql

# Inform the user the setup is complete
echo "Setup complete. Virtual environment created and packages installed."
echo "To deactivate the virtual environment, run 'deactivate'."

# Inform the user to activate the virtual environment
echo "source env/bin/activate"

# Run the Flask project
flask run
