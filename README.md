Requirements to RUN

study_mode.py

Run pip install psutil first
Edit LMS_URL to your college portal link
Needs sudo on Mac/Linux to block sites (hosts file requires root)
Usage: sudo python study_mode.py 25 (or any duration in minutes)

file_organizer.py

No extra installs needed (stdlib only)
Defaults to ~/Downloads if no path given
Always do a dry run first: python file_organizer.py --dry-run
Live run: python file_organizer.py or python file_organizer.py /path/to/folder
