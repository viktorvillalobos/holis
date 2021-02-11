from typing import Any

from django.core import checks
from django.db import models
from django.db.models import UUIDField


class LowerCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).lower()

    def to_python(self, value: Any) -> Any:
        return super().to_python(value).lower()


def _check_field_type_is_uuid(field_instance):
    errors = []
    target_field = field_instance.target_field
    field_model_app_name = field_instance.model._meta.app_label
    field_model_name = field_instance.model.__name__
    field_name = field_instance.name
    field_path = f"{field_model_app_name}.{field_model_name}.{field_name}"

    # IMPORTANT!
    # DO NO MODIFY THIS WITHOUT PERMISSION, this is just temporal fix and it is going to be removed
    allow_field_list = [
        "catalog.ProductBranchDenylist.ext_product_branch",
        "checkout.Checkout.payment_method",
        "checkout.Checkout.user",
        "data_requests.DataRequestTriggerParameters.country",
        "shoppers.ShopperAvailabilitySchedule.shopper",
        "shoppers.ShopperLocality.city",
    ]

    error_type = checks.Error

    if field_path in allow_field_list:
        # change level to warning and do not hide this issue
        error_type = checks.Warning

    max_recursive_steps = 5

    while True:
        if max_recursive_steps < 0:
            raise RecursionError(
                f"{field_path} relationship is jumping over 6 or more times to other "
                "model fields, this needs needs review."
            )

        if isinstance(target_field, models.OneToOneField):
            target_field = target_field.target_field
        elif not isinstance(target_field, UUIDField):
            errors.append(
                error_type(
                    "The field '%s.%s' of type '%s' is not an instance of UUIDField. Provide a `to_field` argument "
                    "specifying the UUID column."
                    % (
                        target_field.model._meta.label,
                        target_field.name,
                        type(target_field),
                    ),
                    obj=field_instance,
                    id="fields.CS001",
                )
            )
            break
        else:
            break

        max_recursive_steps -= 1

    return errors


class UUIDForeignKey(models.ForeignKey):
    def __init__(self, *args, **kwargs):
        kwargs["db_constraint"] = kwargs.get("db_constraint") or False
        super().__init__(*args, **kwargs)

    def check(self, **kwargs):
        errors = super().check(**kwargs)
        errors += _check_field_type_is_uuid(self)
        return errors

    def get_attname(self):
        return f"{self.name}_uuid"
