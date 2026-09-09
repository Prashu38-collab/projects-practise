from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class StudySessionBase(BaseModel):
    roadmap_id: int
    topic_id: int
    goal: Optional[str] = None


class StudySessionCreate(StudySessionBase):
    pass


class StudySessionResponse(StudySessionBase):
    id: int
    user_id: int
    status: str
    started_at: datetime
    ended_at: Optional[datetime]
    duration_minutes: Optional[float]
    summary: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class StudySessionWithEvents(StudySessionResponse):
    exploration_events: List["ExplorationEventResponse"] = []


class ExplorationEventBase(BaseModel):
    source_topic_name: str
    destination_topic_name: str
    source_topic_id: Optional[int] = None
    destination_topic_id: Optional[int] = None
    relationship_type: Optional[str] = None
    resource_id: Optional[int] = None
    notes: Optional[str] = None
    duration_minutes: Optional[float] = None


class ExplorationEventCreate(ExplorationEventBase):
    pass


class ExplorationEventResponse(ExplorationEventBase):
    id: int
    session_id: int
    sequence_order: int
    timestamp: datetime
    
    class Config:
        from_attributes = True


class ResourceBase(BaseModel):
    title: str
    url: Optional[str] = None
    resource_type: str  # youtube, documentation, blog, github, paper, book, course, other
    notes: Optional[str] = None


class ResourceCreate(ResourceBase):
    pass


class ResourceResponse(ResourceBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class RabbitHoleResponse(BaseModel):
    id: int
    session_id: int
    divergence_point: str
    rejoin_point: Optional[str]
    depth: int
    classification: str
    topics_explored: List[str]
    description: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class ComparisonResult(BaseModel):
    planned_path: List[str]
    actual_path: List[str]
    common_path: List[str]
    divergence_point: Optional[str]
    rejoin_point: Optional[str]
    rabbit_holes: List[RabbitHoleResponse]
    skipped_topics: List[str]
    extra_topics: List[str]


class JourneyResponse(BaseModel):
    session_id: int
    events: List[ExplorationEventResponse]
    planned_path: List[str]
    actual_path: List[str]
