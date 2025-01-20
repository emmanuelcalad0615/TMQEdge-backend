from flask import Blueprint, request, jsonify
import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()


amplitud_bp = Blueprint('amplitud', __name__, url_prefix='/amplitud')

def get_amplitud_data():
    api_url = os.getenv("API_AMPLITUD")
    
    try:
        response = requests.get(api_url)
        print(response.status_code) 

        response.raise_for_status()  
        
        if response.status_code == 200:
            print("Procesando datos...")
            return response.json()
    except requests.exceptions.RequestException as e:
            return jsonify({"error": str(e)}), 500

def format_date(date:str):
    return datetime.strptime(date, "%d%m%Y") 

def get_data_nyse_with_header(header:str):

    data = get_amplitud_data()
    nyse_data = data["datosAmplitud"]["nyse"]
    headers = nyse_data[0]
    rows = nyse_data[1:]

    rasi_index = headers.index(header)
    date_index = headers.index("Fecha")

    one_year_ago = datetime.now() - timedelta(days=365)
    
    filtered_rows = [row for row in rows if (format_date(row[date_index]) >= one_year_ago)]
    
    header_values = [row[rasi_index] for row in filtered_rows]
    dates_values  = [row[date_index] for row in filtered_rows]

    return {"dates":dates_values[::-1], "values": header_values[::-1]}




# def amplitud_stream():

#     api_url = os.getenv("API_AMPLITUD")
    
#     try:
#         response = requests.get(api_url, stream=True)
#         print(response.status_code) 

#         response.raise_for_status()  
        
#         if response.status_code == 200:
#             print("Procesando datos en streaming...")
#             for chunk in response.iter_content(chunk_size=1024):  
#                 if chunk:  
                    
#                     print(chunk.decode("utf-8")) 
               
            
    
#     except requests.exceptions.RequestException as e:
#             return jsonify({"error": str(e)}), 500


@amplitud_bp.route('/datos', methods=['GET'])
def ver_datos():
    processed_data = get_data_nyse_with_header("RASI")

    return jsonify(processed_data), 200

