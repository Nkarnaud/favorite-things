# customer/project/config.py
# -*- coding: utf-8 -*-
import os


# Base configuration
class BaseConfig:
    """Base configuration"""
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 13


# Developpement configuration
class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG_TB_ENABLED = True
    SQLALCHEMY_ECHO = True  
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') 


# Production Configuration
class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG_TB_ENABLED = True
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}