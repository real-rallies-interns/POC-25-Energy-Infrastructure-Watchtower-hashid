# Energy Infrastructure Watchtower Backend Runner
Set-Location -Path "backend"
if (-Not (Test-Path -Path ".venv")) {
    python -m venv .venv
}
& ".\.venv\Scripts\Activate.ps1"
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
