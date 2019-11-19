from django.db import connection

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