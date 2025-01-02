# external imports
import datetime
from bson import ObjectId
from pymongo import ReturnDocument
from typing import Tuple, Dict, Any
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, current_app, jsonify, url_for, abort

# internal imports
from api import mongo
from api.networks import net_bp
from api.utils.object_id import PydanticObjectId
from api.services.network_service import connect_to_network
from api.db_models.network_models import Network, ConnectionDetails

db = mongo.db
users = db['users']
networks = db['networks']

@net_bp.route('/connect/<string:slug>', methods=['GET'])
@jwt_required()
def connect(slug) -> Tuple[Dict[str, Any], int]:
    """
    Endpoint to connect to given network.

    Args
        slug: unique identifier for the network

    Returns
        Tuple[Dict[str, Any], int]: json representation, status code
    """
    try:
        res = networks.find_one({ 'slug': slug })

        if not res:
            abort(404, 'Network not found.')

        network = Network(**res)

        connection_details = network.connection_details

        if not connection_details.ip_address:
            abort(404, 'IP address is not set for this network.')
        
        success = connect_to_network(
            ip_address = connection_details.ip_address, 
            token = connection_details.token, 
            credentials = connection_details.credentials
        )

        if success:
            return jsonify({ 'message': 'Network connected successfully.' }), 200
        
        abort(500, 'Couldn\'t connect to the network')
    
    except Exception as e:
        current_app.logger.error('Error while connecting to network %s: %s', slug, e)
        raise e

@net_bp.route('/<string:slug>', methods=['GET'])
@jwt_required()
def get_network(slug) -> Tuple[Dict[str, Any], int]:
    try:
        user_id = get_jwt_identity()
        data = networks.find_one({ 'slug': slug, 'user_id': ObjectId(user_id) })

        if not data:
            abort(404, 'Network not found or is unauthorized.')

        return jsonify({ 
            'message': 'Network fetched successfully.',
            'network' : Network(**data).to_json()
        }), 200
    
    except Exception as e:
        current_app.logger.error('Error while fetching network %s: %s', slug, e)
        raise e

@net_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_networks() -> Tuple[Dict[str, Any], int]:
    try:
        user_id = get_jwt_identity()
        page = max(int(request.args.get('page', 1)), 1)
        per_page = min(int(request.args.get('per_page', 10)), 20)

        user_networks = networks.find({ 'user_id': ObjectId(user_id) })
        paginated_networks = user_networks.sort('created_at', -1).skip(per_page * (page - 1)).limit(per_page)
        network_count = networks.count_documents({ 'user_id': ObjectId(user_id) })

        links = {
            'self': {
                'href': url_for(
                    '.get_all_networks', 
                    page = page, 
                    _external = True
                )
            },
            'last': {
                'href': url_for(
                    '.get_all_networks', 
                    page=(network_count // per_page) + 1, 
                    _external = True
                )
            },
        }

        if page > 1:
            links['prev'] = {
                'href': url_for('.get_all_networks', page = page - 1, _external = True)
            }
        
        if page - 1 < network_count // per_page:
            links['next'] = {
                'href': url_for('.get_all_networks', page = page + 1, _external = True)
            }

        return jsonify({
                'message': 'Fetched all networks successfully.',
                'networks': [Network(**doc).to_json() for doc in paginated_networks],
                '_links': links
        }), 200
    
    except Exception as e:
        current_app.logger.error('Error while fetching all networks: %s', e)
        raise e

@net_bp.route('/add', methods=['POST'])
@jwt_required()
def add_network() -> Tuple[Dict[str, Any], int]:
    try:
        user_id = get_jwt_identity()
        data  = request.get_json()
        name = data.get('name', '').strip().lower()
        connection_details = data.pop('connection_details', None)

        if not data or not connection_details or not name:
            abort(400, 'Missing required fields.')

        if not isinstance(connection_details, dict):
            abort(400, 'Connection details must be a collection of key-value pairs.')

        connection = ConnectionDetails(**connection_details)
        network = Network(**data)
        network.user_id = PydanticObjectId(str(user_id))
        network.connection_details = connection
        network.generate_slug(networks)

        network_id = networks.insert_one(network.to_bson()).inserted_id
        network.id = PydanticObjectId(str(network_id))

        return jsonify({
            'message': 'Network added successfully.',
            'network': network.to_json()
        }), 201

    except Exception as e:
        current_app.logger.error('Error while adding network: %s', e)
        raise e

@net_bp.route('/update/<string:slug>', methods=['PUT'])
@jwt_required()
def update_network(slug: str) -> Tuple[Dict[str, Any], int]:
    """
    Endpoint to update network.

    Args
        slug: unique identifier for network

    Returns 
        Tuple[Dict[str, Any], int]: json representation, status code
    """
    try:
        data = request.get_json()

        if not data:
            abort(400, 'No data to update.')
        
        data['updated_at'] = datetime.datetime.now(tz = datetime.timezone.utc)

        updated_network = networks.find_one_and_update(
            { 'slug': slug }, 
            { '$set': data }, 
            return_document = ReturnDocument.AFTER
        )

        if not updated_network:
            abort(404, 'Network not found.')
        
        network = Network(**updated_network)

        return jsonify({
            'message': 'Message updated successfully.',
            'network': network.to_json()
        }), 200
    
    except Exception as e:
        current_app.logger.error('Error while updating network %s: %s', slug, e)
        raise e

@net_bp.route('/remove/<string:slug>', methods=['DELETE'])
@jwt_required()
def remove_network(slug: str) -> Tuple[Dict[str, Any], int]:
    """
    Endpoint to remove network.

    Args
        slug: unique identifier for network

    Returns 
        Tuple[Dict[str, Any], int]: json representation, status code
    """
    try:
        deleted_network = networks.find_one_and_delete({ 'slug': slug })

        if not deleted_network:
            abort(404, 'Network not found.')

        return jsonify({ 'message': 'Network deletion successful.' }), 200

    except Exception as e:
        current_app.logger.error('Error while removing network %s: %s', slug, e)
        raise e