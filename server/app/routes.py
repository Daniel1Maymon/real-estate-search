from flask import jsonify, request, render_template
from flask_cors import CORS
from app import app
import services

# app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    '''
    **Main Flow:**
    - User enters the desired location, number of rooms, and price range into the search interface.
    - System validates the input and sends a request to various data sources.
    - System retrieves relevant property listings from the data sources.
    - System displays the matching properties along with details (e.g., address, price, number of rooms) to the user.
    '''
    
    # https://www.yad2.co.il/realestate/forsale?area=11&city=6200&rooms=3-4&price=1000000-1700000&Order=1
    
    # get real estate data --> data_result
    area = request.args.get('area')
    rooms = request.args.get('rooms') # range
    price = request.args.get('price')
    order = 1 # Sort by date
    city = '6200' # Bat Yam code
    
    if not area or not rooms or not price:
        return jsonify({'error': 'Please provide area, rooms, and price'}), 400
    
    data = aggregate_real_estate_data(area, rooms, price, order, city)
    
    # return data_result (send it to the frontend side)
    return jsonify(data)

@app.route('/')
def index():
    return render_template("input_form.html")

