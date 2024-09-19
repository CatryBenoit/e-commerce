#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_dataviz = Blueprint('admin_dataviz', __name__,
                        template_folder='templates')

@admin_dataviz.route('/admin/dataviz/etat1')
def show_type_article_stock():
    mycursor = get_db().cursor()
    sql = '''SELECT
    SUBSTRING(a.code_postal, 1, 2) AS departement, count(commande_id) as commande ,    SUM(lp.quantite * c.prix_cle_usb) AS chiffre_affaire
FROM
    commande cmd
JOIN
    adresse a ON cmd.idaddreseLivraison = a.id_adresse OR cmd.idadresseFacture = a.id_adresse
JOIN
    ligne_commande lc ON cmd.id_commande = lc.commande_id
JOIN
    cle_usb c ON lc.cle_usb_id = c.id_cle_usb
JOIN
    ligne_panier lp ON lp.id_cle_usb = c.id_cle_usb
GROUP BY
    departement;
    
           '''
    mycursor.execute(sql)
    adresse = mycursor.fetchall()

    sqladresse = '''
        SELECT
            SUBSTRING(a.code_postal, 1, 2) AS departement,
            COUNT(DISTINCT a.id_adresse) AS nombre_adresses
        FROM
            adresse a
        GROUP BY
            departement
        '''

    mycursor.execute(sqladresse)
    adresses_data = mycursor.fetchall()

    sqlchiffreAffaire = '''
    SELECT
        CAST(SUBSTRING(a.code_postal, 1, 2) AS VARCHAR(2)) AS departement,
       CAST(SUM(lp.quantite * c.prix_cle_usb) AS INT ) AS chiffre_affaire
    FROM
        commande cmd
    JOIN
        adresse a ON cmd.idaddreseLivraison = a.id_adresse OR cmd.idadresseFacture = a.id_adresse
    JOIN
        ligne_commande lc ON cmd.id_commande = lc.commande_id
    JOIN
        cle_usb c ON lc.cle_usb_id = c.id_cle_usb
    JOIN
        ligne_panier lp ON lp.id_cle_usb = c.id_cle_usb
    GROUP BY
        departement
    '''

    # Exécution de la requête SQL pour le chiffre d'affaires par département
    mycursor.execute(sqlchiffreAffaire)
    chiffre_affaire = mycursor.fetchall()


    labels_bar = [row['departement'] for row in adresses_data]
    values_bar = [row['nombre_adresses'] for row in adresses_data]

    labels_pie = [row['departement'] for row in chiffre_affaire]
    values_pie = [row['chiffre_affaire'] for row in chiffre_affaire]




    return render_template('admin/dataviz/dataviz_etat_1.html',
                           adresse=adresse,
                            labels_bar = labels_bar,
                            values_bar = values_bar,
                            labels_pie = labels_pie,
                            values_pie = values_pie)


# sujet 3 : adresses


@admin_dataviz.route('/admin/dataviz/etat2')
def show_dataviz_map():
    mycursor = get_db().cursor()
    sql = ''' SELECT SUBSTRING(code_postal, 1, 2) AS dep, COUNT(DISTINCT id_adresse) AS nbr_dept
                FROM adresse 
                   group by dep'''
    mycursor.execute(sql)
    adresses = mycursor.fetchall()
    print(adresses)



    # recherche de la valeur maxi "nombre" dans les départements
    maxAddress = 0
    for element in adresses:
        if element['nbr_dept'] > maxAddress:
             maxAddress = element['nbr_dept']
    # calcul d'un coefficient de 0 à 1 pour chaque département
        if maxAddress != 0:
             for element in adresses:
                indice = element['nbr_dept'] / maxAddress
                element['indice'] = round(indice,2)

    print(adresses)

    return render_template('admin/dataviz/dataviz_etat_map.html'
                           , adresses=adresses
                          )


