from flask import Blueprint, render_template, redirect, url_for, request, flash

auth=Blueprint("auth", __name__, template_folder="templates/auth")

from app.auth import routes 