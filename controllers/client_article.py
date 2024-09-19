#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_article = Blueprint('client_article', __name__,
                           template_folder='templates')


@client_article.route('/client/index')
@client_article.route('/client/article/show')
def client_article_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    filter_word = session.get('filter_word')
    filter_prix_min = session.get('filter_prix_min')
    filter_prix_max = session.get('filter_prix_max')
    filter_types = session.get('filter_types')

    # Building the SQL query based on filters
    sql = '''SELECT id_cle_usb as id_article, nom_cle_usb as nom, description as libelle,
                         prix_cle_usb as prix, image as image, stock as stock
                 FROM cle_usb
             WHERE 1=1'''
    param = []
    if filter_word:
        sql += " AND nom_cle_usb LIKE %s'"
        param.append(filter_word)
        print(param)
    if filter_prix_min:
        sql += " AND prix_cle_usb >= %s"
        param.append(filter_prix_min)
        print(param)
    if filter_prix_max:
        sql += " AND prix_cle_usb <= %s"
        param.append(filter_prix_max)
        print(param)
    if filter_types:
        sql += " and type_cle_usb_id = %s"
        param.append(int(filter_types[0]))

    mycursor.execute(sql, param)
    articles = mycursor.fetchall()

    mycursor = get_db().cursor()
    sql2 = '''SELECT id_type_cle_usb as id_type_article, libelle_type_cle_usb as libelle FROM type_cle_usb'''
    mycursor.execute(sql2)
    types_article = mycursor.fetchall()

    mycursor = get_db().cursor()
    sql3 = '''SELECT c.id_cle_usb as id_article, c.nom_cle_usb as nom , quantite  as quantite, c.prix_cle_usb as prix  FROM ligne_panier join cle_usb c on ligne_panier.id_cle_usb = c.id_cle_usb where utilisateur_id = %s'''
    mycursor.execute(sql3, id_client)
    articles_panier = mycursor.fetchall()

    if len(articles_panier) >= 1:
        mycursor = get_db().cursor()
        param = (id_client,)
        sql4 = '''SELECT SUM(c.prix_cle_usb * quantite) AS prix_total
          FROM ligne_panier 
          JOIN cle_usb c ON ligne_panier.id_cle_usb = c.id_cle_usb 
          WHERE utilisateur_id = %s'''
        mycursor.execute(sql4, param)
        prix_total = mycursor.fetchone()

    else:
        prix_total = None
    return render_template('client/boutique/panier_article.html'
                           , articles=articles
                           , articles_panier=articles_panier
                           , prix_total=prix_total
                           , items_filtre=types_article
                           )
