# Run backend
cd $PSScriptRoot
.venv/Scripts/activate
uvicorn main:app --host localhost --port 8000