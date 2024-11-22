import datetime
from flask import request, jsonify, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from pymongo import ReturnDocument
from api import mongo
from api.network import net_bp
from api.models import Network, ConnectionDetails
from api.utils.objectId import PydanticObjectId
from api.services.network_service import connect_to_network

db = mongo.db
users = db["users"]
networks = db["networks"]

@net_bp.route('/connect/<string:slug>', methods=["GET"])
@jwt_required
def connect(slug):
    try:
        res = networks.find_one({ "slug": slug })

        if not res:
            return jsonify({ "error": "Network not found" }), 404

        network = Network(**res)

        connection_details = network.connection_details

        if not connection_details.ip_address:
            return jsonify({ "error": "IP Address is required for connection" }), 400
        
        success = connect_to_network(
            ip_address=connection_details.ip_address, 
            token=connection_details.token, 
            credentials=connection_details.credentials)

        if success:
            return jsonify({ "message": "Connected to network successfully! "}), 200
        return jsonify({ "error": "Couldn't connect to the network" }), 500
    except Exception as e:
        print(f'Exception while connecting to network: {e}')
        return jsonify({ "error": "Internal Server Error" }), 500

@net_bp.route('/<string:slug>', methods=['GET'])
@jwt_required
def get_network(slug):
    try:
        data = networks.find_one({ 'slug': slug })

        if not data:
            return jsonify({ "error": "Network not found" }), 404

        return jsonify({ 
            "message": "Network fetched successfully",
            "network" : Network(**data).to_json()
        }), 200
    except Exception as e:
        print(f'Exception while fetching network: {e}')
        return jsonify({ "error": "Internal Server Error" }), 500

@net_bp.route('/', methods=['GET'])
@jwt_required
def get_all_networks():
    user_id = get_jwt_identity()
    page = int(request.args.get("page", 1))
    per_page = 10
    
    try:
        user_networks = networks.find({ "user_id": PydanticObjectId(user_id) })
        paginated_networks = user_networks.sort("created_at", -1).skip(per_page * (page - 1)).limit(per_page)
        network_count = networks.count_documents({ "user_id": PydanticObjectId(user_id) })

        links = {
            "self": {"href": url_for(".get_all_networks", page=page, _external=True)},
            "last": {
                "href": url_for(
                    ".get_all_networks", page=(network_count // per_page) + 1, _external=True
                )
            },
        }

        if page > 1:
            links["prev"] = {
                "href": url_for(".get_all_networks", page=page - 1, _external=True)
            }
        
        if page - 1 < network_count // per_page:
            links["next"] = {
                "href": url_for(".get_all_networks", page=page + 1, _external=True)
            }

        return jsonify(
            {
                "message": "Fetched all networks successfully",
                "networks": [Network(**doc).to_json() for doc in paginated_networks],
                "_links": links
            }
        ), 200
    except Exception as e:
        print(f'Exception while fetching networks: {e}')
        return jsonify({ "error": "Internal Server Error" }), 500

@net_bp.route('/add', methods=['POST'])
@jwt_required
def add_network():
    user_id = get_jwt_identity()
    data  = request.get_json()

    if not data or not all(field in data for field in ["name", "connection_details"]):
        return jsonify({ "error": "Missing required fields" }), 400
    
    connection_details = data.pop("connection_details", None)
    
    try:
        connection = ConnectionDetails(**connection_details)
        network = Network(**data)
        network.user_id = PydanticObjectId(str(user_id))
        network.connection_details = connection
        network.generate_slug(networks)

        network_id = networks.insert_one(network.to_bson()).inserted_id
        network.id = PydanticObjectId(str(network_id))

        return jsonify({
            "message": "Network added successfully",
            "network": network.to_json()
        }), 201

    except Exception as e:
        print(f"Exception while adding network: {e}")
        return jsonify({ "error": "Internal Server Error" }), 500

@net_bp.route('/update/<string:slug>', methods=['POST'])
@jwt_required
def update_network(slug):
    data = request.get_json()

    if not data:
        return jsonify({ "error": "Missing required fields" }), 400

    try:
        data["updated_at"] = datetime.datetime.now(tz=datetime.timezone.utc)

        updated_network = networks.find_one_and_update({ "slug": slug }, { "$set": data }, return_document=ReturnDocument.AFTER)

        if not updated_network:
            return jsonify({ "error": "Network not found" }), 404
        
        network = Network(**updated_network)

        return jsonify({ 
            "message": "Network updated successfully",
            "network": network.to_json()
        }), 200
    
    except Exception as e:
        print(f'Exception while updating network: {e}')
        return jsonify({ "error": "Internal Server Error" }), 500

@net_bp.route('/remove/<string:slug>', methods=['DELETE'])
@jwt_required
def remove_network(slug):
    try:
        deleted_network = networks.find_one_and_delete({ "slug": slug })

        if not deleted_network:
            return jsonify({ "error": "Network not found" }), 404

        return jsonify({
            "message": "Network removed successfully"
        }), 200

    except Exception as e:
        print(f'Exception while removing network: {e}')
        return jsonify({ "error": "Internal Server Error" }), 500