from flask import Blueprint, render_template
from flask_login import login_user, login_required, logout_user, current_user

views=Blueprint('views',__name__)

@views.route('/') #definizione del percorso della homepage
def home():
   return render_template("Home.html",user=current_user) #la funzione render_template() ci consente di caricare la pagina html passata
   # come primo argomento,è possibile passare anche altri argomenti in questo caso l'utente corrente

