#!/usr/bin/python3
"""Celery Task Module"""
from typing import List
from celery import Celery
from api.core.config import Config
from api.v1.mail import mail, create_message
from asgiref.sync import async_to_sync

c_app = Celery()

c_app.config_from_object(Config)


@c_app.task
def send_email(recipients: List[str], subject: str, body: str):
    """Send email"""
    message = create_message(recipients=recipients, subject=subject, body=body)
    async_to_sync(mail.send_message)(message)
    print("Email sent successfully")
