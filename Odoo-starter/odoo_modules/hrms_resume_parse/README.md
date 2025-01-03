### ODIWARE HRMS RESUME PARSING MODULE

This module includes all systems that are required to parse resume and process other
related activities.

This module also requires you to install `openai==0.28` (version 0.28 specifically), `pymupdf` and `python-docx` 
by running: \
`pip install openai==0.28 pymupdf python-docx`

This modules requires you to set certain environment variable. Those
environment variable are listed below:

| Key                     | Default Value | Error                              |
|-------------------------|---------------|------------------------------------|
 `OPENAI_API`             | Unspecified   | Server will crash without this var 
