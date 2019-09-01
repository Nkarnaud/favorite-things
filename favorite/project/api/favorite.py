# -*- coding: utf-8 -*-
import logging


from flask import Blueprint, jsonify, request, render_template
from project.models.models import Favorite, Category, AuditLog
from project import db
from flask import current_app
from project.logsfile import init_logs
from sqlalchemy import exc


# Blueprint initialization
favorite_blueprint = Blueprint('favorite', __name__, template_folder='../templates')
log = init_logs('favourite')
print(log)

# Sanity test
@favorite_blueprint.route('/favorite/ping', methods=['GET'])
def ping_pong():
    logs = log.info('Sanity Test: %s', (request.path))
    logg = str(current_app.logger.info('Sanity test'))
    print(log)
    return jsonify({
        'status': 'success',
        'log': logg,
        'message': 'pong!'
    })


# Create favorite thinks in the database
@favorite_blueprint.route('/favorite/create', methods=['POST'])
def create_favorite():
    # get post data
    trace = none
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400
    title = post_data.get('title')
    category_id = Category.query.filter_by(category_name=post_data.get('category')).id
    ranking = post_data.get('ranking')
    try:
        # fetch the favorite think
        favorite = Favorit.query.filter(ranking=ranking, category_id=category_id).first()
        if not favorite:
            new_favorite(
                title = title,
                category_id = category_id,
                ranking = ranking
            )
            if post_data.get('description'):
                if len(post_data.get('description'))< 10:
                    raise Exception("Description too short")
                new_favorite.description = post_data.get('description')
            if post_data.get('metadata'):
                new_favorite.meta_data = post_data.get('metadata')
            db.session.add(new_favorite)
            log = AuditLog(
              logger = logger.info('Your favorite thing was added.'), 
              level = logger.leve(),
            )
            db.session.add(log)
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = 'Your favorite thing was added.'
            return jsonify(response_object), 201
        else:
            log = AuditLog(
              logger = logger.warning('There exist a ranking with this same category.'), 
              level = logger.leve(),
            )
            db.session.add(log)
            db.session.commit()
            response_object['message'] = 'There exist a ranking with this same category.'
            return jsonify(response_object), 401
    except Exception as e:
        log = AuditLog(
              logger = logger.error(e), 
              level = logger.leve(),
            )
        db.session.add(log)
        db.session.commit()
        return jsonify(response_object), 400


# Get favorite things details from the database
@favorite_blueprint.route('/favorite/<id>', methods=['GET'])
def Favorite_detaile(id):
    """Get single favorite things details"""
    response_object = {
        'status': 'fail', 
        'message': 'Invalid payload.'
    }
    favorite = Favorite.query.filter_by(id=id).first()
    try:
        if favorite:
            response_object = {
                'status': 'success',
                'data': {
                    'id': favorite.id,
                    'title': favorite.title,
                    'category': Category.query.filter_by(id=favorite.category_id),
                    'ranking': favorite.ranking,
                    'metadata': favorite.meta_data,
                    'create_data': favorite.create_data,
                    'modified_data': favorite.modified_data,
                }
            }
            log = AuditLog(
              logger = logger.info('Favorite details fetch.'), 
              level = loger.leve(),
            )
            db.session.add(log)
            db.session.commit()
            return jsonify(response_object), 201
        else:
            log = AuditLog(
              logger = logger.warning('Favorite things does not exists..'), 
              level = logger.leve(),
            )
            db.session.add(log)
            db.session.commit()
            response_object ={
                'status' : 'fail',
                'message': 'Favorite things does not exists.'}
            return jsonify(response_object), 401
    except exc.IntegrityError as e:
        log = AuditLog(
              logger = logger.error('Favorite things does not exists..'), 
              level = logger.leve(),
            )
        db.session.add(log)
        db.session.commit()
        return jsonify(response_object), 400


# List Favorite things in the database
@favorite_blueprint.route('/favorite/lists', methods=['GET'])
def get_all_favorite():
    # This function provide the list of all favorite in the system
        response_object = {
            'status': 'success',
            'data': {
                'users': [favorite.to_json() for favorite in Favorite.query.all()]
            }
        }
        log = AuditLog(
              logger = logger.info('List of favorite user in the system.'), 
              level = logger.leve(),
            )
        db.session.add(log)
        db.session.commit()
        return jsonify(response_object), 201


# Update favorite things in the database
@favorite_blueprint.route('/favorite/update/<id>', methods=['PUT'])
def update_favorite(id):
    """To update a favorite things in the systeme"""
    response_object = {
        'status': 'fail',
        'message': 'Sorry. The favorite things does not exists'
    }
    post_data = request.get_json()
    try:
        favorite = Favorite.query.get(id)
        if not favorite:
            log = AuditLog(
              logger = logger.warning('The favorit thing Id to update is wrong.'), 
              level = logger.leve(),
            )
            db.session.add(log)
            db.session.commit()
            return jsonsify(response_object), 404
        else:
            favorite.title = post_data.get('title')
            favorite.category_id = Category.query.filter_by(category_name=post_data.get('category')).id
            favorite.ranking = post_data.get('ranking')
            favorite.meta_data = post_data.get('metadata')
            favorite.modified_date = datetime.datetime.utcnow()
            log = AuditLog(
              logger = logger.info('Favorite things was updated.'), 
              level = logger.leve(),
            )
            db.session.add(log)
            db.session.commit()
            response_object = {'status': 'Modified', 
                'message': 'The Favorite thing has been update'}
            return response_object, 201
    except Exception as e:
        log = AuditLog(
              logger = logger.error(e), 
              level = logger.leve(),
            )
        db.session.add(log)
        db.session.commit()
        return jsonify({"message": str(e)}), 401


# Create category of favorite things in the database
@favorite_blueprint.route('/favorite/create_category', methods=['POST'])
def create_category():
    # get post data
    trace = none
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400
    category_name = post_data.get('category_name')
    try:
        # fetch the favorite think
        cat = Category.query.filter_by(category_name=category_name).first()
        if not cat:
            new_cat(
                category_name = category_name
            )
            db.session.add(new_cat)
            log = AuditLog(
              logger = logger.info('A new category was added.'), 
              level = logger.leve(),
            )
            db.session.add(log)
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = 'A new category was added.'
            return jsonify(response_object), 201
        else:
            log = AuditLog(
              logger = logger.warning('This category already exit.'), 
              level = logger.leve(),
            )
            db.session.add(log)
            db.session.commit()
            response_object['message'] = 'This category already exit.'
            return jsonify(response_object), 401
    except Exception as e:
        log = AuditLog(
              logger = logger.error(e), 
              level = logger.leve(),
            )
        db.session.add(log)
        db.session.commit()
        return jsonify(response_object), 400


# Provide the list ofr log activities in the database.
@favorite_blueprint.route('/favorite/logs', methods=['GET'])
def get_logs():
    # This function provide the list of all favorite in the system
        response_object = {
            'status': 'success',
            'data': {
                'users': [logs.to_json() for logs in AuditLog.query.all()]
            }
        }
        return jsonify(response_object), 201