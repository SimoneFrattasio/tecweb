from flask import Blueprint, render_template, request, flash, redirect, url_for , abort ,session
from sqlalchemy.engine import create_engine
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.expression import delete
from sqlalchemy import delete

from website.models import Utente , Lezioni
from werkzeug.security import generate_password_hash, check_password_hash
from website import db
from flask_login import login_user, login_required, logout_user, current_user


auth=Blueprint('auth',__name__)


@auth.route('/login',methods=['GET','POST']) #Passando alla funzione route l'array methods contenente le parole GET e POST stiamo stabilendo che è possibile effettuare richieste sia di tipo PUT che di tipo POST
def login():
    if request.method=='POST': #in questo caso gestiamo la richiesta di tipo POST
       email=request.form.get('email') #prendiamo i dati dal form compilato dall'utente
       password=request.form.get('password')
       utente=Utente.query.filter_by(email=email).first() #controlliamo se l'utente registrato con la mail inserita esiste
       if utente:
          if check_password_hash(utente.password,password): #controlliamo se la password inserita è corretta attraverso la funzione check password hash che controlla la password già crittografata
             flash('Login effettuato correttamente',category='success')
             login_user(utente,remember=True) #la funzione login_user() della libreria flask_login consente di effettuare il login e di ricordare l'utente durante la sessione
             return redirect(url_for('views.home'))
          else:
            flash('Password errata',category='error')
       else:
         flash('Utente non registrato',category='error')

    return render_template("login.html",user=current_user) 


@auth.route('/logout') # Gestione del logout
@login_required #il decoratore login_required importato da flask_login ci consente di accedere alla pagina solo se si è effettuato prima l'accesso
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@auth.route('/servizi') #Gestione pagina dei servizi
def servizi():
   return render_template("servizi.html",user=current_user)

@auth.route('/contatti') #Gestione pagina dei contatti
def contatti():
   return render_template("contatti.html",user=current_user)

@auth.route('/aula',methods=['GET','POST']) #Gestione della pagina per la visualizzazione e la prenotazione dei posti in aula
@login_required
def aula():
  if request.method=='POST': #Nel momento in cui arriva una richiesta di tipo POST dal client 
     id_allievo=current_user.id  #innanzitutto prendiamo i dati del form compilato e dell'utente corrente
     giorno=request.form.get('giorno')
     orario=request.form.get('orario')
     tipologia = 'aula'
     if giorno == '' or orario == '':
       flash('Compilare tutti i campi',category='error') #controlliamo se i campi sono tutti compilati
     elif Lezioni.calcolaPosti(giorno,orario,tipologia)<=0 :
        flash('Non ci sono posti disponibili',category='error') #controlliamo se ci sono posti disponibili con la funzione creata
     elif Lezioni.query.filter_by(giorno=giorno,tipologia=tipologia,id_allievo=id_allievo).first()!=None :
        print(Lezioni.query.filter_by(giorno=giorno,tipologia=tipologia,id_allievo=id_allievo).first())    #controlliamo se l'utente ha già prenotato una lezione per il giorno selezionato
        flash('Hai già prenotato una lezione per questo giorno',category='error')
     else:
       flash('Prenotazione effettuata con successo!',category='success')
       new_lezione = Lezioni(id_allievo=id_allievo, giorno=giorno,orario=orario,tipologia=tipologia) #nel caso in cui non si verificassero le condizioni precedenti procediamo all'inserimento della prenotazione nel database
       db.session.add(new_lezione)
       db.session.commit()
     
  return render_template("aula.html",user=current_user,lezione=Lezioni)

@auth.route('/guida',methods=['GET','POST']) 
@login_required
def guida(): #analogamente alla precedente questa funzione consente di gestire la pagina della prenotazione delle guide
   if request.method=='POST': 
     id_allievo=current_user.id #innanzitutto prendiamo i dati del form compilato e dell'utente corrente
     giorno=request.form.get('giorno')
     orario=request.form.get('orario')
     tipologia = 'guida'
     if giorno == '' or orario == '':
       flash('Compilare tutti i campi',category='error') #controlliamo se sono compilati tutti i campi
     elif Lezioni.calcolaPosti(giorno,orario,tipologia)<=0 :
        flash('Non ci sono posti disponibili',category='error')
     elif Lezioni.query.filter_by(giorno=giorno,tipologia=tipologia,id_allievo=id_allievo).count()>=2 : #controlliamo se l'utente ha già prenotato 2 lezioni per quel giorno
        flash('Hai già prenotato due lezioni per questo giorno',category='error')
     else:
       new_lezione = Lezioni(id_allievo=id_allievo, giorno=giorno,orario=orario,tipologia=tipologia) #in caso contrario creiamo un nuovo oggetto lezione e lo inseriamo nel database
       flash('Prenotazione effettuata con successo!',category='success')
       db.session.add(new_lezione)
       db.session.commit()

   return render_template("guida.html",user=current_user,lezione=Lezioni)

@auth.route('/iscrizione',methods=['GET','POST'])
@login_required
def signUp():  #questa funzione gestisce la pagina riguardante l'iscrizione di nuovi allievi

    if request.method=='POST':
       email=request.form.get('email')
       nome=request.form.get('nome')
       cognome=request.form.get('cognome')
       password1=request.form.get('password1')
       password2=request.form.get('password2')
       utente = Utente.query.filter_by(email=email).first()
       if utente:
          flash('Esiste già un account con questa email',category='error')
       elif len(email) < 4:
          flash('L indirizzo deve essere di almeno 4 caratteri.',category='error')
       elif len(nome) < 2:
          flash('Il nome  deve essere di almeno 2 caratteri.',category='error')
       elif password1 != password2:
          flash('Le password non corrispondono.',category='error')
       elif len(password1) < 6:
          flash('La password deve essere di almeno 6 caratteri.',category='error')
       else:
           new_utente = Utente(email=email, nome=nome,cognome=cognome, password=generate_password_hash(password1, method='sha256'))
           flash('Iscrizione effettuata!',category='success')
           db.session.add(new_utente)
           db.session.commit()
           return redirect(url_for('views.home'))
    if current_user.email=="admin@autoscuola.it": #E' possibile effettuare l'iscrizione di un nuovo allievo solo se sei l'amministratore
      return render_template("iscrizione.html",user=current_user)
    else:
      return abort(404)

@auth.route('/elenco',methods=['GET','POST'])
@login_required
def elenco(): # questa funzione consente di gestire la pagina dell'elenco delle prenotazioni
   if request.method=='POST':
      elenco=request.form.getlist('elenco_check_box')
      print(elenco)
      for elemento in elenco:
         print(elemento)
         l = Lezioni.query.filter_by(id=elemento).first() # e all'occorrenza di cancellare una lezione prenotata
         db.session.delete(l)
         db.session.commit()


   if current_user.email=="admin@autoscuola.it": #Se cerchiamo di caricare questa pagina loggati da amministratore avremo la possibilità di vedere ed eliminare tutte le lezioni prenotate dagli allievi
     return render_template("elenco.html",user=current_user,lezioni=Lezioni.query.filter_by().all(),utenti=Utente.query.filter_by().all())
   else:
      return render_template("elenco.html",user=current_user,lezioni=Lezioni.query.filter_by(id_allievo=current_user.id).all())
   

@auth.route('/anagrafica')
@login_required
def anagrafica():
   return render_template("anagrafica.html",user=current_user)