from re import findall


def parse(string):
    if string:
        template_maze_in_action = r'(Mob|Location|Boss)(\d+)?_(exp)?(\w+)_tm(.+)$'
        parsed = findall(template_maze_in_action, string)
        template_maze_exit = r'(Hatch)_tm(.+)'
        if len(parsed):
            return list(parsed[0])
        else:
            return list(findall(template_maze_exit, string)[0])
    return None


def get_action_list(raw_list):
    formatted_list = []
    for item in raw_list:
        if isinstance(item, str):
            formatted_list.append([item, f'- Monster {item}'])
        else:
            item_key = list(item.keys())[0]
            formatted_list.append([item_key, f'- Exit to location {item_key}'])
    return formatted_list
