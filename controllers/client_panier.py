#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                          template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST']) #fait
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article')
    quantite = request.form.get('quantite')

    id_declinaison_article = 1

    # Uncomment this section to handle variations of articles

    # id_declinaison_article = request.form.get('id_declinaison_article', None)
    # declinaisons = mycursor.fetchall()
    # if len(declinaisons) == 1:
    #   id_declinaison_article = declinaisons[0]['id_declinaison_article']
    # elif len(declinaisons) == 0:
    #    abort("pb nb de declinaison")
    # else:
    #    sql = '''   '''
    #    mycursor.execute(sql, (id_article,))
    #    article = mycursor.fetchone()
    #    return render_template('client/boutique/declinaison_article.html',
    #                           declinaisons=declinaisons,
    #                           quantite=quantite,
    #                           article=article)

    sql = '''select id_cle_usb from ligne_panier where id_cle_usb = %s and utilisateur_id = %s'''
    mycursor.execute(sql, (id_article, id_client))

    result = mycursor.fetchone()

    if result is not None and len(result) == 1:
        sql2 = '''update ligne_panier set quantite = quantite + %s where id_cle_usb = %s and utilisateur_id =%s'''
        mycursor.execute(sql2, (quantite, id_article, id_client))

    else:
        sql_insert_panier = """
            INSERT INTO ligne_panier (utilisateur_id, id_cle_usb, date_ajout, quantite)
            VALUES (%s, %s, NOW(), %s)
            """
        mycursor.execute(sql_insert_panier, (id_client, id_article, quantite))

    sql_update_stock = """
    UPDATE cle_usb
    SET stock = stock - %s
    WHERE id_cle_usb = %s
    """
    mycursor.execute(sql_update_stock, (quantite, id_article))

    get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/delete', methods=['POST']) #fait
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article')
    quantite = 1

    sql_select_panier = "SELECT quantite FROM ligne_panier WHERE utilisateur_id = %s AND id_cle_usb = %s"
    mycursor.execute(sql_select_panier, (id_client, id_article))
    quantitepanier = mycursor.fetchone()

    if quantitepanier['quantite'] > 1:

        sql_update_quantite = "UPDATE ligne_panier SET quantite = quantite - 1 WHERE utilisateur_id = %s AND id_cle_usb = %s"
        mycursor.execute(sql_update_quantite, (id_client, id_article))
    else:

        sql_delete_panier = "DELETE FROM ligne_panier WHERE utilisateur_id = %s AND id_cle_usb = %s"
        mycursor.execute(sql_delete_panier, (id_client, id_article))

    sql_update_stock = "UPDATE cle_usb SET stock = stock + %s WHERE id_cle_usb = %s"
    mycursor.execute(sql_update_stock, (quantite, id_article))

    get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/vider', methods=['POST']) #fait
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']

    sql_select_panier = "SELECT id_cle_usb, quantite FROM ligne_panier WHERE utilisateur_id = %s"
    mycursor.execute(sql_select_panier, (client_id,))
    items_panier = mycursor.fetchall()

    for item in items_panier:
        item_id = item['id_cle_usb']
        quantite = item['quantite']

        sql_delete_item = "DELETE FROM ligne_panier WHERE utilisateur_id = %s AND id_cle_usb = %s"
        mycursor.execute(sql_delete_item, (client_id, item_id))

        sql_update_stock = "UPDATE cle_usb SET stock = stock + %s WHERE id_cle_usb = %s"
        mycursor.execute(sql_update_stock, (quantite, item_id))

    get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/delete/line', methods=['POST']) #fait
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_cle_usb = request.form.get('id_article')
    # id_declinaison_article = request.form.get('id_declinaison_article')

    sql_update_stock = ''' UPDATE cle_usb SET stock = stock + (SELECT quantite FROM ligne_panier WHERE utilisateur_id = %s AND id_cle_usb = %s) WHERE id_cle_usb = %s'''
    mycursor.execute(sql_update_stock, (id_client, id_cle_usb, id_cle_usb))

    sql_delete_panier = "DELETE FROM ligne_panier WHERE utilisateur_id = %s AND id_cle_usb = %s"
    mycursor.execute(sql_delete_panier, (id_client, id_cle_usb))




    get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre', methods=['POST']) #fait
def client_panier_filtre():
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)

    session['filter_word'] = filter_word
    session['filter_prix_min'] = filter_prix_min
    session['filter_prix_max'] = filter_prix_max
    session['filter_types'] = filter_types
    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST']) #fait
def client_panier_filtre_suppr():
    session.pop('filter_word', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    session.pop('filter_types', None)
    print("suppr filtre")
    return redirect('/client/article/show')
