from django.urls import path
from .models import Post


class RestlessConfig:
    types = []
    """
    @var types
    """

    def __init__(self):
        with open(BASE_DIR/"restless/structure.yaml") as fh:
            structure = json.load(fh)
        if 'objects' not in structure.keys():
            raise NameError(msg="Structure missing key 'objects'")
        self.types = structure.keys()


def get_object(object_type: str):
    return lambda **kwargs: Post.get(**kwargs)


def _generate_paths(structure: dict):
    try:
        return [(
            description[url],
            lambda z: get_object(description[name])
        ) for (name, description) in structure.items()]
    except Exception as e:
        raise e


def generate_paths():
    with open(BASE_DIR/"restless/structure.yaml") as fh:
        structure = json.load(fh)
    return _generate_paths(structure['objects'])
