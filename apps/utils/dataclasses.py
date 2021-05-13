from dataclasses import dataclass, fields


def build_dataclass_from_model_instance(klass: dataclass, instance: "Model", **kwargs):
    """
    Return a dataclass from a model instance
    """
    # Get the dataclass fields
    dataclass_field_names = set(f.name for f in fields(klass))

    # Exclude given properties
    dataclass_field_names -= kwargs.keys()

    _kwargs = {field: getattr(instance, field) for field in dataclass_field_names}
    _kwargs.update(kwargs)

    return klass(**_kwargs)


def build_model_from_dataclass_instance(klass: dataclass, instance: "Model", **kwargs):
    """
    Return a dataclass from a model instance
    """
    # Get the dataclass fields
    dataclass_field_names = set(f.name for f in fields(klass))

    # Exclude given properties
    dataclass_field_names -= kwargs.keys()

    _kwargs = {field: getattr(instance, field) for field in dataclass_field_names}
    _kwargs.update(kwargs)

    return instance(**_kwargs)
