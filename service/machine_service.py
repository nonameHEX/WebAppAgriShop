import base64

from database.database import get_db


class MachineService:
    @staticmethod
    def get_all():
        db = get_db()
        sql_query = "SELECT * FROM machines"
        return db.execute(sql_query).fetchall()

    @staticmethod
    def get_machine(id):
        db = get_db()
        arguments = []
        sql_query = "SELECT * FROM machines WHERE id = ?"
        arguments.append(id)
        return db.execute(sql_query, arguments).fetchall()

    @staticmethod
    def get_filterMachines(priceFrom,priceTo,machineName,dateTo,dateFrom):

        db = get_db()

        # SQL dotaz pro vyhledávání strojů
        sql_query = """
        SELECT * 
        FROM machines 
        WHERE 
            price_per_day BETWEEN ? AND ? 
            AND name LIKE ? 
            AND id NOT IN (
                SELECT machine_id 
                FROM order_machine 
                JOIN main_orders ON main_orders.id = order_machine.order_id
                WHERE (main_orders.date_to_delivery BETWEEN ? AND ?) OR (main_orders.date_to_pickup BETWEEN ? AND ?)
            )
        """

        # Parametry dotazu
        machine_name_param = f"%{machineName}%" if machineName else '%'
        arguments = [priceFrom or 0, priceTo or 10000000, machine_name_param, dateFrom, dateTo, dateFrom, dateTo]

        # Vykonání dotazu a vrácení výsledků
        return db.execute(sql_query, arguments).fetchall()

    @staticmethod
    def get_machine_types():
        db = get_db()
        sql_query = "SELECT * FROM machine_types"
        return db.execute(sql_query).fetchall()

    @staticmethod
    def add_machine(name, price_per_day, type, description, image):
        db = get_db()
        file = image.read()

        # We must encode the file to get base64 string
        file = base64.b64encode(file).decode('ascii')

        db.execute('INSERT INTO machines (name, price_per_day, type, description, image) VALUES (?, ?, ?, ?, ?)',
            [name, price_per_day, type, description, file])
        db.commit()
