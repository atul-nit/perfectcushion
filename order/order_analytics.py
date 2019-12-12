from django.db import connection

def get_order_list():
    result = []
    with connection.cursor() as cursor:
        cursor.execute('SELECT id, total, email_address, created FROM "Order"')
        for order in cursor:
            row_data = list(order)
            order_date = row_data[3]
            row_data[3] = str(order_date)
            result.append(row_data)
    return {"result": result}

def get_order_three_months_old():
    result = []
    with connection.cursor() as cursor:
        cursor.execute('SELECT id, total, email_address, created FROM "Order" where created <= date("now", "-3 month")')
        for order in cursor:
            result.append(order)
    return {"result": result}
