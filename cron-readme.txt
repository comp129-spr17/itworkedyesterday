In order to regularly check for notifications, you must do the following:
1. Alter cron_command.txt so that {SERVER PROJECT PATH GOES HERE} is replaced with the absolute path that leads to manage.py.
2. Run crontab -e
3. Paste the contents of cron_command.txt into the text editor.
4. Save. This should now execute python3 manage.py runcrons, every five minutes now.
