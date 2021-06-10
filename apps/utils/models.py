from django.db.models.expressions import Func


class UpdateJSONValue(Func):

    function = "jsonb_set"
    template = "%(function)s(%(expressions)s, '{\"%(keyname)s\"}','\"%(new_value)s\"', %(create_missing)s)"
    arity = 1

    def __init__(
        self,
        expression: str,
        keyname: str,
        new_value: str,
        create_missing: bool = False,
        **extra,
    ):
        super().__init__(
            expression,
            keyname=keyname,
            new_value=new_value,
            create_missing="true" if create_missing else "false",
            **extra,
        )


class InsertJSONValue(Func):

    function = "jsonb_insert"
    template = "%(function)s(%(expressions)s, '{\"%(keyname)s\"}','\"%(new_value)s\"', %(create_missing)s)"
    arity = 1

    def __init__(
        self,
        expression: str,
        keyname: str,
        new_value: str,
        create_missing: bool = False,
        **extra,
    ):
        super().__init__(
            expression,
            keyname=keyname,
            new_value=new_value,
            create_missing="true" if create_missing else "false",
            **extra,
        )
