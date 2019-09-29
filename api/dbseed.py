from models import user_datastore, Config, Role


def make_db_seed(db):
    print("== Seeding database")
    db.session.begin(subtransactions=True)
    try:
        seed_config(db)
        seed_roles(db)
    except:  # noqa: E722
        db.session.rollback()
        raise


def seed_roles(db):
    print("++ Seeding roles")
    role_usr = Role()
    role_usr.name = "user"
    role_usr.description = "Simple user"

    role_adm = Role()
    role_adm.name = "admin"
    role_adm.description = "Admin user"

    db.session.add(role_usr)
    db.session.add(role_adm)
    db.session.commit()


def seed_users(db):
    print("++ Seeding users")
    role_usr = Role()
    role_usr.name = "user"
    role_usr.description = "Simple user"

    role_adm = Role()
    role_adm.name = "admin"
    role_adm.description = "Admin user"

    db.session.add(role_usr)
    db.session.add(role_adm)

    user_datastore.create_user(
        email="dashie@sigpipe.me", password="fluttershy", name="toto", timezone="UTC", roles=[role_adm]
    )
    db.session.commit()
    return


def seed_config(db):
    print("++ Seeding config")
    a = Config(app_name="My reel2bits instance")
    a.app_description = """This is a reel2bits instance"""
    db.session.add(a)
    db.session.commit()
    db.session.commit()
    # Bug, two commit necessary
