import hashlib
from database.database import get_db
import config


class UserService:
    # TODO Přidat metody, které budou potřeba v rámci komunikace (až během implementace stránek)
    @staticmethod
    def get_all():
        db = get_db()
        sql_query = "SELECT * FROM users "
        return db.execute(sql_query).fetchall()

    @staticmethod
    def insert_user(username, name, last_name, email, password):
        db = get_db()
        # Odkomentovat hash funkci a přepsat password na hashed_password, až budeme mít upravená data v databázi, aby to prošlo
        hashed_password = hashlib.sha256(f'{password}{config.PASSWORD_SALT}'.encode())
        #print(hashed_password.hexdigest())
        db.execute(
            'INSERT INTO users (username, name, last_name, email, password) VALUES (?, ?, ?, ?, ?)',
            [username, name, last_name, email, hashed_password.hexdigest()]
        )
        db.commit()

    @staticmethod
    def verify(username, password):
        db = get_db()
        # Odkomentovat hash funkci a přepsat password na hashed_password, až budeme mít upravená data v databázi, aby to prošlo
        hashed_password = hashlib.sha256(f'{password}{config.PASSWORD_SALT}'.encode())
        #print(hashed_password.hexdigest())
        sql = '''
            SELECT users.id, users.username, roles.name AS role
            FROM users
            JOIN roles ON users.role_id = roles.id
            WHERE username = ? AND password = ?
        '''
        args = [username, hashed_password.hexdigest()]
        user = db.execute(sql, args).fetchone()
        if user:
            return user
        else:
            return None

    @staticmethod
    def get_user_by_id(id):
        db = get_db()
        sql_query = """
            SELECT users.id, users.username, users.name, users.last_name, users.email, users.phone_number, users.created_date,
            roles.id AS role_id, roles.name AS role_name, roles.description AS role_description
            FROM users
            JOIN roles ON users.role_id = roles.id
            WHERE users.id == ?
        """
        args = [id]
        user = db.execute(sql_query, args).fetchone()
        if user:
            return user
        else:
            return None

    @staticmethod
    def alter_profile_by_id(id, name, last_name, email, phone_number):
        db = get_db()
        sql_query = '''
            UPDATE users
            SET name = ?, last_name = ?, email = ?, phone_number = ?
            WHERE id = ?
        '''
        args = [name, last_name, email, phone_number, id]
        db.execute(sql_query, args)
        db.commit()

    @staticmethod
    def alter_user_role_by_id(id, username, role, phone_number ,salary):
        db = get_db()
        sql_query = '''
            UPDATE users
            SET role_id = ?, phone_number = ?, salary_per_hour = ?
            WHERE id = ? AND username = ?
        '''
        args = [role, phone_number, salary, id, username]
        db.execute(sql_query, args)
        db.commit()

    @staticmethod
    def get_roles():
        db = get_db()
        sql_query = "SELECT * FROM roles"
        return db.execute(sql_query).fetchall()

    @staticmethod
    def get_all_employees_by_role_id(role_id):
        db = get_db()
        sql_query = "SELECT * FROM users WHERE users.role_id = ?"
        args = [role_id]
        return db.execute(sql_query, args).fetchall()