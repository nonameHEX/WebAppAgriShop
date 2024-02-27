from database.database import get_db


class ReservationService:
    @staticmethod
    def get_all():
        db = get_db()
        sql_query = '''
            SELECT
                main_orders.*,
                users.name AS user_name,
                users.last_name AS user_last_name,
                order_state.name AS order_state_name,
                order_machine.machine_id as machine_id,
                machines.price_per_day * (julianday(main_orders.date_to_pickup) - julianday(main_orders.date_to_delivery)) AS price_per_all_day
            FROM
                main_orders
            LEFT JOIN
                users ON main_orders.creator = users.id
            LEFT JOIN
                order_state ON main_orders.state = order_state.id
            LEFT JOIN
                order_machine ON main_orders.id = order_machine.order_id
            LEFT JOIN
                machines ON order_machine.machine_id = machines.id
            GROUP BY
                main_orders.id
        '''
        return db.execute(sql_query).fetchall()

    @staticmethod
    def get_by_order_id(order_id):
        db = get_db()
        sql_query = '''
            SELECT
                main_orders.*,
                order_state.name AS order_state_name,
                us.name AS user_name,
                us.last_name AS user_last_name,
                us.email AS user_email,
                us.phone_number AS phone_number
            FROM
                main_orders
            LEFT JOIN
                users AS us ON main_orders.creator = us.id
            LEFT JOIN
                order_state ON main_orders.state = order_state.id
            WHERE
                main_orders.id = ?
        '''
        args = [order_id]
        order = db.execute(sql_query, args).fetchone()
        if order:
            return order
        else:
            return None

    @staticmethod
    def get_by_order_machine_id(order_id):
        db = get_db()
        sql_query = '''
            SELECT
                order_machine.with_service AS with_service,
                order_machine.machine_id as machine_id,
                machines.name AS machine_name,
                machines.description AS machine_description,
                machines.image AS machine_image,
                machine_types.name AS machine_type,
                tech.name AS technician_name,
                tech.last_name AS technician_last_name,
                tech.phone_number AS technician_phone_number,
                machines.price_per_day * (julianday(main_orders.date_to_pickup) - julianday(main_orders.date_to_delivery)) AS price_per_all_day,
                CASE
                    WHEN main_orders.given_employee IS NOT NULL THEN tech.salary_per_hour * 8 * (julianday(main_orders.date_to_pickup) - julianday(main_orders.date_to_delivery))
                    ELSE NULL
                END AS salary_for_worker
            FROM
                main_orders
            LEFT JOIN
                order_machine ON main_orders.id = order_machine.order_id
            LEFT JOIN
                machines ON order_machine.machine_id = machines.id
            LEFT JOIN
                machine_types ON machines.type = machine_types.id
            LEFT JOIN
                users AS tech ON main_orders.given_employee = tech.id
            WHERE
                main_orders.id = ?
        '''
        args = [order_id]
        machines = db.execute(sql_query, args).fetchall()
        if machines:
            return machines
        else:
            return None

    @staticmethod
    def get_by_employee_all(worker_id):
        db = get_db()
        args = []
        sql_query = '''
        SELECT
            main_orders.*,
            order_state.name AS order_state_name,
            order_machine.machine_id as machine_id
        FROM 
            main_orders 
        LEFT JOIN
            order_state ON main_orders.state = order_state.id
        LEFT JOIN
            order_machine ON main_orders.id = order_machine.order_id
        WHERE main_orders.given_employee = ? 
        GROUP BY
                main_orders.id
        '''

        args.append(worker_id)
        return db.execute(sql_query, args).fetchall()

    @staticmethod
    def get_by_user_all(user_id):
        db = get_db()
        args = []
        sql_query = '''
            SELECT
                main_orders.*,
                order_machine.machine_id as machine_id,
                machines.price_per_day * (julianday(main_orders.date_to_pickup) - julianday(main_orders.date_to_delivery)) AS price_per_all_day,
            CASE 
                WHEN main_orders.given_employee IS NOT NULL THEN users.salary_per_hour * 8 * (julianday(main_orders.date_to_pickup) - julianday(main_orders.date_to_delivery))
                ELSE NULL 
            END AS salary_for_worker,
                order_state.name AS order_state_name
            FROM 
                main_orders 
            LEFT JOIN
                order_state ON main_orders.state = order_state.id
            LEFT JOIN
                order_machine ON main_orders.id = order_machine.order_id
            LEFT JOIN
                machines ON order_machine.machine_id = machines.id
            LEFT JOIN
                users ON main_orders.given_employee = users.id
            WHERE main_orders.creator = ? 
            GROUP BY
                main_orders.id
            '''

        args.append(user_id)
        return db.execute(sql_query, args).fetchall()

    @staticmethod
    def create_order(dateFrom, dateTo, address, user_id):
        db = get_db()
        sql_query = 'INSERT INTO main_orders (date_to_delivery, date_to_pickup, address, state, creator) VALUES (?, ?, ?, ?, ?)'
        arguments = [dateFrom, dateTo, address, 1, user_id]
        db.execute(sql_query, arguments)
        db.commit()

    @staticmethod
    def get_user_last_order(user_id):
        db = get_db()
        sql_query = 'SELECT id FROM main_orders WHERE (creator = ?) ORDER BY id DESC LIMIT 1'
        args = [user_id]
        return db.execute(sql_query, args).fetchall()

    @staticmethod
    def add_machine_to_order(machine_id, order_id, service_status):
        db = get_db()
        sql_query = 'INSERT INTO order_machine (order_id, machine_id, with_service) VALUES (?, ?, ?)'
        arguments = [order_id, machine_id, service_status]
        db.execute(sql_query, arguments)
        db.commit()

    @staticmethod
    def update_order_state(order_id, state):
        db = get_db()
        sql_query = 'UPDATE main_orders SET state = ? WHERE main_orders.id = ?'
        arguments = [state, order_id]
        db.execute(sql_query, arguments)
        db.commit()