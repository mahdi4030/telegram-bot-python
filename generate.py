from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
from geopy.geocoders import Nominatim
import random
import os
import telegram
import difflib

# États de la conversation
SET_ADDRESS, SET_FILENAME, GENERATING_ADDRESSES = range(3)

# Variables globales pour stocker les coordonnées GPS et le nom du fichier
base_latitude = None
base_longitude = None
filename = None
generated_addresses_count = 0

# Seuil de dissimilitude acceptable entre les adresses (à ajuster selon vos besoins)
SIMILARITY_THRESHOLD = 0.7

def similarity_score(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()

def generate_random_offset():
    max_offset = 0.005
    offset_latitude = random.uniform(-max_offset, max_offset)
    offset_longitude = random.uniform(-max_offset, max_offset)
    return offset_latitude, offset_longitude

def get_coordinates_from_address(address):
    geolocator = Nominatim(user_agent="coordinate_generator")
    try:
        location = geolocator.geocode(address)

        if location:
            latitude = location.latitude
            longitude = location.longitude
            return latitude, longitude
        else:
            raise ValueError("Impossible de trouver les coordonnées pour l'adresse spécifiée.")
    except geopy.exc.GeocoderUnavailable:
        raise ValueError("Service de géocodage indisponible. Veuillez réessayer plus tard.")

def set_address(update: Update, context: CallbackContext):
    global base_latitude, base_longitude

    # Obtenir l'adresse spécifiée par l'utilisateur dans le message
    user_specified_address = update.message.text

    try:
        # Obtenir les coordonnées GPS (latitude et longitude) à partir de l'adresse spécifiée
        coords = get_coordinates_from_address(user_specified_address)

        base_latitude, base_longitude = coords
        context.user_data['address'] = user_specified_address
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"L'adresse spécifiée a été enregistrée :\n{user_specified_address}")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Veuillez maintenant spécifier le nom du fichier où vous souhaitez enregistrer les adresses.")
        return SET_FILENAME
    except ValueError as e:
        send_error_message(update, context, str(e))
        return ConversationHandler.END

def set_filename(update: Update, context: CallbackContext):
    global filename

    # Obtenir le nom du fichier spécifié par l'utilisateur dans le message
    folder_name = "adresse"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    user_specified_filename = update.message.text
    filename = os.path.join(folder_name, user_specified_filename + ".txt")

    context.user_data['filename'] = filename  # Sauvegarder le nom du fichier dans user_data

    # Créer le fichier s'il n'existe pas
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as file:
            file.write("")

    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Le fichier '{filename}' a été créé ou mis à jour.")
    context.bot.send_message(chat_id=update.effective_chat.id, text="La génération des adresses a commencé...")
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=telegram.ChatAction.TYPING)  # Ajout de l'action du bot
    context.user_data['address_latitude'] = base_latitude  # Sauvegarder les coordonnées GPS dans user_data
    context.user_data['address_longitude'] = base_longitude

    # On passe maintenant à l'étape de génération des adresses
    context.user_data['generated_addresses_count'] = 0  # Réinitialiser le compteur
    generate_addresses(update, context)  # Appeler la fonction pour générer les adresses

    return ConversationHandler.END

def generate_address(update: Update, context: CallbackContext, latitude, longitude):
    generated_addresses_count = context.user_data.get('generated_addresses_count', 0)

    address = get_address_with_postalcode_city(latitude, longitude)
    if address and "," in address and address != ",":
        # Ajouter l'adresse dans le fichier
        with open(filename, "r", encoding="utf-8") as file:
            addresses_in_file = set(file.read().splitlines())

        # Vérifier les doublons
        if address not in addresses_in_file:
            # Vérifier la dissimilitude
            if not any(similarity_score(address, addr) > SIMILARITY_THRESHOLD for addr in addresses_in_file):
                with open(filename, "a", encoding="utf-8") as file:
                    file.write(f"{address}\n")
                generated_addresses_count += 1

    context.user_data['generated_addresses_count'] = generated_addresses_count

def generate_addresses(update: Update, context: CallbackContext):
    base_latitude = context.user_data.get('address_latitude')
    base_longitude = context.user_data.get('address_longitude')
    generated_addresses_count = context.user_data.get('generated_addresses_count', 0)

    # Vérifier si les coordonnées GPS et le nom de fichier ont été spécifiés par l'utilisateur
    if not base_latitude or not base_longitude or 'filename' not in context.user_data:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Veuillez d'abord spécifier l'adresse et le nom du fichier en envoyant les messages correspondants.")
        return

    # Utiliser une boucle for avec un pas de 30
    for i in range(generated_addresses_count, generated_addresses_count + 250, 30):
        for _ in range(30):
            offset_latitude, offset_longitude = generate_random_offset()
            latitude = base_latitude + offset_latitude
            longitude = base_longitude + offset_longitude

            generate_address(update, context, latitude, longitude)

        # Afficher la progression toutes les 30 adresses générées
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Progression : {context.user_data['generated_addresses_count']} / 250 adresses générées.")

    context.bot.send_message(chat_id=update.effective_chat.id, text="Génération des adresses terminée.")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Les adresses ont été enregistrées dans le fichier '{filename}'.")

def get_address_with_postalcode_city(lat, lon):
    geolocator = Nominatim(user_agent="address_generator")
    location = geolocator.reverse((lat, lon), exactly_one=True)
    if location:
        address_parts = location.raw['address']
        house_number = address_parts.get('house_number', '')
        road = address_parts.get('road', '')
        address = f"{house_number}, {road}"
        return address.strip() if address.strip() else "Adresse non trouvée"
    else:
        return "Adresse non trouvée"

def send_error_message(update, context, error_message):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Erreur : {error_message}")

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Veuillez envoyer l'adresse que vous souhaitez utiliser pour la génération des adresses.")
    return SET_ADDRESS

def cancel(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Opération annulée.")
    return ConversationHandler.END

def main():
    # Remplacez "YOUR_TELEGRAM_BOT_TOKEN" par votre token d'API Telegram
    updater = Updater("6345760997:AAEDJHASPMDzE9kN0zPvkzgoZ-LihFQjHJo")

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SET_ADDRESS: [MessageHandler(Filters.text & ~Filters.command, set_address)],
            SET_FILENAME: [MessageHandler(Filters.text & ~Filters.command, set_filename)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()