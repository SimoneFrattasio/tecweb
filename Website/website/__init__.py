#Questo file serve per inizializzare il nostro programma un file __init__.py in python assume 
# un significato specifico: fa si che un progetto all’interno di una cartella sia considera un modulo python.
from flask import Flask
from flask_login.utils import login_required
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
db=SQLAlchemy() #dichiarazione del database
DB_NAME = "database.db"
def createApp():
    app=Flask(__name__) #inizializzazione 
    app.config['SECRET_KEY']='SIMONE'  #dichiariamo la nostra secret key,Ciascuna applicazione Web Flask contiene una chiave segreta  
    # utilizzata per firmare i cookie di sessione per la protezione contro la manomissione dei dati
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  #collegamento del database
    db.init_app(app)
    
    from .views import views
    from auth import auth

    app.register_blueprint(views,url_prefix='/')#Registrazione dei blueprint auth.py e views.py
    app.register_blueprint(auth,url_prefix='/')

    from .models import Utente
    create_database(app)  

    login_manager=LoginManager() #Inizializziamo l'oggetto login_manager che ci consente di utilizzare le funzionalità della libreria  
    login_manager.login_view = 'auth.login' #flask login.Flask-Login fornisce la gestione della sessione utente per Flask. Gestisce le attività comuni di accesso, 
    login_manager.init_app(app) #  disconnessione e memorizzazione delle sessioni degli utenti per lunghi periodi di tempo.


    @login_manager.user_loader
    def load_user(id):
        return Utente.query.get(id)  
    
    return app

def create_database(app): #questa funzione consente di creare il database qualora al momento dell'avvio dell'applicazione non esistesse
        if not path.exists('website/' + DB_NAME):
            db.create_all(app=app)
            print('Database creato')
