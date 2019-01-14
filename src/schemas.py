from gwap_framework.schemas.base import BaseSchema
from schematics.types import StringType, NumberType, ListType, ModelType


class ExerciseFileInputSchema(BaseSchema):
    exercise_file_id = StringType(required=False, serialized_name='exerciseFileId')
    file_id = StringType(required=False, serialized_name='fileId')
    exercise_id = StringType(required=False, serialized_name='exerciseId')


class ExerciseInputSchema(BaseSchema):
    exercise_id = StringType(required=False, serialized_name='exerciseId')
    name = StringType(required=True, max_length=100, min_length=0)
    description = StringType(required=True, max_length=500, min_length=0)
    video_url = StringType(required=True, serialized_name='videoUrl', max_length=1000, min_length=0)
    equipment_number = NumberType(required=True, serialized_name='equipmentNumber')
    files = ListType(field=ModelType(model_spec=ExerciseFileInputSchema, required=False), required=False)


class ExerciseFileOutputSchema(BaseSchema):
    exercise_file_id = StringType(required=False, serialized_name='exerciseFileId')
    file_id = StringType(required=False, serialized_name='fileId')
    exercise_id = StringType(required=False, serialized_name='exerciseId')


class ExerciseOutputSchema(BaseSchema):
    exercise_id = StringType(required=False, serialized_name='exerciseId')
    name = StringType(required=True, max_length=100, min_length=0)
    description = StringType(required=True, max_length=500, min_length=0)
    video_url = StringType(required=True, serialized_name='videoUrl', max_length=1000, min_length=0)
    equipment_number = NumberType(required=True, serialized_name='equipmentNumber')
    files = ListType(field=ModelType(model_spec=ExerciseFileOutputSchema, required=False), required=False)

