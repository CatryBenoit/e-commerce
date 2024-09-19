#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_coordonnee = Blueprint('client_coordonnee', __name__,
                        template_folder='templates')


@client_coordonnee.route('/client/coordonnee/show')
def client_coordonnee_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    utilisateurs = [id_client]

    tab = (utilisateurs)
    sqlutilisateur = '''SELECT email, login, nom FROM utilisateur WHERE id_utilisateur = %s'''
    mycursor.execute(sqlutilisateur, tab)
    utilisateur = mycursor.fetchone()

    sql = '''SELECT adresse.nom as nom, adresse.rue as rue, adresse.code_postal as code_postal, adresse.ville as ville, adresse.valide as valide, adresse.id_adresse, adresse.favori, adresse.nb_utilisation
             FROM adresse 
             JOIN utilisateur ON adresse.id_utilisateur = utilisateur.id_utilisateur 
             WHERE adresse.id_utilisateur = %s'''
    mycursor.execute(sql, tab)
    adresses = mycursor.fetchall()

    sql2 = '''SELECT COUNT(a.id_adresse) AS nbadresses FROM adresse a WHERE a.id_utilisateur = %s and a.valide = '1' '''
    mycursor.execute(sql2, utilisateurs)
    nb_adresses_dict = mycursor.fetchone()
    nb_adresses = nb_adresses_dict['nbadresses']

    if nb_adresses >= 4:
        message ="nombre maximale d'adresses  atteint"
        flash(message)



    return render_template('client/coordonnee/show_coordonnee.html',
                           utilisateur=utilisateur,
                           adresses=adresses,
                           nb_adresses=nb_adresses)

@client_coordonnee.route('/client/coordonnee/edit', methods=['GET'])
def client_coordonnee_edit():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sqlutilisateur='''select email, login, nom  from utilisateur where id_utilisateur=%s'''
    mycursor.execute(sqlutilisateur,(id_client))
    utilisateur = mycursor.fetchone()


    return render_template('client/coordonnee/edit_coordonnee.html'
                           ,utilisateur=utilisateur
                           )

@client_coordonnee.route('/client/coordonnee/edit', methods=['POST'])
def client_coordonnee_edit_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom=request.form.get('nom')
    login = request.form.get('login')
    email = request.form.get('email')

    tabverif=(login,email,id_client)

    sqlV = '''SELECT * FROM utilisateur WHERE (login = %s OR email = %s) AND id_utilisateur != %s'''
    mycursor.execute(sqlV, tabverif)
    utilisateur = mycursor.fetchone()

    sqlutilisateur='''select email, login, nom  from utilisateur where id_utilisateur=%s'''
    mycursor.execute(sqlutilisateur,(id_client))
    user = mycursor.fetchone()


    if utilisateur:
        flash(u'votre cet Email ou ce Login existe déjà pour un autre utilisateur', 'alert-warning')
        return render_template('client/coordonnee/edit_coordonnee.html'
                               , utilisateur=user
                               )

    tab =(nom,login,email, id_client)
    sql=''' UPDATE utilisateur SET nom =%s,login =%s,email =%s WHERE id_utilisateur=%s'''
    mycursor.execute(sql, (tab))

    get_db().commit()
    return redirect('/client/coordonnee/show')


@client_coordonnee.route('/client/coordonnee/delete_adresse',methods=['POST'])
def client_coordonnee_delete_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_adresse= request.form.get('id_adresse')

    tab2 = (id_adresse, id_client)
    sqlVfav = '''select favori from adresse where id_adresse =%s and id_utilisateur =%s'''
    mycursor.execute(sqlVfav, tab2)
    fav = mycursor.fetchone()
    print(fav)

    if fav is not None:
        tab3=(id_client,id_adresse)
        sqlfav2='''UPDATE adresse a SET favori = 1
                    WHERE id_adresse = ( SELECT a.id_adresse FROM ( SELECT a.id_adresse, ROW_NUMBER() over (ORDER BY c.date_achat DESC) AS num
                    FROM adresse a JOIN commande c ON a.id_adresse = c.idaddreseLivraison OR a.id_adresse = c.idadresseFacture
                     WHERE c.utilisateur_id = %s AND a.id_adresse != %s AND a.valide = 1) AS sub WHERE sub.num = 1);  '''
        mycursor.execute(sqlfav2, tab3)
        fa1v = mycursor.fetchone()
        print(fa1v)
        get_db().commit()

    tab=(id_adresse, id_client)
    sql = '''update adresse set valide=0 where id_adresse=%s and id_utilisateur =%s'''
    mycursor.execute(sql, tab)

    get_db().commit()
    return redirect('/client/coordonnee/show')

@client_coordonnee.route('/client/coordonnee/add_adresse')
def client_coordonnee_add_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']


    tab=(id_client)
    sql='''SELECT nom, login FROM utilisateur WHERE id_utilisateur = %s'''
    mycursor.execute(sql, (tab))
    utilisateur =mycursor.fetchone()
    get_db().commit()

    return render_template('client/coordonnee/add_adresse.html'
                           ,utilisateur=utilisateur
                           )

@client_coordonnee.route('/client/coordonnee/add_adresse',methods=['POST'])
def client_coordonnee_add_adresse_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom= request.form.get('nom')
    rue = request.form.get('rue')
    code_postal = request.form.get('code_postal')
    ville = request.form.get('ville')

    tabfav=(id_client)
    sqlfavsupp='''UPDATE adresse SET favori =0 WHERE id_utilisateur =%s'''
    mycursor.execute(sqlfavsupp, (tabfav))

    get_db().commit()

    tab=(id_client,nom,rue,code_postal,ville)
    sql='''INSERT INTO adresse(id_utilisateur, nom, rue, code_postal, ville,valide,favori, nb_utilisation ) VALUES (%s,%s,%s,%s,%s,1,1,0)'''
    mycursor.execute(sql, (tab))

    get_db().commit()

    return redirect('/client/coordonnee/show')

@client_coordonnee.route('/client/coordonnee/edit_adresse')
def client_coordonnee_edit_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_adresse = request.args.get('id_adresse')


    tab1 =(id_client)
    sqlutilisateur='''select email, login, nom  from utilisateur where id_utilisateur=%s'''
    mycursor.execute(sqlutilisateur,tab1)
    utilisateur = mycursor.fetchone()

    tab2 = (id_adresse,id_client)
    sqladresse='''select adresse.nom as nom, adresse.rue as rue, adresse.code_postal as code_postal, adresse.ville as ville, id_adresse  from adresse where id_adresse =%s and id_utilisateur =%s'''
    mycursor.execute(sqladresse, tab2)
    adresse = mycursor.fetchone()

    get_db().commit()
    return render_template('/client/coordonnee/edit_adresse.html'
                           ,utilisateur=utilisateur
                           ,adresse=adresse
                           )

@client_coordonnee.route('/client/coordonnee/edit_adresse',methods=['POST'])
def client_coordonnee_edit_adresse_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom= request.form.get('nom')
    rue = request.form.get('rue')
    code_postal = request.form.get('code_postal')
    ville = request.form.get('ville')
    id_adresse = request.form.get('id_adresse')

    tab2=(id_adresse,id_adresse)
    sqlverifcommande = "SELECT COUNT(*) as nbadresses  FROM commande WHERE idaddreseLivraison = %s OR idadresseFacture = %s"
    mycursor.execute(sqlverifcommande, tab2)
    nbcommande = mycursor.fetchone()
    nbcommande = nbcommande['nbadresses']
    print(nbcommande)

    if nbcommande > 0:

        tab3=(id_adresse)

        sqlCopieAddress = "INSERT INTO adresse (nom, rue, code_postal, ville, valide, favori, nb_utilisation, id_utilisateur) SELECT nom, rue, code_postal, ville, valide, favori, nb_utilisation, id_utilisateur FROM adresse WHERE id_adresse = %s"
        mycursor.execute(sqlCopieAddress, tab3)
        copie_id = mycursor.lastrowid
        tab4=(0,0,id_adresse,id_client)
        sql3=("update adresse SET valide =%s, favori =%s where id_adresse =%s and id_utilisateur=%s")
        mycursor.execute(sql3 , tab4)
        id_adresse = copie_id
        get_db().commit()



    tab =(nom,rue,code_postal,ville,id_adresse,id_client)
    sql='''UPDATE adresse SET nom = %s, rue = %s, code_postal = %s, ville =%s where id_adresse = %s and id_utilisateur =%s'''
    mycursor.execute(sql, tab)
    print(tab)
    get_db().commit()
    return redirect('/client/coordonnee/show')
