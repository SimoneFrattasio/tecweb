#In questo file dichiariamo le nostre 2 classi,che saranno anche le tabelle del nostro database grazie ad SQLAlchemy .
#SQLAlchemy è un ORM (Object Relational Mapper), una libreria di codice Python che trasferisce i dati archiviati in un database SQL 
# in oggetti Python.E' possibile utilizzare il codice Python per creare,leggere,aggiornare ed eliminare i dati invece di utilizzare SQL.
from . import db
from sqlalchemy import ForeignKey
from flask_login import UserMixin
from sqlalchemy.sql import func


class Utente(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    nome = db.Column(db.String(150))
    cognome=db.Column(db.String(150))


class Lezioni(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    id_allievo=db.Column(db.Integer,ForeignKey(Utente.id))
    giorno=db.Column(db.String(100))
    orario = db.Column(db.Integer)
    tipologia = db.Column(db.String(100))
    def calcolaPosti( gg,h,t): #Questa funzione consente di calcolare di volta in volta i posti rimanenti per una lezione in un determinato orario e giorno
      
      numeri = Lezioni.query.filter_by(giorno=gg,orario=h,tipologia=t)
      if t=="aula":
        posti=20-numeri.count()
      else :
          posti=3-numeri.count()
      return posti