from project.utils.mongo import fetch_config


def generate_resource_levels(cfg=None):
    """Генерация resource_levels"""
    if cfg is None:
        cfg = fetch_config()

    resourse_names = sorted(cfg["resource_ids"].keys())
    return {x: 1 for x in resourse_names}


def generate_resource_stages(cfg=None):
    """Генерация resource_stages"""
    if cfg is None:
        cfg = fetch_config()

    resourse_names = sorted(cfg["resource_ids"].keys())
    return {x: 0 for x in resourse_names}
