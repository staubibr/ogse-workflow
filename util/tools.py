
def get_value(json, props):
    if len(props) == 0:
        return json

    props = props if type(props) == list else [props]
    curr = json

    for p in props:
        if p not in curr:
            raise Exception("property {0} not found in experiment.".format(p))

        curr = curr[p]

    return curr


def traverse(json, func):
    if isinstance(json, dict):
        return {k: traverse(v, func) for k, v in json.items()}

    elif isinstance(json, list) or isinstance(json, tuple):
        return [traverse(v, func) for v in json]

    else:
        return func(json)


def replace_tags(json, tag, func):
    def wrap(v):
        return func(v.lstrip(tag).lstrip(":")) if isinstance(v, str) and v.startswith(tag) else v

    return traverse(json, wrap)
