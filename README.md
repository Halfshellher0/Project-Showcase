# Project-Showcase

To set up the virtual python environment run these commands in a powershell terminal:

# Create the Virtual Environment
python -m virtualenv .venv

# Activate the Virtual Environment
.venv\Scripts\activate

# Install the required python modules
python -m pip install -r requirements.txt

# Record the installed modules in requirements.txt
pip freeze | Set-Content requirements.txt

# Run both backend and frontend servers
./Start.ps1
