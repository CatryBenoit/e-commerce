DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS adresse;
DROP TABLE IF EXISTS utilisateur;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS cle_usb;
DROP TABLE IF EXISTS capacite;
DROP TABLE IF EXISTS type_cle_usb;
DROP TABLE IF EXISTS fournisseur;

CREATE TABLE IF NOT EXISTS fournisseur(
    id_fournisseur INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    libelle_fournisseur VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS capacite (
    id_capacite INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    libelle_capacite VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS type_cle_usb (
    id_type_cle_usb INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    libelle_type_cle_usb VARCHAR(255)
);

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

CREATE TABLE adresse(
    id_adresse INT AUTO_INCREMENT,
    nom varchar(50),
    rue varchar(50),
    code_postal int,
    ville varchar(50),
    valide TINYINT(1),
    favori TINYINT(1),
    nb_utilisation int,
    id_utilisateur int not null,
    primary key (id_adresse),
    foreign key (id_utilisateur) references utilisateur(id_utilisateur)

);



CREATE TABLE IF NOT EXISTS etat (
    id_etat INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    libelle VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS couleur(
    id_couleur INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    libelle_couleur VARCHAR(255)
);

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

CREATE TABLE commande(
    id_commande INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    date_achat DATE,
    utilisateur_id INT,
    etat_id INT,
    idaddreseLivraison int not null,
    idadresseFacture int not null,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (etat_id) REFERENCES etat(id_etat),
    foreign key (idaddreseLivraison) REFERENCES adresse(id_adresse),
    FOREIGN KEY (idadresseFacture) REFERENCES  adresse(id_adresse)
);

CREATE TABLE ligne_panier (
    id_ligne_panier INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    utilisateur_id INT,
    id_cle_usb INT,
    date_ajout DATETIME,
    quantite INT,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur (id_utilisateur),
    FOREIGN KEY (id_cle_usb) REFERENCES cle_usb (id_cle_usb)
);

CREATE TABLE IF NOT EXISTS ligne_commande(
    commande_id INT,
    cle_usb_id INT,
    prix DECIMAL(10, 2),
    quantite INT,
    FOREIGN KEY (commande_id) REFERENCES commande(id_commande),
    FOREIGN KEY (cle_usb_id) REFERENCES cle_usb(id_cle_usb)
);

INSERT INTO couleur(libelle_couleur) VALUES
('Bleu'),
('Argent'),
('Noir'),
('Rouge');

INSERT INTO fournisseur(libelle_fournisseur) VALUES
('Amazon'),
('Flashbay'),
('SanDisk');

INSERT INTO etat(libelle) VALUES
('En attente'),
('Expédié'),
('Validé'),
('Confirmé');

INSERT INTO capacite(libelle_capacite) VALUES
('1Go'),
('16Go'),
('32Go'),
('64Go'),
('128Go'),
('256Go'),
('1To'),
('2To');

INSERT INTO type_cle_usb(libelle_type_cle_usb) VALUES
('USB'),
('DualC'),
('DualMicro');

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


SELECT c.nom_cle_usb, f.libelle_fournisseur, t.libelle_type_cle_usb
FROM cle_usb c
JOIN fournisseur f ON c.fournisseur_id = f.id_fournisseur
JOIN type_cle_usb t ON c.type_cle_usb_id = t.id_type_cle_usb;

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


INSERT INTO adresse (nom, rue, code_postal, ville, valide, favori, nb_utilisation, id_utilisateur)
VALUES
    ('Jean', 'Rue de la République', 69001, 'Lyon', 1, 0, 0, 2),
    ('Marie', 'Avenue des Champs-Élysées', 75008, 'Paris', 1, 1, 0, 2),
    ('Pierre', 'Boulevard Haussmann', 75000, 'Paris', 0, 0, 0, 2),
    ('Sophie', 'Place de la Bastille', 33000, 'Bordeaux', 1, 0, 0, 2),
    ('Luc', 'Rue du Faubourg Saint-Antoine', 31000, 'Toulouse', 1, 0, 0, 3),
    ('Anne', 'Rue de Rivoli', 59000, 'Lille', 1, 0, 0, 3),
    ('Thomas', 'Avenue Montaigne', 44000, 'Nantes', 1, 1, 0, 3),
    ('Julie', 'Rue de la Paix', 67000, 'Strasbourg', 1, 0, 0, 3);


INSERT INTO ligne_panier (utilisateur_id, id_cle_usb, date_ajout, quantite)
VALUES
(2, 1, NOW(), 1),
(2, 2, NOW(), 1),
(2, 3, NOW(), 1),
(3, 4, NOW(), 1),
(3, 5, NOW(), 1),
(3, 6, NOW(), 1);

SELECT lp.utilisateur_id, lp.id_cle_usb, lp.date_ajout, lp.quantite
FROM ligne_panier lp
JOIN cle_usb c ON lp.id_cle_usb = c.id_cle_usb
WHERE lp.utilisateur_id = 2;


SELECT SUM(lp.quantite * c.prix_cle_usb) AS prix_total
FROM ligne_panier lp
JOIN cle_usb c ON lp.id_cle_usb = c.id_cle_usb
WHERE lp.utilisateur_id = 2;

INSERT INTO commande (date_achat, utilisateur_id, etat_id, idadresseFacture,idaddreseLivraison)
VALUES
    ('2024-03-25', 2, 1, 1, 2),
    ('2024-03-27', 3, 1, 5, 6),
    ('2024-04-01', 2, 1, 3, 2),
    ('2024-04-02', 3, 1, 7, 6),
    ('2024-04-05', 2, 1, 4, 1),
    ('2024-04-07', 3, 1, 8, 5);


INSERT INTO ligne_commande (commande_id, cle_usb_id, prix, quantite)
VALUES
    (1, 2, 1.20, 2),
    (1, 6, 11.98, 2),
    (1, 1, 20.60, 1),
    (2, 8, 5.97, 3),
    (2, 7, 9.99, 1),
    (3, 3, 9.99, 1);



SELECT
    c.nom_cle_usb AS nom,
    lp.quantite AS quantite,
    c.prix_cle_usb AS prix,
    (lp.quantite * c.prix_cle_usb) AS prix_ligne,
    NULL AS nb_declinaisons,
    NULL AS couleur_id,
    NULL AS libelle_couleur,
    NULL AS taille_id,
    NULL AS libelle_taille
FROM ligne_commande lc
JOIN cle_usb c ON lc.cle_usb_id = c.id_cle_usb
JOIN commande cmd ON lc.commande_id = cmd.id_commande
JOIN utilisateur u ON cmd.utilisateur_id = u.id_utilisateur
JOIN ligne_panier lp
WHERE u.id_utilisateur = 2;


SELECT * FROM cle_usb;

SELECT last_insert_id() as last_insert_id;




#Select adresse.nom, adresse.rue, adresse.code_postal, adresse.ville, adresse.valide from adresse  join utilisateur on adresse.id_utilisateur = utilisateur.id_utilisateur where adresse.id_utilisateur = '2'

#select count(a.id_adresse) from adresse a where a.id_utilisateur ='2'

#test
select * from adresse a where a.id_adresse in (
SELECT a.id_adresse FROM ( SELECT a.id_adresse, ROW_NUMBER() over (ORDER BY c.date_achat DESC) AS num
                    FROM adresse a JOIN commande c ON a.id_adresse = c.idaddreseLivraison OR a.id_adresse = c.idadresseFacture
                     WHERE c.utilisateur_id = 2 AND a.id_adresse != 2 AND a.valide = 1) AS sub WHERE sub.num = 1)

SELECT SUBSTRING(code_postal, 1, 2) AS dep, COUNT(DISTINCT id_adresse) AS nombre
                FROM adresse
group by dep;

SELECT
    SUBSTRING(a.code_postal, 1, 2) AS departement,
    SUM(lp.quantite * c.prix_cle_usb) AS chiffre_affaires_total,
    count(commande_id) as commande
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


SELECT
    SUBSTRING(a.code_postal, 1, 2) AS departement,
    COUNT(DISTINCT cmd.id_commande) AS nombre_commandes
FROM
    commande cmd
JOIN
    adresse a ON cmd.idaddreseLivraison = a.id_adresse OR cmd.idadresseFacture = a.id_adresse
GROUP BY
    departement;
