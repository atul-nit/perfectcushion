from django.db import connection
from .utilities.merge import mergeSort

actions_for_list = ['data_from_table', 'prepare_result' 'send_response']

class ActionCheckList:
    def __init__(self):
        self.check_list = []

    def push_action(self, action):
        self.check_list.append(action)

    def pop_action(self):
        return self.check_list.pop()

    def show_check_list(self):
        return self.check_list

def check_actions_completed(actions_object):
    if actions_object.check_list == actions_for_list:
        return True
    else:
        return False

def get_product_list_name():
    result = []
    action_obj = ActionCheckList()
    with connection.cursor() as cursor:
        # Fetch data from table
        cursor.execute('SELECT id, name FROM shop_product')
        action_obj.push_action('data_from_table')
        for product in cursor:
            result.append(product)
        action_obj.push_action('prepare_result')
        action_obj.push_action('send_response')

        # Check all actions completed
        actions_completed = check_actions_completed(action_obj)
    return {"result": result, "actions_completed": actions_completed}
    # return result

def get_all_ids():
    all_ids = []
    with connection.cursor() as cursor:
        cursor.execute('SELECT id from shop_product')
        for row in cursor:
            all_ids.append(row[0])
    return all_ids

def get_all_products():
    result = []
    product_ids = get_all_ids()
    ids = mergeSort(product_ids, 0, len(product_ids) - 1)
    with connection.cursor() as cursor:
        cursor.execute('SELECT id, name, slug, price, stock FROM shop_product where id in (%s)' %(', '.join(str(id) for id in ids)))
        for product in cursor:
            result.append(product)
    actions_completed = True
    return {"result": result, "actions_completed": actions_completed}


