def service_get_postings_by_token(token, en_index, fr_index):
    postings = en_index.get(token)
    if postings == None: # not in en_index
        postings = fr_index.get(token)
    # regulate output
    if postings == None:
        postings = []
    return postings


def service_bubble_sort(lst_dict, ref_key):
    for p in range(0, len(lst_dict)-1):
        for i in range(0, len(lst_dict)-1-p):
            if lst_dict[i].get(ref_key) < lst_dict[i+1].get(ref_key):
                temp = lst_dict[i]
                lst_dict[i] = lst_dict[i+1]
                lst_dict[i+1] = temp


def service_get_ele_by_attr(list, attr_name, target):
    result = None
    for ele in list:
        if ele.get(attr_name) == target:
            result = ele
            break
    return result


def service_get_theme_by_token(token, dict_theme):
    target_theme = None
    for theme, lst_tokens in dict_theme.items():
        if token in lst_tokens:
            target_theme = theme
            break
    return target_theme
