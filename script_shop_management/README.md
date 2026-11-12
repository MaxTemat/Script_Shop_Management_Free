<p align="center">
  <img src="static/description/icon.png" alt="Script Shop Management" width="140">
</p>

<h1 align="center">Script Shop Management</h1>
<p align="center"><b>Version gratuite</b> &middot; Odoo 19.0 &middot; LGPL-3</p>

Gérez vos **boutiques locales** (points de vente) depuis une seule application Odoo : les produits de chaque boutique,
les achats par boutique et un tableau de bord simple.

## Fonctionnalités

- **Boutiques locales** : tout point de vente peut être marqué « Est une boutique » et recevoir une image.
- **Produits par boutique** : la caisse d'une boutique ne charge que les produits qui lui sont assignés.
- **Boutique de destination** sur les bons de commande d'achat et sur les transferts de stock.
- **Un entrepôt, une boutique** : un entrepôt ne peut être le stock que d'une seule boutique.
- **Menu Achats** : les achats qui ont une boutique de destination, avec recherche rapide par boutique et par article.
- **Tableau de bord** : une carte par boutique et une carte « Toutes les boutiques », sélecteur de période, trois
  indicateurs (achats, ventes locales, stock). Un clic sur les achats ou les ventes ouvre la liste filtrée.
- **Sécurité** : groupes *Utilisateur* et *Responsable*.
- **Langues** : anglais et français.

## Besoin de plus ?

**Script Shop Management Pro** (extension payante) ajoute les boutiques en ligne liées à vos boutiques locales, le stock
partagé, le menu Commandes unifié (caisse + site), le tableau de bord du stock, les courbes et la comparaison
en ligne contre local.

## Installation

1. Copier le dossier `script_shop_management` dans le chemin des addons d'Odoo.
2. Mettre à jour la liste des applications et installer **Script Shop Management**.

Dépendances : `point_of_sale`, `purchase`, `stock`.

## Prise en main

1. Ajouter votre utilisateur au groupe *Script Shop Management* (Utilisateur ou Responsable).
2. Configuration du point de vente : cocher **Est une boutique** et ajouter une image. Donner à chaque boutique son entrepôt.
3. Sur les produits, renseigner **Disponible dans les boutiques**.
4. Ouvrir **Script Shop Management › Tableau de bord**.

> Ce module contient du code Python : il n'est pas compatible avec Odoo Online (Odoo.sh ou installation sur serveur).

## Auteur

**Script Consulting** &middot; licence LGPL-3.
