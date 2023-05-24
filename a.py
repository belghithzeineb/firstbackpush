import os
import shutil
import zipfile 
import json
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, make_response, request, jsonify, send_file
import fitz
import time
from flask_cors import CORS
import base64
from flask import send_from_directory
import io
from io import BytesIO
from PIL import Image
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/auth_demo'
mongo = PyMongo(app)
CORS(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']

    # Vérifier si l'utilisateur existe déjà
    existing_user = mongo.db.users.find_one({'username': username})
    if existing_user:
        return jsonify({'error': 'Username already exists'})

    # Hasher le mot de passe
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insérer l'utilisateur dans la base de données
    user_id = mongo.db.users.insert_one({'username': username, 'password': hashed_password}).inserted_id

    return jsonify({'message': 'User registered successfully', 'user_id': str(user_id)})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    # Récupérer l'utilisateur depuis la base de données
    user = mongo.db.users.find_one({'username': username})
    if not user:
        return jsonify({'error': 'Invalid username or password'})

    # Vérifier le mot de passe
    if bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'error': 'Invalid username or password'})
@app.route('/downloadpdf/<filename>', methods=['GET'])
def download_pdf(filename):
    try:
        pdf_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)
        return send_file(pdf_path)
    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred while processing your request."

@app.route("/form", methods=["POST"])
def add_page():
    try:
           
        data = request.json['data']
       
        pdf_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),'document.pdf')
        doc = fitz.open(pdf_path)
        app.logger.info(f"{pdf_path} opened successfully with {len(doc)} pages")

        with open('a.json', 'r') as f:
                    input_data = json.load(f)


        for item in input_data:
                    for field in item['ids']:
                        # Skip this field if it does not have an 'x' value
                        if 'x' not in field:
                            continue
                        
                        x = field['x']
                        y = field['y']
                        z = field['lines']
                        print(data[z])

                        # Define the color for text fields
                        color = (field['color']['r'], field['color']['g'], field['color']['b'])

                        page = doc[0]

                        if field['visibility'] == 'Oui':  
                            app.logger.info(f"Processing {field['fieldType']} field at ({x}, {y})")

                            if field['fieldType'] == 'image':
                                img_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '4.JPG')
                                image_rect = fitz.Rect(x, y, x + 100, y + 100)
                                page.insert_image(image_rect, filename=img_path)

                            elif field['fieldType'] == 'Text':
                                text = f" {data[z]}"
                                font = field['fontFamily'] 
                                size = field['size']
                                page.insert_text((x, y), text, fontname=font, fontsize=size, fill=color)


                            elif field['fieldType'] == 'Check':
                                new_size = (300, 300)
                                image = Image.open("check2.png")
                                image = image.resize(new_size)
                                buf = io.BytesIO()
                                image.save(buf, format='PNG')
                                image_data = buf.getvalue()
                                buf.close()
                                a=x-14
                                b=y-14
                                image_rect = fitz.Rect(a, b, a+43,b+43)
                                page.insert_image(image_rect, stream=image_data)

                            elif field['fieldType'] == 'Phone':
                                text = f" {data[z][:8]}"
                                font = field['fontFamily'] 
                                size = field['size']
                                page.insert_text((x, y), text, fontname=font, fontsize=size, fill=color)

                            elif field['fieldType'] == 'IBAN':
                                text = f" {data[z][:24]}"
                                font = field['fontFamily'] 
                                size = field['size']
                                page.insert_text((x, y), text, fontname=font, fontsize=size, fill=color)

                            elif field['fieldType'] == 'BIC':
                                text = f" {data[z][:11]}"
                                font = field['fontFamily'] 
                                size = field['size']
                                page.insert_text((x, y), text, fontname=font, fontsize=size, fill=color)

                # Save the modified PDF
        timestamp = int(time.time())
        output_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), f'modified_{timestamp}.pdf')
        doc.save(output_path)
        app.logger.info(f"{output_path} saved successfully")
        name=f"modified_{timestamp}.pdf"
        print({"url":f"http://127.0.0.1:5000/downloadpdf/{name}"})
        return make_response({"url":f"http://127.0.0.1:5000/downloadpdf/{name}"},200) 
            #eturn send_file(pdf_data, mimetype='application/pdf', as_attachment=True, attachment_filename='output.pdf')




    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return "An error occurred while processing your request."
@app.route('/')
def index():
    # Chemin du dossier à créer
    dossier = os.path.join(os.getcwd(),  'pfe1')
    os.makedirs(dossier, exist_ok=True)
    return 'Dossier créé avec succès !'

@app.route('/copydossier')
def copydossier():
    # Chemin du dossier source à copier
    sourcePath = os.path.abspath('pfe')

    # Chemin du dossier de destination
    destinationPath = os.path.join(os.getcwd(), 'pfe1', 'l')

    # Utilisation de la fonction shutil.copytree pour copier le dossier
    try:
        shutil.copytree(sourcePath, destinationPath)
        message = f"The folder {sourcePath} was successfully copied to {destinationPath}"
    except Exception as e:
        message = f"An error occurred while copying the folder: {str(e)}"

    return message

@app.route('/copyfile', methods=['POST'])
def copyfile():
    file = request.files['file']
    filename = file.filename
    new_filename = "data.json"  # Remplacez "nouveau_nom.txt" par le nom que vous souhaitez donner au fichier.
    destination = os.path.join(os.getcwd(),  'pfe1', 'l', 'src', new_filename)
    new_filename1 = "a.json" 
    
    file.save(destination)
  
    return 'File saved successfully!'

@app.route('/copypdf', methods=['POST'])
def copypdf():
    pdf_file = request.files['pdf_file']
    filename = pdf_file.filename
    new_filename = "document.pdf"
    # Remplacez "document.pdf" par le nom que vous souhaitez donner au fichier PDF.
   
    destination = os.path.join(os.getcwd(),  'pfe1', new_filename)
    pdf_file.save(destination)
    
    return 'PDF file saved successfully!'

@app.route('/zipfolder')
def zipfolder():
    # Chemin du dossier à compresser
    folder_path = os.path.join(os.getcwd(),  'pfe1')

    # Chemin du fichier zip de destination
    zip_path = os.path.join(os.getcwd(),  'pf1.zip')

    # Utilisation de la fonction zipfile.ZipFile pour compresser le dossier
    try:
        with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_file.write(file_path, os.path.relpath(file_path, folder_path))
        message = f"The folder {folder_path} was successfully compressed to {zip_path}"
    except Exception as e:
        message = f"An error occurred while compressing the folder: {str(e)}"

    return message

@app.route('/downloadzip')
def download_zip():
    # Chemin du fichier zip à télécharger
    zip_path = os.path.join(os.getcwd(),  'pf1.zip')

    # Vérifier si le fichier zip existe
    if not os.path.exists(zip_path):
        return "Le fichier zip n'existe pas !"

    # Lire le contenu du fichier zip
    with open(zip_path, 'rb') as file:
        zip_content = file.read()

    

    # Utilisation de la fonction send_file de Flask pour renvoyer le fichier zip en tant que réponse HTTP
    return send_file(zip_path, as_attachment=True)
if __name__== '__main__':
    app.run(debug=True ,port=5000,host='0.0.0.0')