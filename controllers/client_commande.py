#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


# validation de la commande : partie 2 -- vue pour choisir les adresses (livraision et facturation)
@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    id_client = session['id_user']
    mycursor = get_db().cursor()
    tuple_param = (id_client,)
    sql = ''' SELECT ligne_panier.utilisateur_id, ligne_panier.id_cle_usb, ligne_panier.date_ajout, ligne_panier.quantite
        FROM ligne_panier
        JOIN cle_usb ON ligne_panier.id_cle_usb = cle_usb.id_cle_usb
        WHERE ligne_panier.utilisateur_id = %s;

    '''
    mycursor.execute(sql, tuple_param)
    item_panier = mycursor.fetchall()

    print(item_panier)

    if len(item_panier) >= 1:

        id_client = session['id_user']
        mycursor = get_db().cursor()
        tuple_param = (id_client,)
        sql = ''' SELECT SUM(ligne_panier.quantite * cle_usb.prix_cle_usb) AS prix_total
        FROM  ligne_panier
        JOIN cle_usb ON ligne_panier.id_cle_usb = cle_usb.id_cle_usb
        WHERE ligne_panier.utilisateur_id = %s; '''
        mycursor.execute(sql, tuple_param)

        prix_total = mycursor.fetchone()
        print('Le prix total est:'+str(prix_total))
    else:
        prix_total = None


    tabadr=(id_client)
    sqladress ='''SELECT id_adresse, nom, ville,rue,code_postal FROM adresse where id_utilisateur = %s and valide =1'''
    mycursor.execute(sqladress, tabadr)
    adresses=mycursor.fetchall()

    tabfav=(id_client)
    sqladressfav = '''SELECT id_adresse 
                      FROM adresse 
                      WHERE id_utilisateur = %s AND favori = 1'''
    mycursor.execute(sqladressfav, tabfav)
    id_adresse_fav = mycursor.fetchone()

    print(adresses)
    print(id_adresse_fav)
    return render_template('client/boutique/panier_validation_adresses.html'
                           , adresses=adresses
                           , item_panier= item_panier
                           , prix_total= prix_total
                           , id_adresse_fav=id_adresse_fav
                           )


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    id_client = session['id_user']
    id_adresse_livraison = request.form.get('id_adresse_livraison')
    adresse_identique = request.form.get('adresse_identique')
    id_adresse_facturation = request.form.get('id_adresse_facturation')



    print(adresse_identique)

    if adresse_identique is None:
        adresse_identique = id_adresse_facturation
        print(adresse_identique)
    else:
        adresse_identique = id_adresse_livraison
        print(adresse_identique)



    mycursor = get_db().cursor()

    tabfav=(id_client)
    sqlfav1='''update adresse set favori = 0 where id_utilisateur = %s '''
    mycursor.execute(sqlfav1, tabfav)
    get_db().commit()
    tabfav2=( id_adresse_livraison,id_client)
    sqlfav2='''update adresse set favori = 1, nb_utilisation = (nb_utilisation +1) where id_adresse =%s and id_utilisateur =%s'''
    mycursor.execute(sqlfav2, tabfav2)
    get_db().commit()
    # choix de(s) (l')adresse(s)form


    sql = '''SELECT * FROM ligne_panier WHERE utilisateur_id = %s '''
    mycursor.execute(sql, (id_client,))

    items_ligne_panier = mycursor.fetchall()
    if items_ligne_panier is None or len(items_ligne_panier) < 1:
        flash(u'Pas d\'articles dans le ligne_panier', 'alert-warning')
        return redirect('/client/article/show')

    date_commande = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tab = (date_commande, id_client, '1', id_adresse_livraison, adresse_identique)

    sql = '''INSERT INTO commande (date_achat, utilisateur_id, etat_id, idaddreseLivraison,idadresseFacture) VALUES (%s, %s, %s,%s,%s) '''
    mycursor.execute(sql, tab)

    sql = '''SELECT last_insert_id() as last_insert_id'''
    mycursor.execute(sql)
    commande_id = mycursor.fetchone()

    # numéro de la dernière commande
    for item in items_ligne_panier:
        sql = '''DELETE FROM ligne_panier WHERE id_ligne_panier = %s and id_cle_usb = %s '''
        mycursor.execute(sql, (item['id_ligne_panier'], item['id_cle_usb']))

        sql = '''SELECT prix_cle_usb FROM cle_usb WHERE id_cle_usb = %s '''
        mycursor.execute(sql, (item['id_cle_usb'],))
        prix = mycursor.fetchone()
        prix = prix['prix_cle_usb']

        sql = '''INSERT INTO ligne_commande (commande_id, cle_usb_id, prix, quantite) VALUES (%s, %s, %s, %s) '''
        tuple_insert = (commande_id['last_insert_id'], item['id_cle_usb'], prix, item['quantite'])
        mycursor.execute(sql, tuple_insert)

    get_db().commit()
    flash(u'Commande ajoutée','alert-success')
    return redirect('/client/article/show')








@client_commande.route('/client/commande/show', methods=['GET', 'POST'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    
    sql = '''SELECT id_commande, date_achat, COUNT(ligne_commande.quantite) AS nbr_articles, 
              SUM(ligne_commande.quantite * cle_usb.prix_cle_usb) AS prix_total, etat_id
          FROM commande
          JOIN ligne_commande ON commande.id_commande = ligne_commande.commande_id
          JOIN cle_usb ON ligne_commande.cle_usb_id = cle_usb.id_cle_usb
          WHERE commande.utilisateur_id = %s
          GROUP BY id_commande'''
    mycursor.execute(sql, (id_client,))
    commandes = mycursor.fetchall()
    articles_commande = None

    id_commande = request.args.get('id_commande')

    if id_commande:
        sql_articles = '''SELECT cle_usb.nom_cle_usb AS nom, ligne_commande.quantite, cle_usb.prix_cle_usb AS prix, 
                  (ligne_commande.quantite * cle_usb.prix_cle_usb) AS prix_ligne
              FROM ligne_commande
              JOIN cle_usb ON ligne_commande.cle_usb_id = cle_usb.id_cle_usb
              WHERE ligne_commande.commande_id = %s'''
        mycursor.execute(sql_articles, (id_commande,))
        articles_commande = mycursor.fetchall()


    commande_adresses=None
    sql_adresses = '''SELECT adresse_livraison.nom AS nom_livraison, adresse_livraison.rue AS rue_livraison, adresse_facturation.id_adresse as idfact,
                                adresse_livraison.code_postal AS code_postal_livraison, adresse_livraison.ville AS ville_livraison,
                                adresse_facturation.nom AS nom_facturation, adresse_facturation.rue AS rue_facturation,
                                adresse_facturation.code_postal AS code_postal_facturation, adresse_facturation.ville AS ville_facturation
                                ,adresse_livraison.id_adresse as idlivr
                         FROM commande
                         JOIN adresse adresse_livraison ON commande.idaddreseLivraison = adresse_livraison.id_adresse
                         JOIN adresse adresse_facturation ON commande.idadresseFacture = adresse_facturation.id_adresse
                         WHERE commande.id_commande = %s'''
    mycursor.execute(sql_adresses, (id_commande,))
    commande_adresses = mycursor.fetchone()


    
    return render_template('client/commandes/show.html',
                           commandes=commandes,
                           articles_commande=articles_commande,
                           commande_adresses=commande_adresses)
