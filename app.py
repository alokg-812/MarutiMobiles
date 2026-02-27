import os
from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db, User, Role

# --------------------venv\Scripts\activate
# Login Manager setup
# --------------------
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# --------------------
# App Factory
# --------------------
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from routes import main_bp
    from auth import auth_bp
    from admin import admin_bp
    from customer import customer_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(customer_bp, url_prefix='/customer')

    # Initialize database & seed data
    with app.app_context():
        db.create_all()
        os.makedirs(app.config.get('UPLOAD_FOLDER', 'uploads'), exist_ok=True)
        seed_roles_and_admin()

    return app


# --------------------
# Seeding Logic
# --------------------
def seed_roles_and_admin():
    # Create roles if they don't exist
    if not Role.query.first():
        db.session.add_all([
            Role(name='admin'),
            Role(name='customer')
        ])
        db.session.commit()
        print("✅ Roles created")

    # Read admin credentials SAFELY
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_email or not admin_password:
        print("⚠️ ADMIN_EMAIL or ADMIN_PASSWORD not set. Skipping admin creation.")
        return

    admin_role = Role.query.filter_by(name='admin').first()

    if not User.query.filter_by(email=admin_email).first():
        admin = User(
            full_name="Admin",
            email=admin_email,
            phone="9140242204",
            role_id=admin_role.id
        )
        admin.set_password(admin_password)
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created")
    else:
        print("ℹ️ Admin user already exists")

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
