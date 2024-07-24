from app.auth.controllers import AuthController
from .controllers import AdminController
from flask import Blueprint, request
from ..utils.access_handler import admin_required

admin = Blueprint('site_admin', __name__)


@admin.route("/refresh")
@admin_required(refresh=True)
def admin_refresh_access():
    return AdminController.admin_refresh_access()


@staticmethod
@admin.route('/register', methods=['POST'])
def admin_register():
    return AdminController.admin_register()


@admin.route('/login', methods=['POST'])
def admin_login():
    return AdminController.admin_login()


@admin.route('/dashboard')
@admin_required()
def admin_dashboard():
    return AdminController.admin_dashboard()


@admin.route('/dashboard/data-with-date')
@admin_required()
def admin_dashboard_date():
    return AdminController.admin_dashboard()


@admin.route('/get-client-details')
@admin_required()
def get_client_details():
    return AdminController.get_client_details()


@admin.route('/get-service-price', methods=['POST'])
@admin_required()
def get_service_price():
    return AdminController.get_service_price


@admin.route('/set-service-price', methods=['POST'])
@admin_required()
def set_service_price():
    return AdminController.set_service_price()


@admin.route('/wallet-logs', methods=['POST'])
@admin_required()
def wallet_logs():
    return AdminController.wallet_logs()


@admin.route('/get-user-role-distribution')
@admin_required()
def user_role_distribution():
    return AdminController.user_role_distribution()
