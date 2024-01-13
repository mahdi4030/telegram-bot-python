import os
import random
import requests
import uuid
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

# Obtenir le chemin absolu du répertoire du script
chemin_repertoire = "data"
chemin_repertoire1 = ""

# Fonction pour charger les adresses e-mail depuis le fichier mail.txt
def charger_adresses_email():
    with open(os.path.join(chemin_repertoire, 'mail.txt'), 'r', encoding='utf-8') as mail_fichier:
        return mail_fichier.read().splitlines()

# Fonction pour écrire les adresses e-mail dans le fichier mail.txt
def ecrire_adresses_email(adresses):
    with open(os.path.join(chemin_repertoire, 'mail.txt'), 'w', encoding='utf-8') as mail_fichier:
        mail_fichier.write('\n'.join(adresses))

def append_adresses_email(generated_email):
    with open(os.path.join(chemin_repertoire, 'mail.txt'), 'a', encoding='utf-8') as mail_fichier:
        mail_fichier.write(f'\n{generated_email}')

# Charger les prénoms, noms et adresses e-mail
with open(os.path.join(chemin_repertoire, 'prenom.txt'), 'r', encoding='utf-8') as prenoms_fichier:
    prenoms = prenoms_fichier.read().splitlines()

with open(os.path.join(chemin_repertoire, 'nom.txt'), 'r', encoding='utf-8') as noms_fichier:
    noms = noms_fichier.read().splitlines()

# Fonction pour charger les adresses depuis un fichier
def charger_files(file_name, directory_name):
    with open(os.path.join(chemin_repertoire1, directory_name, file_name), 'r', encoding='utf-8') as file:
        return file.read().splitlines()

# Fonction pour sauvegarder les adresses dans un fichier
def sauvegarder_adresses(file_name, addresses):
    with open(os.path.join(chemin_repertoire1, 'adresse', file_name), 'w', encoding='utf-8') as file:
        file.write('\n'.join(addresses))

# Fonction pour générer un nom et prénom mélangés
def generer_nom_prenom():
    prenom = random.choice(prenoms)
    nom = random.choice(noms)
    return prenom + ' ' + nom

# Fonction pour envoyer les données via webhook
def envoyer_donnees_webhook(adresse_email, nom_prenom, adresse, identifiant, utilisateur, postal_code):
    url_webhook = "https://hook.eu1.make.com/cp4erl1o5m7xwka1qmgq9xg6jd297cse"
    payload = {
        "adresse_email": adresse_email,
        "nom_prenom": nom_prenom,
        "adresse": adresse,
        "identifiant": identifiant,  # Inclure l'identifiant dans le payload
        "utilisateur": utilisateur,
        "postal_code": postal_code
    }
    response = requests.post(url_webhook, json=payload)
    print(response.status_code)
    print(response.text)

# Nouvelle fonction pour charger les adresses depuis le fichier mail2.txt lorsque mail.txt est vide
def charger_adresses_mail2_si_vide():
    with open(os.path.join(chemin_repertoire, 'mail2.txt'), 'r', encoding='utf-8') as mail2_fichier:
        return mail2_fichier.read().splitlines()
    
def ecrire_adresses_mail2(addresses):
    with open(os.path.join(chemin_repertoire, 'mail2.txt'), 'w', encoding='utf-8') as mail_fichier:
        mail_fichier.write('\n'.join(addresses))

def append_adresses_mail2(addresse_email):
    path = os.path.join(chemin_repertoire, 'mail2.txt')
    with open(path, 'a', encoding='utf-8') as mail_fichier:
        if os.path.getsize(path) == 0:
            mail_fichier.write(f'{addresse_email}')
        else:
            mail_fichier.write(f'\n{addresse_email}')

# Commande /start
def start(update: Update, context: CallbackContext) -> None:
    global adresses_email
    adresses_email = charger_adresses_email()

    if not adresses_email:
        # Charger les adresses du fichier mail2.txt si mail.txt est vide
        adresses_email = charger_adresses_mail2_si_vide()
        if not adresses_email:
            update.message.reply_text("Désolé, il n'y a plus d'adresses e-mail disponibles.")
            return
        else:
            ecrire_adresses_email(adresses_email)
            ecrire_adresses_mail2([])

    # Générer un nouvel identifiant unique et le stocker dans user_data
    context.user_data['identifiant'] = str(uuid.uuid4())

    send_address_files(update, context)

# Nouvelle fonction pour afficher les boutons de choix de fichier d'adresse à l'utilisateur
def send_address_files(update: Update, context: CallbackContext) -> None:
    files = os.listdir(os.path.join(chemin_repertoire1, 'adresse'))
    buttons = [
        [InlineKeyboardButton(file_name, callback_data=f"choose_address_file:{file_name}")] for file_name in files
    ]
    reply_markup = InlineKeyboardMarkup(buttons)

    # Utiliser context.bot.send_message(...) au lieu de update.message.reply_text(...)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Choisissez le fichier contenant l'adresse :", reply_markup=reply_markup)

# Nouvelle fonction pour gérer le choix du fichier d'adresse par l'utilisateur
def choose_address_file(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    file_name = query.data.split(":")[1]
    context.user_data['selected_address_file'] = file_name

    # Continuer le processus en demandant à l'utilisateur de valider ou refuser l'adresse
    show_address_confirmation(update, context)

# Nouvelle fonction pour afficher l'adresse et demander à l'utilisateur de la valider ou refuser
def show_address_confirmation(update: Update, context: CallbackContext) -> None:
    selected_address_file = context.user_data.get('selected_address_file')
    if selected_address_file:
        addresses = charger_files(selected_address_file, "adresse")
        if addresses:
            selected_address = random.choice(addresses)
            context.user_data['selected_address'] = selected_address

            # Afficher l'adresse et les boutons de confirmation
            context.bot.send_message(chat_id=update.effective_chat.id, text="Adresse sélectionnée :\n{}".format(selected_address),
                                    reply_markup=InlineKeyboardMarkup([
                                        [InlineKeyboardButton("Valider l'adresse", callback_data="validate_address"),
                                         InlineKeyboardButton("Refuser l'adresse", callback_data="reject_address")]
                                    ]))
        else:
            update.message.reply_text("Le fichier {} est vide.".format(selected_address_file))
    else:
        update.message.reply_text("Vous n'avez pas encore choisi de fichier d'adresse.")

# Nouvelle fonction pour envoyer l'adresse par webhook et supprimer l'adresse du fichier après envoi
def envoyer_adresse_et_supprimer(adresse_email, nom_prenom, adresse, identifiant, utilisateur, postal_code):
    envoyer_donnees_webhook(adresse_email, nom_prenom, adresse, identifiant, utilisateur, postal_code)

    # Supprimer l'adresse e-mail envoyée du fichier mail.txt
    global adresses_email
    if adresse_email in adresses_email:
        adresses_email.remove(adresse_email)
        ecrire_adresses_email(adresses_email)
        append_adresses_mail2(adresse_email)
        

# Nouvelle fonction pour gérer la validation de l'adresse par l'utilisateur
def validate_address(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    selected_address = context.user_data.get('selected_address')
    if selected_address:
        buttons = [
            [InlineKeyboardButton("Ija", callback_data=f"user_selection:Ija"),
            InlineKeyboardButton("Mra", callback_data=f"user_selection:Mra")]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)

        # Utiliser context.bot.send_message(...) au lieu de update.message.reply_text(...)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Choisissez l'utilisateur :", reply_markup=reply_markup)
    else:
        query.message.reply_text("Vous n'avez pas encore choisi d'adresse à valider.")
        query.answer()

# Nouvelle fonction pour gérer le refus de l'adresse par l'utilisateur
def reject_address(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    # Supprimer l'adresse précédente de la session pour permettre au bot de proposer une nouvelle adresse
    del context.user_data['selected_address']

    selected_address_file = context.user_data.get('selected_address_file')
    addresses = charger_files(selected_address_file, "adresse")
    selected_address = random.choice(addresses)
    context.user_data['selected_address'] = selected_address
    # Continuer le processus
    query = update.callback_query
    query.edit_message_text("Adresse sélectionnée :\n{}".format(selected_address),
                            reply_markup=InlineKeyboardMarkup([
                                [InlineKeyboardButton("Valider l'adresse", callback_data="validate_address"),
                                InlineKeyboardButton("Refuser l'adresse", callback_data="reject_address")]
                            ]))

# Nouvelle fonction pour gérer le choix du fichier d'adresse par l'utilisateur
def user_selection(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    utilisateur = query.data.split(":")[1]
    context.user_data['utilisateur'] = utilisateur

    # Continuer le processus en demandant à l'utilisateur de valider ou refuser l'adresse
    show_email_confirmation(update, context)


""" email selection """
# Nouvelle fonction pour afficher l'e-mail et demander à l'utilisateur de la valider ou refuser
def show_email_confirmation(update: Update, context: CallbackContext) -> None:
    adresse_email = random.choice(adresses_email)
    context.user_data['adresse_email'] = adresse_email

    # Afficher l'e-mail et les boutons de confirmation
    context.bot.send_message(chat_id=update.effective_chat.id, text="E-mail sélectionnée :\n{}".format(adresse_email),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("Valider l'e-mail", callback_data="validate_email_address"),
                        InlineKeyboardButton("Refuser l'e-mail", callback_data="reject_email_address"),
                        InlineKeyboardButton("e-mail générer", callback_data="email_generate")]
                    ]))

# Nouvelle fonction pour gérer la validation de l'e-mail par l'utilisateur
def validate_email_address(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    selected_address = context.user_data.get('selected_address')
    adresse_email = context.user_data.get('adresse_email')
    if selected_address and adresse_email:
        show_name_confirmation(update, context)
    else:
        query.message.reply_text("Vous n'avez pas encore choisi d'adresse ou d'email à valider.")
        query.answer()

# Nouvelle fonction pour gérer le refus de l'e-mail par l'utilisateur
def reject_email_address(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    # Supprimer l'adresse précédente de la session pour permettre au bot de proposer une nouvelle adresse
    del context.user_data['adresse_email']

    adresse_email = random.choice(adresses_email)
    context.user_data['adresse_email'] = adresse_email

    # Continuer le processus
    query = update.callback_query
    query.edit_message_text("E-mail sélectionnée :\n{}".format(adresse_email),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Valider l'e-mail", callback_data="validate_email_address"),
                    InlineKeyboardButton("Refuser l'e-mail", callback_data="reject_email_address"),
                    InlineKeyboardButton("e-mail générer", callback_data="email_generate")]
                ]))

#email generate
def email_generate(update: Update, context: CallbackContext) -> None:
    # Set the URL for the POST request
    url = 'https://p55-maildomainws.icloud.com/v1/hme/generate'

    # Define the headers and cookies
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',  # Example header
        'Content-Type': 'application/json',  # Example header
        'X-Apple-Twosv-Trust-Token': 'HSARMTKNSRVXWFlaxiufPHaLA/yY/e2xmqVNuPMQOG+iHav5smb8p1TJD11QXTM98G13E8I4s2n7ByD8xPMz4Op+K7pECGxtroUfiC9MdlZlB2Wm9o1SK4vMeXvAKOus5nhwPHjkeqO5tNYOTNIR874/RMMb6iCqhJe1z8zF2TwJNlJcftY3hpYfHujuLuO4bh270+w/uCHS5oz9f/JAfZLf2ubr6pTs8f7lDPmgvQ==SRVX',
        'Accept': 'application/json, text/plain, */*',
        'X-Apple-Session-Token': 'izJzAA5Cwz3DeCx3bxwfYsV1VQW7ZMUokchcEpnjAz1HN/7gwW/lK7zVhYp1O5r6syB82yNlJZwhJ5D7zTdWlCRgSRO8jDzJgv2fuVT6vPmeWItaUpFQw8KBFNE+Loahk6T2K0YTXJEqZILdsur5F1LCb/9eP0zRck7bPmRCXNltnvRZLk8zwjEfQ+OkBrRkwQagniowIRWWxT9pP4KXt1F0lon88TyUE25LxTAw5jbO1NQi5TxNKXcua8l3ryZJoX6DKRVgtjbRXYNkfMQGDk0lfj1+5HiCVWdrlej18315rz9d3EVu/smy6iA4TZHoncHjcknu85jE8NrrNS/qX6FmzHutOvvKlGeNX8HSSnotZFeXk7JxmSlWBQT+tzQ9UwUiO51PZ1FUE7dcQlCOkcIybe9TQh5Xu6/MjCwG8avlF5aNHHwDnwtCX0yzQWNuY3saxS9NKvdmUrfqDJ9tHLuzYhIlzUNelIvVIikY023bXQPJQhvsw9KOvuZuCq2BScmg06ryyOkdz9R/Yk+RkcQXvfeVvXyvJtk8SnoAIytJIcOsVuvBVxYS1oy6J8zL+g1Rp9Zak94mRXuONtEmKIYDvsEpR9jVc/bL06xU152KlnlQjqyBimOWLr4XBWL8Sr9ORaxLHLazyOUY02yfFY0kcM0S/tX32x/dAZD8lTGQ+XkFcOL+3WdcbbOPCTwwnmv3krHpgUU2HXeraQqY2pmMEbcM3VjBLlFzZUrQrpB2NqY6jN7xPXplN/5HQUgitbIHnppsZ2eJeUEE7/sNdZeoXukwBZ9YoP0cNIT/CIrUZpqY7P16ddNoavIS+eOacqr17UaSeAcRiqroW4NmB2o1DZc9MIThIo2bChLQ3EpMTWHLIiYzJArIeFaqthnQi4WyejQ9fqLAOWs44rJmONlqa2Ov5wAb7GhTgXl/+m/2H8suoubNXYQl97vmJVE7AdBkQNU/Z+/rY/MWByrBqVcccOzbV/nhYAk50YR0roN12571+L5mVPn2H/DPwrvcf6DmUNMqBcwOPV9micBmCfYXBlHucJ6yDf2QbY4sFBFeEjAbmAa5sNkEHjxfWKU56qqQxW/SlFE6hOrpAWcZHKbgxpFwRaCZrQ1FPuNbU/sd42mawoW+ngbPWpKO+HesZc+NYppbHGLPqUKG75d50agGHQvJlpFiJFOGIhW3WwQZcKqyeWswn1c282aWs+SMAQ2UACM3YZ8q1Bo=',
        'X-Apple-Id-Account-Country': 'FRA',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Origin': 'https://www.icloud.com',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,fr-FR;q=0.8,fr;q=0.7',
        'Referer': 'https://www.icloud.com/',
        'Connection': 'close'
    }

    cookies = {
        'X_APPLE_WEB_KB-WFWZ4PBNDP9ETPOF8M5CCU-DQ74': 'v=1: t=Gg==BST_IAAAAAAABLwIAAAAAGTM3tARDmdzLmljbG91ZC5hdXRovQC_RYRPMNyM9ZEOdpESCsk24IEjSPOmRobtD7NzSXTq_xVPoIGVkHTw_QKQS39ya9Hea9Ddu7TBureEsuzGEE5wHkKVhnhwaUP8EmtNGEYFZ4yrhrq7Wk1vssPOEDx17Wn_ijGMHmKbptOPDwSoiFZno3I4TA~~',  # Example cookie
        'X-APPLE-WEBAUTH-HSA-TRUST': '876be86a633b92cecdc2bf3ee2a52fb7b45d557026b765fbc708d1165f2b660f_HSARMTKNSRVXWFlaXDh+kzSuLx6nRWuuh90xRUjT5Zm+hGfaw8Cr6M8GBMRo+ttUy+ySJfSUzS71HiubXAALi7wfpdFxviQV2wQs1wg4gP1iDmiS69ixR0f14D0jXDq1r3hCUIn0M8cCTYI33l2U9Qw/NQXATb3jy/ixuNe25/SRIWOZgjCI1Qx+/teUkkJjBvd+iaf8BhclIjds/GRuHPRRKOhQAlKC3zeuAbCxCw==SRVX',  # Example cookie
        'X-APPLE-WEBAUTH-USER': 'v=1:s=1:d=18319617384',
        'X-APPLE-DS-WEB-SESSION-TOKEN': 'AQGzmdNXEm+yq0+V7peD9ARhID7W7OqP3TZYplPJMtsJBw7PMUCOB6CDdfKuIjB4Qf8k1ydnzVjnbhKvJ2bC5AxMkILdiiM46QGSzeYC7GmMwl51dAt5KB3psOBu1h3hY1JX6KMAVVwPQJKltI0vKPBvtJ1w5xVfaXRKPUshVcMkfCJXJvewvgjltLlLbENtFtxXv/0Pl3/IuTrBYjbbV3VwT/Bcp5Ceu5kdDbKRTJS/Csb5lq0QmEA/vt2DxqYW1thP4jpEsZRigM+h8y+rh2ZzmWgMtymeCJhul1zTCZE+IOiqMEmk9OGc9+ESuZhUciGbKQjyUMWc1EzFOkjD1vDfbxP2lIhkEF0toWjZmx4JQ08wxiegQQ1td76T0EyeshSunP6eOMMd7KzZkjwsMDviq/qPgGz4ICFKW8cxF4eL3H4NhV0Sx0RFFCSW+PltlLhCd+2KsCPgZ+IRvOp4kY9unUrYkYS/s5XSOgZ/0qI0dCNqXhqUI8xPECfnVZjaUVPTTNH95/rJ+3ERbyR4BiBkVnM3gCXyFAxaxx5EGBFjfYXpZkskdDc7X6V8hXRrwdGxZ33p++n9MfdfacWXClYEZa2fP6naZaaowtG+XWskKo4nxNn+JolYEp5a2lOQyBEoUnWZUak/iUP58bfrZl61qEVSsqCqVmLr8O50AzfXt6vDFMlxUH3vXrAdxFuHfbuL0Em/Yt7OBxTqygW/uxKYHZJeG3t94K3z0w82+olNtzGB/ZztQSzDcLpwZmQGPlZKlDHn4qKMCGqmdENkJfERznJmbQWi3/rXYA==',
        'X-APPLE-WEBAUTH-PCS-Documents': 'TGlzdEFwcGw6MTpBcHBsOjE6AeUsbBpNG0kxP+kB1RHcfMyOY6LFr15TpuASkFh6qVU/YzHpHvTpPDznyQ+Y3iqxigze0DJYmW5CArahekkPqvmlytC9URY6P9EygrcRXNZgp7GsqgMx2nTn/wZs19Tmrk9H+mzNaPtvmdXaUIIt9cv/7iCIDWBT7oyADc/w48TpR3FmFtFqNw==',
        'X-APPLE-WEBAUTH-PCS-Photos': 'TGlzdEFwcGw6MTpBcHBsOjE6AfYw8o8NlXNoIdbh8HxrZsXNIoCLvVO+8DZQAqPdcopGdYokNPSQIonm9MMYX+QcwAdjPJlJS5J5fPr1X9RS4pXu3tEMz/rK4E8JUcIApbOlKjhRJSKEXi70ATj7rxFv6U54TAX5GbaWHzkIwZzKmU1x7euiL153XZkwMIali9r3aOemzLI3FQ==',
        'X-APPLE-WEBAUTH-PCS-Cloudkit': 'TGlzdEFwcGw6MTpBcHBsOjE6AcqEb4+NIe4QGdcVsUTKwUGw08VEaR6YSBk+ZZh0l3TKQm7WPelCIqACsUHf22lXzHFRfpf/8QhI9BwI2L46XmcRp4x2UZMufZH8J//N3f3NwbYipzdIUqLLc0ABsVoqvjZPc3HQw67bkfukp5ClCuPDxwQBK0+cxP7J0Ha81DIVV9UXBTpYcg==',
        'X-APPLE-WEBAUTH-PCS-Safari': 'TGlzdEFwcGw6MTpBcHBsOjE6AZtr2V4kiOWKJNSXM9Q4TmRhVoJHyNFWerEyi4HPG1vLeylh0+BqJIxkN6Aia2AMYOAzIU14FTs1p0gv048mUyTXSb9hQwQvnyD2NJQW7L1X9HczdKcXqGY1RInl0u/y07PjL9PGDiHh/Bv88ysWEvOYitime43CyZEl1MQRTJ3Lm0BtGQpjJg==',
        'X-APPLE-WEBAUTH-PCS-Mail': 'TGlzdEFwcGw6MTpBcHBsOjE6AYPsQ+V8f3tSYYFf12rxDGQqqlDMgMU5rq+wzMP7LmMH0JIzSuSoDGcL1o7IKei1M+opfJlCYpvNtQA1osXMeDOAJzHDhD+7rV/wt3V3aXBeU2Aa6F1ugfLvpKGXynuHDUYY2P4yI7wAEwFYAdq+1uuZUuvbi8bUZxkV5LQ9dXdsm+xyATV0GQ==',
        'X-APPLE-WEBAUTH-PCS-Notes': 'TGlzdEFwcGw6MTpBcHBsOjE6Aaj19yWLzeNrvkvRyffmXSrOQ8l837pAAQOz8LK9ImCMg62JCjT8dw08BCfx3VBcqSHZeNRRlPu2A7l3rZCiYWV1fjTyZuaags97c1tCpkIcNPxhZ5TCoIShqfedJtXbkcCDdn+MuyxRM+VSKQpZ9RuSqi1J10fgeCIJw4DXH+benyLi/Tp62w==',
        'X-APPLE-WEBAUTH-PCS-News': 'TGlzdEFwcGw6MTpBcHBsOjE6AcEjFDZ7WcK23wKNg4+QKM8DT9rl1IkLjnQ0KnJ9J5rFSKGgmVZdbTC8vwPwzQrdTEx7y9R86psJQUFMi4JOL44Xje03U4zULXw19X0qWNFwJdkrNsLtyeQ78BPaSSNy4vblztJc9MnXsGZmgU8Ty/ELkuAtLBGms9+ejlFsLSkljsAVDgRN3A==',
        'X-APPLE-WEBAUTH-PCS-Sharing': 'TGlzdEFwcGw6MTpBcHBsOjE6AXnJe/2Y6fDxfy121O4PIUF9tFZYCNPmNx6Aojx3AyB25QvZQBwcMUEcra6z3Kjt7FMeK44YvZKI1IvcttFM2BWXM8OJAfZ3yn+8Vj+pJJpRd3XY6jdDEQ9Q6ecAbfBv3wm/heyD81M95Sin52ANMbMZhDBiHoZmp0Ftk515Wwuh3IDLnJjNUw==',
        'X-APPLE-WEBAUTH-TOKEN': 'v=2:t=GA==BST_IAAAAAAABLwIAAAAAGTM9KYRDmdzLmljbG91ZC5hdXRovQDdieEZ51ZPqgtZQynLvGd9Wl-_AWUyx_PzFlFNPXVmdvHPzg24_4co006Vz9i1BUer0493R1PbAL-l6dmxmSoH0xMLns_WKDkS962qEvUxT45F94Cp0fSf8uFwfGCETgDFOF9es_nYTndb4z5hpQgJJPAlmA~~',
        'X-APPLE-WEBAUTH-VALIDATE': 'v=1:t=GA==BST_IAAAAAAABLwIAAAAAGTM9KYRDmdzLmljbG91ZC5hdXRovQDdieEZ51ZPqgtZQynLvGd9Wl-_AWUyx_PzFlFNPXVmdvHPzg24_4co006Vz9i1BUer0493R1PbAL-l6dmxmSoH0xMLns_WKDkS962qEvUxT5SAbbAbVpitwH3csHs3b1oYxI3NU3eDs3ncqvgyYuNYinNaMA~~'
    }

    # Send the POST request with the defined cookies, headers, and payload
    response = requests.post(url, headers=headers, cookies=cookies)
    response_json = response.json()

    # Check the response status code
    if response_json["success"]:
        created_mail = response_json["result"]["hme"]

        url = "https://p55-maildomainws.icloud.com/v1/hme/reserve"
        payload = {
            'hme': created_mail,  # Example payload data
            'label': 'settings',
            'note': 'Generated through the iCloud Telegram bot'
        }

        response = requests.post(url, headers=headers, cookies=cookies, json=payload)
        response_json = response.json()
        if response_json["success"]:
            # Get the response content
            # response_json = response.json()
            print(response_json["result"]["hme"]["hme"])
            del context.user_data['adresse_email']

            adresse_email = created_mail
            global adresses_email
            adresses_email.append(adresse_email)
            append_adresses_email(adresse_email)
            context.user_data['adresse_email'] = adresse_email

            # Continuer le processus
            query = update.callback_query
            query.edit_message_text("E-mail sélectionnée :\n{}".format(adresse_email),
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton("Valider l'e-mail", callback_data="validate_email_address"),
                            InlineKeyboardButton("Refuser l'e-mail", callback_data="reject_email_address"),
                            InlineKeyboardButton("e-mail générer", callback_data="email_generate")]
                        ]))
        else:
            query = update.callback_query
            query.message.reply_text("Échec de la génération d'e-mail, hme/reserve.")
            query.answer()
            # print('Request failed hme reserve:', response.text)
    else:
        query = update.callback_query
        query.message.reply_text("Échec de la génération d'e-mail, hme/generate.")
        # print('Request failed hme generate:', response.text)


""" name selection """
# Nouvelle fonction pour afficher l'e-mail et demander à l'utilisateur de la valider ou refuser
def show_name_confirmation(update: Update, context: CallbackContext) -> None:
    nom_prenom = generer_nom_prenom()
    context.user_data['nom_prenom'] = nom_prenom

    # Afficher l'e-mail et les boutons de confirmation
    context.bot.send_message(chat_id=update.effective_chat.id, text="Nom et prénom sélectionnée :\n{}".format(nom_prenom),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("Valider l'nom", callback_data="validate_name"),
                        InlineKeyboardButton("Refuser l'nom", callback_data="reject_name")]
                    ]))

# Nouvelle fonction pour gérer la validation de l'e-mail par l'utilisateur
def validate_name(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    selected_address = context.user_data.get('selected_address')
    adresse_email = context.user_data.get('adresse_email')
    nom_prenom = context.user_data.get('nom_prenom')
    if selected_address and adresse_email and nom_prenom:
        selected_address_file = context.user_data['selected_address_file']
        postal_code = "".join(selected_address_file.split(".")[:-1])
        identifiant = context.user_data['identifiant']  # Récupérer l'identifiant généré
        utilisateur = context.user_data['utilisateur']  # Récupérer l'identifiant généré

        # Créer le texte à envoyer en tant que message MarkdownV2
        text_to_send = (
            f"Adresse mail : `{adresse_email}`\n"
            f"Nom et prénom : `{nom_prenom}`\n"
            f"Adresse : `{selected_address}`\n"
            f"Identifiant : `{identifiant}`\n"  # Inclure l'identifiant dans le message
            f"Utilisateur : `{utilisateur}`\n"
            f"Postal Code : `{postal_code}`\n"
        )

        # Envoyer le texte en tant que message MarkdownV2
        query.message.reply_text(text_to_send, parse_mode=ParseMode.MARKDOWN_V2)

        # Envoyer les données via webhook en incluant l'identifiant et supprimer l'adresse du fichier mail.txt
        envoyer_adresse_et_supprimer(adresse_email, nom_prenom, selected_address, identifiant, utilisateur, postal_code)

        # Supprimer les données de la session pour permettre au bot de continuer
        del context.user_data['selected_address_file']
        del context.user_data['selected_address']
        del context.user_data['adresse_email']
        del context.user_data['nom_prenom']
        del context.user_data['utilisateur']
    else:
        query.message.reply_text("Vous n'avez pas encore choisi d'adresse, de mail ou de nom à valider.")
        query.answer()

# Nouvelle fonction pour gérer le refus de l'e-mail par l'utilisateur
def reject_name(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    # Supprimer l'adresse précédente de la session pour permettre au bot de proposer une nouvelle adresse
    del context.user_data['nom_prenom']

    nom_prenom = generer_nom_prenom()
    context.user_data['nom_prenom'] = nom_prenom

    # Continuer le processus
    query = update.callback_query
    query.edit_message_text("Nom et prénom sélectionnée :\n{}".format(nom_prenom),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("Valider l'nom", callback_data="validate_name"),
                        InlineKeyboardButton("Refuser l'nom", callback_data="reject_name")]
                    ]))
# ...

def main():
    # Remplacez "VOTRE_CLE_API" par la clé API de votre bot Telegram
    # updater = Updater("6253032181:AAFRBqZ_bqHIcFwQfgcZNk82UG5NPqPoRko")
    updater = Updater("6245556723:AAFpq6R1wi0NxoTHQ0mI-9gWiwLRZTV0vnU")
    dispatcher = updater.dispatcher

    # Définir le gestionnaire de la commande /start
    dispatcher.add_handler(CommandHandler("start", start))

    """ address validation """
    # Définir le gestionnaire pour la commande /send_address
    dispatcher.add_handler(CommandHandler("send_address", send_address_files))

    # Ajouter le gestionnaire pour les boutons de choix de fichier d'adresse
    dispatcher.add_handler(CallbackQueryHandler(choose_address_file, pattern="^choose_address_file:"))

    # Ajouter le gestionnaire pour le bouton de validation d'adresse
    dispatcher.add_handler(CallbackQueryHandler(validate_address, pattern="^validate_address$"))

    # Ajouter le gestionnaire pour le bouton de refus d'adresse
    dispatcher.add_handler(CallbackQueryHandler(reject_address, pattern="^reject_address$"))
    

    """ user selection """
    # Ajouter le gestionnaire pour les boutons de choix de fichier d'adresse
    dispatcher.add_handler(CallbackQueryHandler(user_selection, pattern="^user_selection:"))

    """ email validation """
    # Ajouter le gestionnaire pour le bouton de validation d'e-mail
    dispatcher.add_handler(CallbackQueryHandler(validate_email_address, pattern="^validate_email_address$"))

    # Ajouter le gestionnaire pour le bouton de refus d'e-mail
    dispatcher.add_handler(CallbackQueryHandler(reject_email_address, pattern="^reject_email_address$"))

    # Ajouter un gestionnaire pour le bouton de génération d'e-mails
    dispatcher.add_handler(CallbackQueryHandler(email_generate, pattern="^email_generate$"))

    """ name validation """
    # Ajouter le gestionnaire pour le bouton de validation d'nom
    dispatcher.add_handler(CallbackQueryHandler(validate_name, pattern="^validate_name$"))

    # Ajouter le gestionnaire pour le bouton de refus d'nom
    dispatcher.add_handler(CallbackQueryHandler(reject_name, pattern="^reject_name$"))
    
    # Démarrer le bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
