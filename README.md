# database Duello

Software per il progetto di riscrittura del software usato per il Database Duelli.
Progetto intrapreso nel 2006 dall' università di Roma la Sapienza.

### Informazioni tecniche

L' idea è di scrivere un software web-based appoggiandolo al framework Python Django.
Il database utilizzato (salvo direttive contrarie) sarà MySql.

~~Lo storage di file multimediali (immagini, audio, video etc..) sarà affidata al pacchetto
[pyFsdb](https://github.com/ael-code/pyFsdb)~~

### Progettazione

* Scrivere database:
  * Capire come strutturare database
  * Scrivere tabelle e relazioni tra di esse
* Interfaccia web:
  * Interfaccia per ricerca su db
  * Interfaccia di amministrazione per: aggiunta, rimozione e modifica di dati.
* Sistema di autenticazione ed autorizzazione:
  * Amministrazione sotto autenticazione (admin)
  * Consultazione tramite autenticazione (normal-user)


### Original Resources

[Database Duelli](http://studiinterculturali.uniroma1.it/node/5590)
Il database ad oggi è consultabile tramite richiesta di password (automatizzata)

### Installazione

#### Debian

``sudo apt-get install python-virtualenv libmysqlclient-dev libsqlite3-dev git``

il pacchetto ``libmysqlclient-dev`` è utilizzato se il database in uso è MySql altrimenti ``libsqlite3-dev`` per utilizzare SqLite.

#### Archlinux

``sudo pacman -Sy libmysqlclient python2-virtualenv git``
specificare che python deve essere la versione 2.* perché su archlinux la versione di default di python è la 3.*

a questo punto creare una directory
``mkdir Duello && cd Duello``

poi

``virtualenv env && source env/bin/activate``

a questo punto clona il repository:

``git clone https://github.com/frenko/dbDuello.git``

una volta all' interno del virtualenv eseguire:

``pip install -r requirements.txt`` 

per installare i pacchetti necessari al funzionamento di django.
Infine eseguire ``python manage.py runserver`` per lanciare il server di default di django e visualizzare l' applicazione.
