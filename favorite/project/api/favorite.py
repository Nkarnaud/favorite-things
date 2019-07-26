# -*- coding: utf-8 -*-

import logging
from flask import Blueprint, jsonify, request, render_template
from project.models.models import Favorite, Category, AuditLog
from project import db
from sqlalchemy import exc

favorite_blueprint = Blueprint('favorite', __name__, template_folder='../templates')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@favorite_blueprint.route('/friends/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

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
                title = title
                category_id = category_id
                ranking = ranking
            )
            if post_data.get('description'):
                new_favorite.metadata = post_data.get('description')
            if post_data.get('metadata'):
                new_favorite.metadata = post_data.get('metadata')
            db.session.add(new_favorite)
            log = AuditLog(
              logger = logger.info('Your favorite thing was added.'), 
              level = loger.leve(),
            )
            db.session.add(log)
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = 'Your favorite thing was added.'
            return jsonify(response_object), 201
        else:
            log = AuditLog(
              logger = logger.warning('There exist a ranking with this same category.'), 
              level = loger.leve(),
            )
            db.session.add(log)
            db.session.commit()
            response_object['message'] = 'There exist a ranking with this same category.'
            return jsonify(response_object), 401
    except Exception as e:
        log = AuditLog(
              logger = logger.error(e), 
              level = loger.leve(),
            )
            db.session.add(log)
            db.session.commit()
        return jsonify(response_object), 400

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
                    'metadata': favorite.metadata,
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
              level = loger.leve(),
            )
            db.session.add(log)
            db.session.commit()
            response_object ={
                'status' : 'fail',
                'message': 'Favorite things does not exists.'}
            return jsonify(response_object), 401
    except exc.IntegrityError as e:
        db.session.rollback()
        log = AuditLog(
              logger = logger.error('Favorite things does not exists..'), 
              level = loger.leve(),
            )
            db.session.add(log)
            db.session.commit()
        return jsonify(response_object), 400

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
              level = loger.leve(),
            )
            db.session.add(log)
            db.session.commit()
        return jsonify(response_object), 201

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
              level = loger.leve(),
            )
            db.session.add(log)
            db.session.commit()
            return jsonsify(response_object), 404
        else:
            favorite.title = post_data.get('title')
            favorite.category_id = Category.query.filter_by(category_name=post_data.get('category')).id
            favorite.ranking = post_data.get('ranking')
            favorite.metadata = post_data.get('metadata')
            favorite.modified_date = datetime.datetime.utcnow()
            log = AuditLog(
              logger = logger.info('Favorite things was updated.'), 
              level = loger.leve(),
            )
            db.session.add(log)
            db.session.commit()
            response_object = {'status': 'Modified', 
                'message': 'The Favorite thing has been update'}
            return response_object, 201
    except Exception as e:
        db.session.rollback()
        log = AuditLog(
              logger = logger.error(e), 
              level = loger.leve(),
            )
            db.session.add(log)
            db.session.commit()
        return jsonify({"message": str(e)}), 401

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
              level = loger.leve(),
            )
            db.session.add(log)
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = 'A new category was added.'
            return jsonify(response_object), 201
        else:
            log = AuditLog(
              logger = logger.warning('This category already exit.'), 
              level = loger.leve(),
            )
            db.session.add(log)
            db.session.commit()
            response_object['message'] = 'This category already exit.'
            return jsonify(response_object), 401
    except Exception as e:
        log = AuditLog(
              logger = logger.error(e), 
              level = loger.leve(),
            )
            db.session.add(log)
            db.session.commit()
        return jsonify(response_object), 400
