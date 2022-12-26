from django.core.exceptions import ValidationError
import os


# NOT USING CURRENTLY
def allow_only_images_validator(value):
    ext = os.path.splitext(value.name)[1]  # image-name.jpg
    valid_extensions = ['.png', '.jpg', '.jpeg']
    if not ext.lower() in valid_extensions:
        return ValidationError("Unsupported file extension. Allowed extensions: "
                               + str(valid_extensions))
        # raise ValidationError("Unsupported file extension. Allowed extensions: "
        #                       + str(valid_extensions))
