from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class TopicBase(BaseModel):
    title: str
    slug: str
    description: Optional[str] = None
    learning_objectives: Optional[str] = None
    difficulty: Optional[int] = None
    estimated_hours: Optional[float] = None


class TopicCreate(TopicBase):
    roadmap_id: int
    section_id: Optional[int] = None


class TopicResponse(TopicBase):
    id: int
    roadmap_id: int
    section_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class TopicRelationshipBase(BaseModel):
    from_topic_id: int
    to_topic_id: int
    relationship_type: str  # prerequisite, related, optional, next


class TopicRelationshipCreate(TopicRelationshipBase):
    pass


class TopicRelationshipResponse(TopicRelationshipBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class RoadmapSectionBase(BaseModel):
    title: str
    description: Optional[str] = None
    order_index: int
    parent_section_id: Optional[int] = None


class RoadmapSectionCreate(RoadmapSectionBase):
    roadmap_id: int


class RoadmapSectionResponse(RoadmapSectionBase):
    id: int
    roadmap_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class RoadmapBase(BaseModel):
    title: str
    description: Optional[str] = None


class RoadmapCreate(RoadmapBase):
    pass


class RoadmapResponse(RoadmapBase):
    id: int
    version: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class RoadmapWithDetails(RoadmapResponse):
    sections: List[RoadmapSectionResponse] = []
    topics: List[TopicResponse] = []


class TopicWithRelationships(TopicResponse):
    prerequisites: List[TopicResponse] = []
    related: List[TopicResponse] = []
    next_topics: List[TopicResponse] = []


class TopicDetail(TopicWithRelationships):
    resources: List["ResourceResponse"] = []
    exercises: Optional[str] = None
    projects: Optional[str] = None
