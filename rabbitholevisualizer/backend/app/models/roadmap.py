from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.core.database import Base


class Roadmap(Base):
    __tablename__ = "roadmaps"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    version = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    sections = relationship("RoadmapSection", back_populates="roadmap")
    topics = relationship("Topic", back_populates="roadmap")
    user_roadmaps = relationship("UserRoadmap", back_populates="roadmap")


class RoadmapSection(Base):
    __tablename__ = "roadmap_sections"
    
    id = Column(Integer, primary_key=True, index=True)
    roadmap_id = Column(Integer, ForeignKey("roadmaps.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    order_index = Column(Integer, nullable=False)
    parent_section_id = Column(Integer, ForeignKey("roadmap_sections.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    roadmap = relationship("Roadmap", back_populates="sections")
    parent_section = relationship("RoadmapSection", remote_side=[id])
    sub_sections = relationship("RoadmapSection", back_populates="parent_section")


class Topic(Base):
    __tablename__ = "topics"
    
    id = Column(Integer, primary_key=True, index=True)
    roadmap_id = Column(Integer, ForeignKey("roadmaps.id"), nullable=False)
    section_id = Column(Integer, ForeignKey("roadmap_sections.id"), nullable=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    learning_objectives = Column(Text, nullable=True)  # JSON array
    difficulty = Column(Integer, nullable=True)  # 1-5
    estimated_hours = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    roadmap = relationship("Roadmap", back_populates="topics")
    section = relationship("RoadmapSection")
    relationships_from = relationship("TopicRelationship", foreign_keys="TopicRelationship.from_topic_id", back_populates="from_topic")
    relationships_to = relationship("TopicRelationship", foreign_keys="TopicRelationship.to_topic_id", back_populates="to_topic")
    resources = relationship("TopicResource", back_populates="topic")
    user_progress = relationship("UserTopicProgress", back_populates="topic")


class TopicRelationship(Base):
    __tablename__ = "topic_relationships"
    
    id = Column(Integer, primary_key=True, index=True)
    from_topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    to_topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    relationship_type = Column(String(50), nullable=False)  # prerequisite, related, optional, next
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    from_topic = relationship("Topic", foreign_keys=[from_topic_id], back_populates="relationships_from")
    to_topic = relationship("Topic", foreign_keys=[to_topic_id], back_populates="relationships_to")


class UserRoadmap(Base):
    __tablename__ = "user_roadmaps"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    roadmap_id = Column(Integer, ForeignKey("roadmaps.id"), nullable=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="user_roadmaps")
    roadmap = relationship("Roadmap", back_populates="user_roadmaps")


class UserTopicProgress(Base):
    __tablename__ = "user_topic_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    status = Column(String(50), default="not_started")  # not_started, in_progress, completed
    progress_percent = Column(Integer, default=0)
    notes = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    topic = relationship("Topic", back_populates="user_progress")
