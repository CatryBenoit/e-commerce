#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin')
@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get','post'])
def admin_commande_show():
    mycursor = get_db().cursor()
    admin_id = session['id_user']

    sql = '''SELECT commande.id_commande, utilisateur.login, commande.date_achat, COUNT(ligne_commande.cle_usb_id) AS nbr_articles, 
                        SUM(ligne_commande.quantite * cle_usb.prix_cle_usb) AS prix_total, etat.libelle, GROUP_CONCAT(cle_usb.nom_cle_usb) AS nom_cle_usb,
                        adr_livraison.nom AS nom_livraison, adr_livraison.rue AS rue_livraison, adr_livraison.code_postal AS code_postal_livraison, adr_livraison.ville AS ville_livraison,
                        adr_facturation.nom AS nom_facturation, adr_facturation.rue AS rue_facturation, adr_facturation.code_postal AS code_postal_facturation, adr_facturation.ville AS ville_facturation,
                        CASE WHEN adr_livraison.id_adresse = adr_facturation.id_adresse THEN 'adresse_identique' ELSE 'adresse_différente' END AS adresse_identique
                 FROM commande
                 JOIN utilisateur ON commande.utilisateur_id = utilisateur.id_utilisateur
                 JOIN etat ON commande.etat_id = etat.id_etat
                 LEFT JOIN ligne_commande ON commande.id_commande = ligne_commande.commande_id
                 LEFT JOIN cle_usb ON ligne_commande.cle_usb_id = cle_usb.id_cle_usb
                 LEFT JOIN adresse adr_livraison ON commande.idaddreseLivraison = adr_livraison.id_adresse
                 LEFT JOIN adresse adr_facturation ON commande.idadresseFacture = adr_facturation.id_adresse
                 GROUP BY commande.id_commande'''

    mycursor.execute(sql)
    commandes = mycursor.fetchall()

    articles_commande = None
    commande_adresses = {}

    id_commande = request.args.get('id_commande')

    if id_commande is not None:

        sql_articles = '''SELECT cle_usb.nom_cle_usb AS nom, ligne_commande.quantite, 
                                     (ligne_commande.quantite * cle_usb.prix_cle_usb) AS prix_ligne, cle_usb.prix_cle_usb as prix
                              FROM ligne_commande
                              JOIN cle_usb ON ligne_commande.cle_usb_id = cle_usb.id_cle_usb
                              WHERE ligne_commande.commande_id = %s'''

        mycursor.execute(sql_articles, (id_commande,))
        articles_commande = mycursor.fetchall()


        sql_adresses = '''SELECT adr_livraison.nom AS nom_livraison, adr_livraison.rue AS rue_livraison, adr_livraison.code_postal AS code_postal_livraison, adr_livraison.ville AS ville_livraison,
                                     adr_facturation.nom AS nom_facturation, adr_facturation.rue AS rue_facturation, adr_facturation.code_postal AS code_postal_facturation, adr_facturation.ville AS ville_facturation,
                                     adr_livraison.id_adresse as idlivr,adr_facturation.id_adresse as idfact
                              FROM commande
                              LEFT JOIN adresse adr_livraison ON commande.idaddreseLivraison = adr_livraison.id_adresse
                              LEFT JOIN adresse adr_facturation ON commande.idadresseFacture = adr_facturation.id_adresse
                              WHERE commande.id_commande = %s'''

        mycursor.execute(sql_adresses, (id_commande,))
        commande_adresses = mycursor.fetchone()

    return render_template('admin/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )


@admin_commande.route('/admin/commande/valider', methods=['get','post'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    commande_id = request.form.get('id_commande', None)
    if commande_id != None:
        print(commande_id)
        sql = '''UPDATE commande SET etat_id = 4 WHERE id_commande = %s'''
        mycursor.execute(sql, (commande_id,))
        get_db().commit()
    return redirect('/admin/commande/show')
