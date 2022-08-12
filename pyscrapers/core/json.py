def find_paths(element, json):
    paths = []
    to_search = [("", json)]
    while to_search:
        path, current = to_search.pop()
        did = False
        if isinstance(current, str):
            did = True
            if current == element:
                paths.append(path)
        if isinstance(current, dict):
            did = True
            for k, v in current.items():
                if k == element:
                    paths.append(path + f"[{k}]")
                to_search.append((path + f"[{k}]", v))
        if isinstance(current, list):
            did = True
            for i, x in enumerate(current):
                to_search.append((path + f"[{i}]", x))
        if isinstance(current, (type(None), bool, int, float)):
            did = True
        assert did, f"{current} of type {type(current)}"
    return paths
