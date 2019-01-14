from uuid import uuid4

from gwap_framework.models.base import BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class ExerciseModel(BaseModel):
    __tablename__ = 'exercises'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    video_url = Column(String(1000), nullable=True)
    equipment_number = Column(Integer, nullable=True)
    files = relationship("ExerciseFileModel", backref="exercise")


class ExerciseFileModel(BaseModel):
    __tablename__ = 'exercises_files'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    exercise_id = Column(UUID(as_uuid=True), ForeignKey('exercises.id'))
    file_id = Column(UUID(as_uuid=True), nullable=False)
    exercise = relationship("ExerciseModel", back_populates="files")
