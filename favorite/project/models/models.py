# -*- coding: utf-8 -*-
import datetime
from flask import current_app
from project import db


# Favorite model
class Favorite(db.Model):
    __tablename__ = "Favorite"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    categorie_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    title = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(256), nullable=True)
    ranking = db.Column(db.String(128), nullable=False)
    meta_data = db.Column(db.String(128), unique=True, nullable=True)
    create_date = db.Column(db.DateTime, nullable=False)
    modified_date = db.Column(db.DateTime, nullable=False)
    priority = db.relationship('Category', foreign_keys=categorie_id)
    
    # Class constructor 
    def __init__(self, title, category_id, ranking):
        self.title = title
        self.category_id = category_id
        self.ranking = ranking 
        self.create_date = datetime.datetime.utcnow()
        self.modified_date = datetime.datetime.utcnow()
    
    # Returning class attribute in a json format
    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'category_id': self.category_id,
            'ranking': self.ranking,
            'metadata': self.meta_data,
            'create_data': self.create_date,
            'modified_data': self.modified_date,
        }


# Category table
class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(32), unique=True, nullable=True)
    
    # Class constructor
    def __init__(self, category_name):
        self.category_name = category_name
    
    # Reture class attribute in json
    def to_json(self):
        return{
            'id': self.id,
            'category_name':self.category_name
        }


# Audit log table
class AuditLog(db.Model):
    __tablename__ = "audit_log"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    logger = db.Column(db.String(254))
    level = db.Column(db.String(254))
    msg = db.Column(db.String(254))
    create_data = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    # Class constuctor
    def __init__(self, logger=None, level=None, msg =None):
        self.logger = logger
        self.level = level
        self.msg = msg
    
    # Returning class attribute in json format
    def to_json(self):
        return{
            "id": self.id,
            "logger": self.logger,
            "level": self.level,
            "msg": self.msg,
            "create_data": self.create_data
        }
