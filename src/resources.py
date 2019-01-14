from typing import Dict
from uuid import uuid4

from gwap_framework.resource.base import BaseResource
from gwap_framework.utils.decorators import validate_schema

from src.cache import cache
from src.database import master_async_session, read_replica_async_session
from src.models import ExerciseModel, ExerciseFileModel
from src.schemas import ExerciseInputSchema, ExerciseOutputSchema, ExerciseFileOutputSchema


class ExerciseResource(BaseResource):
    cache = cache
    method_decorators = {
        'create': [validate_schema(ExerciseInputSchema)],
        'update': [validate_schema(ExerciseInputSchema)],
    }

    def create(self, request_model: 'ExerciseInputSchema') -> Dict:
        exercise = ExerciseModel()
        exercise.id = request_model.exercise_id or str(uuid4())
        exercise.name = request_model.name
        exercise.description = request_model.description
        exercise.video_url = request_model.video_url

        exercise.files = []
        for f in request_model.files:
            exercise_file = ExerciseFileModel()
            exercise_file.id = f.exercise_id or str(uuid4())
            exercise_file.exercise_id = exercise.id
            exercise_file.file_id = f.file_id
            exercise.files.append(exercise_file)

        with master_async_session() as session:
            session.add(exercise)
            output = ExerciseOutputSchema()
            output.exercise_id = exercise.id
            output.name = exercise.name
            output.description = exercise.description
            output.video_url = exercise.video_url
            output.files = []
            for file in exercise.files:
                output_file = ExerciseFileOutputSchema()
                output_file.id = file.id
                output_file.exercise_id = file.exercise_id
                output_file.file_id = file.file_id
                output.files.append(output_file)

            output.validate()
            return output.to_primitive()

    def update(self, request_model: 'ExerciseInputSchema', exercise_id=None):
        exercise = ExerciseModel()
        exercise.id = exercise_id
        exercise.name = request_model.name
        exercise.description = request_model.description
        exercise.video_url = request_model.video_url

        with master_async_session() as session:
            session.merge(exercise)
            output = ExerciseOutputSchema()
            output.exercise_id = exercise.id
            output.name = exercise.name
            output.description = exercise.description
            output.video_url = exercise.video_url
            output.files = []
            for file in exercise.files:
                output_file = ExerciseFileOutputSchema()
                output_file.id = file.id
                output_file.exercise_id = file.exercise_id
                output_file.file_id = file.file_id
                output.files.append(output_file)

            output.validate()
            return output.to_primitive()

    def list(self, args=None, kwargs=None):
        with read_replica_async_session() as session:
            results = []
            for exercise in session.query(ExerciseModel).all():
                output = ExerciseOutputSchema()
                output.exercise_id = exercise.id
                output.name = exercise.name
                output.description = exercise.description
                output.video_url = exercise.video_url
                output.files = []
                for file in exercise.files:
                    output_file = ExerciseFileOutputSchema()
                    output_file.id = file.id
                    output_file.exercise_id = file.exercise_id
                    output_file.file_id = file.file_id
                    output.files.append(output_file)

                results.append(output.to_primitive())
        return results

    def retrieve(self, exercise_id):
        with read_replica_async_session() as session:
            exercise = session.query(ExerciseModel).filter_by(id=exercise_id).first()
            output = ExerciseOutputSchema()
            output.exercise_id = exercise.id
            output.name = exercise.name
            output.description = exercise.description
            output.video_url = exercise.video_url
            output.files = []
            for file in exercise.files:
                output_file = ExerciseFileOutputSchema()
                output_file.id = file.id
                output_file.exercise_id = file.exercise_id
                output_file.file_id = file.file_id
                output.files.append(output_file)
            return output.to_primitive()

    def destroy(self, exercise_id):
        with master_async_session() as session:
            session.query(ExerciseModel).filter_by(id=exercise_id).delete()
            return None


resources_v1 = [
    {'resource': ExerciseResource, 'urls': ['/exercises/<exercise_id>'], 'endpoint': 'Exercises ExerciseId',
     'methods': ['GET', 'PUT', 'PATCH', 'DELETE']},
    {'resource': ExerciseResource, 'urls': ['/exercises'], 'endpoint': 'Exercises',
     'methods': ['POST', 'GET']},
]
