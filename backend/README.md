
# Le nom du projet!


## Dev notes - Backend

### postgres

    sudo apt-get install postgresql postgresql-contrib
    sudo -u postgres createuser --superuser jdisctf
    sudo su - postgres
    createdb -O jdisctf jdisctf_db

### venv

    pip install virtualenv
    virtualenv venv
    source venv/bin/activate


### Setup flask (sera automatisé plus tard)

Dans le venv:

    pip install -r requirements.txt
    
    export FLASK_APP=JDISCTF
    export FLASK_ENV=development
    export DATABASE_URL=postgresql://localhost/jdisctf_db
    flask run