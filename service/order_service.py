from database.database import get_db


class OrderService:

    @staticmethod
    def get_items_for_user(user_id):
        db = get_db()
        sql_query = 'SELECT * FROM cart_items WHERE user_id = ? ORDER BY created_date ASC'
        arguments = [user_id]

        return db.execute(sql_query, arguments).fetchall()

    @staticmethod
    def add_item(item_id, user_id, date_to_delivery, date_to_pickup, with_service):
        db = get_db()
        sql_query = 'INSERT INTO cart_items (item_id, user_id, date_to_delivery, date_to_pickup, with_service) VALUES (?, ?, ?, ?, ?)'
        arguments = [item_id, user_id, date_to_delivery, date_to_pickup, with_service]
        db.execute(sql_query, arguments)
        db.commit()

    @staticmethod
    def delete_item_by_index(user_id, index):
        db = get_db()
        # delete item via user id on the given row and thus keep the order of items by deleting nth row given by index
        sql_query = 'DELETE FROM cart_items WHERE user_id = ? AND created_date = (SELECT created_date FROM cart_items WHERE user_id = ? ORDER BY created_date ASC LIMIT 1 OFFSET ?);'
        arguments = [user_id, user_id, index]
        db.execute(sql_query, arguments)
        db.commit()

    @staticmethod
    def delete_cart_by_user(user_id):
        db = get_db()
        # delete item via user id on the given row and thus keep the order of items by deleting nth row given by index
        sql_query = 'DELETE FROM cart_items WHERE user_id = ?;'
        arguments = [user_id]
        db.execute(sql_query, arguments)
        db.commit()

    @staticmethod
    def update_item_service_by_index(user_id, index, service):
        db = get_db()
        sql_query = ('UPDATE cart_items SET with_service = ? WHERE user_id = ? AND created_date = (SELECT created_date FROM cart_items '
                     'WHERE user_id = ? ORDER BY created_date ASC LIMIT 1 OFFSET ?);')
        arguments = [service, user_id, user_id, index]
        db.execute(sql_query, arguments)
        db.commit()

    @staticmethod
    def update_given_employee_on_order(employee_id, order_id):
        db = get_db()
        sql_query = '''
            UPDATE main_orders SET given_employee = ? WHERE main_orders.id = ?;
        '''
        arguments = [employee_id, order_id]
        db.execute(sql_query, arguments)
        db.commit()