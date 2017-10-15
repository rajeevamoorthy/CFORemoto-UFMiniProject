# CFORemoto-UFMiniProject

- Dev Environment: Eclipse Oxygen
- Python: 2.7
- Django: 1.11.6
- sqlite: 3.13
- Beautifulsoup: 4
- Selenium: 3.6.0
- ChromeDriver: 2.27 Download from https://chromedriver.storage.googleapis.com/index.html?path=2.27/ and modify location of chrome driver in globalConstants.chromeDriverLocation

**NOTES:**
- You might have to run the following:
  - python manage.py makemigrations uf
  - python manage.py migrate

**Start the server:**
- python manage.py runserver
- Access the site at: http://127.0.0.1:8000/uf/
  - Access the functionalities from the menu presented.
- retrieveUF can be run as a Cron Job(daily): /uf/retrieveUF

**Known Issues:**
- Unit tests are not Included
- Exception handlng is not implemented elegantly
- Selenium and ChromeDriver are used to emulate human interaction on the bCentral site - there may be other tricks to make this elegant. Though this is slow, this is a easier implementation.




