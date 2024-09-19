#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import *
import datetime
from decimal import *
from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__,
                          template_folder='templates')


@fixtures_load.route('/base/init')
def fct_fixtures_load():
    mycursor = get_db().cursor()

    sql_statements = [
        'DROP TABLE IF EXISTS ligne_commande;',
        'DROP TABLE IF EXISTS ligne_panier;',
        'DROP TABLE IF EXISTS commande;',
        'DROP TABLE IF EXISTS utilisateur;',
        'DROP TABLE IF EXISTS etat;',
        'DROP TABLE IF EXISTS cle_usb;',
        'DROP TABLE IF EXISTS capacite;',
        'DROP TABLE IF EXISTS type_cle_usb;',
        'DROP TABLE IF EXISTS fournisseur;',
        '''
        CREATE TABLE IF NOT EXISTS fournisseur(
            id_fournisseur INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
            libelle_fournisseur VARCHAR(255)
        );
        ''',
        '''
        CREATE TABLE IF NOT EXISTS capacite (
            id_capacite INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
            libelle_capacite VARCHAR(255)
        );
        ''',
        '''
        CREATE TABLE IF NOT EXISTS type_cle_usb (
            id_type_cle_usb INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
            libelle_type_cle_usb VARCHAR(255)
        );
        ''',
        '''
        CREATE TABLE utilisateur(
            id_utilisateur INT AUTO_INCREMENT,
            login VARCHAR(50),
            email VARCHAR(50),
            password VARCHAR(250),
            role VARCHAR(50),
            nom VARCHAR(50),
            est_actif VARCHAR(50),
            PRIMARY KEY (id_utilisateur)
        );
        ''',
        '''
        CREATE TABLE IF NOT EXISTS etat (
            id_etat INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
            libelle VARCHAR(255)
        );
        ''',
        '''
        CREATE TABLE IF NOT EXISTS couleur(
            id_couleur INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
            libelle_couleur VARCHAR(255)
        );
        ''',
        '''
        CREATE TABLE IF NOT EXISTS cle_usb (
            id_cle_usb INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
            nom_cle_usb VARCHAR(255),
            description VARCHAR(255),
            vitesse_transfert INT,
            prix_cle_usb DECIMAL(10, 2),
            couleur_id INT,
            fournisseur_id INT,
            marque VARCHAR(255),
            image VARCHAR(255) UNIQUE ,
            capacite_id INT,
            type_cle_usb_id INT,
            stock INT,
            FOREIGN KEY (couleur_id) REFERENCES couleur(id_couleur),
            FOREIGN KEY (fournisseur_id) REFERENCES fournisseur(id_fournisseur),
            FOREIGN KEY (capacite_id) REFERENCES capacite(id_capacite),
            FOREIGN KEY (type_cle_usb_id) REFERENCES type_cle_usb(id_type_cle_usb)
        );

        ''',
        '''
        CREATE TABLE commande(
            id_commande INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
            date_achat DATE,
            utilisateur_id INT,
            etat_id INT,
            FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
            FOREIGN KEY (etat_id) REFERENCES etat(id_etat) );
        ''',
        '''
        CREATE TABLE ligne_panier (
        id_ligne_panier INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
        utilisateur_id INT,
        id_cle_usb INT,
        date_ajout DATETIME,
        quantite INT,
        FOREIGN KEY (utilisateur_id) REFERENCES utilisateur (id_utilisateur),
        FOREIGN KEY (id_cle_usb) REFERENCES cle_usb (id_cle_usb)
        );  

        ''',
        '''
        CREATE TABLE IF NOT EXISTS ligne_commande(
            commande_id INT,
            cle_usb_id INT,
            prix INT,
            quantite INT,
            FOREIGN KEY (commande_id) REFERENCES commande(id_commande),
            FOREIGN KEY (cle_usb_id) REFERENCES cle_usb(id_cle_usb)
        );
        ''',
        '''
        INSERT INTO couleur(libelle_couleur) VALUES
        ('Bleu'),
        ('Argent'),
        ('Noir'),
        ('Rouge');
        ''',
        '''
        INSERT INTO fournisseur(libelle_fournisseur) VALUES
        ('Amazon'),
        ('Flashbay'),
        ('SanDisk');
        ''',
        '''
        INSERT INTO etat(libelle) VALUES
        ('En attente'),
        ('Expédié'),
        ('Validé'),
        ('Confirmé');
        ''',
        '''
        INSERT INTO capacite(libelle_capacite) VALUES
        ('1Go'),
        ('16Go'),
        ('32Go'),
        ('64Go'),
        ('128Go'),
        ('256Go'),
        ('1To'),
        ('2To');
        ''',
        '''
        INSERT INTO type_cle_usb(libelle_type_cle_usb) VALUES
        ('USB'),
        ('DualC'),
        ('DualMicro');
        ''',
        '''
        INSERT INTO cle_usb VALUES
        (NULL, 'USB 1Go', 'Belle clé USB 1Go', 50, 20.6, 1, 1, 'imation', 'USB1Go.jpg', 1, 1, 42),
        (NULL, 'Clé USB 1To', 'Belle clé USB 1To', 50000, 0.6, 1, 2, 'SuperbX', 'USB1To.jpg', 7, 1, 14),
        (NULL, 'USB 2To', 'Belle clé USB 2To', 480, 9.99, 1, 3, 'DataTraveler', 'USB2To.jpg', 8, 1, 27),
        (NULL, 'Clé USB 16Go', 'Belle clé USB 16Go', 500, 39.99, 1, 1, 'Qilive', 'USB16Go.jpeg', 2, 1, 2),
        (NULL, 'Clé  USB128Go', 'Belle clé USB 128Go', 400, 19.99, 1, 2, 'POHOVE', 'USB128Go.jpg', 5, 1, 143),
        (NULL, 'USB DualC 16Go', 'Belle clé USB DualC 16Go', 460, 5.99, 1, 1, 'Wish', 'USBDualC16Go.jpg', 2, 2, 12),
        (NULL, 'DualC 32Go', 'Belle clé USB DualC 32Go', 367, 9.99, 1, 3, 'SanDisk', 'USBDualC32Go.jpg', 3, 2, 54),
        (NULL, 'Clé DualC 64Go', 'Belle clé USB DualC 64Go', 10, 1.99, 1, 2, 'EMTEC', 'USBDualC64Go.jpg', 4, 2, 22),
        (NULL, 'DualC 256Go', 'Belle clé USB DualC 256Go', 600, 9.99, 1, 1, 'KROCEUS', 'USBDualC256Go.jpg', 6, 2, 36),
        (NULL, 'DualMicro 2To', 'Belle clé USB DualMicro 2To', 900, 79.99, 1, 2, 'Wish', 'USBDualMicro2To.jpg', 8, 3, 48),
        (NULL, 'Clé USB DualMicro 32Go', 'Belle clé USB DualMicro 32Go', 2000, 8.99, 1, 3, 'SanDisk', 'USBDualMicro32Go.jpg', 3, 3, 8),
        (NULL, 'Clé DualMicro 32Go2', 'Belle clé USB DualMicro 32Go', 1957, 15.99, 1, 2, 'YLPUCI', 'USBDualMicro32Go2.jpg', 3, 3, 3),
        (NULL, 'USB DualMicro 64Go', 'Belle clé USB DualMicro 64Go', 480, 99.99, 1, 1, 'YLPUCI', 'USBDualMicro64Go.jpg', 4, 3, 124),
        (NULL, 'DualMicro 256Go', 'Belle clé USB DualMicro 256Go', 909, 60.99, 1, 3, 'DataTraveler', 'USBDualMicro256Go.jpg', 6, 3, 212),
        (NULL, 'Clé USB 32Go', 'Belle clé USB 32Go', 5678, 0.99, 1, 1, 'SanDisk', 'USB32Go.jpeg', 3, 1, 14298);

        ''',
        '''
        INSERT INTO utilisateur(login,email,password,role,nom,est_actif) VALUES
('admin','admin@admin.fr',
    'pbkdf2:sha256:600000$828ij7RCZN24IWfq$3dbd14ea15999e9f5e340fe88278a45c1f41901ee6b2f56f320bf1fa6adb933d',
    'ROLE_admin','admin','1'),
('client','client@client.fr',
    'pbkdf2:sha256:600000$ik00jnCw52CsLSlr$9ac8f694a800bca6ee25de2ea2db9e5e0dac3f8b25b47336e8f4ef9b3de189f4',
    'ROLE_client','client','1'),
('client2','client2@client2.fr',
    'pbkdf2:sha256:600000$3YgdGN0QUT1jjZVN$baa9787abd4decedc328ed56d86939ce816c756ff6d94f4e4191ffc9bf357348',
    'ROLE_client','client2','1');
        ''',

        '''
        INSERT INTO ligne_panier (utilisateur_id, id_cle_usb, date_ajout, quantite)
        VALUES
        (2, 1, NOW(), 1),
        (2, 2, NOW(), 1),
        (2, 3, NOW(), 1),
        (3, 4, NOW(), 1),
        (3, 5, NOW(), 1),
        (3, 6, NOW(), 1);
        ''',
        '''INSERT INTO commande (date_achat, utilisateur_id, etat_id)
            VALUES
            (NOW(), 2, 1),
            (NOW(), 2, 2),
            (NOW(), 3, 1);
            ''',
        '''
        INSERT INTO ligne_commande (commande_id, cle_usb_id, prix, quantite)
        VALUES
        (1, 2, 1.20, 2),
        (1, 6, 11.98, 2),
        (1, 1, 20.60, 1),
        (2, 8, 5.97, 3),
        (2, 7, 9.99, 1),
        (3, 3, 9.99, 1);'''
    ]

    for statement in sql_statements:
        mycursor.execute(statement)

    get_db().commit()
    return redirect('/')