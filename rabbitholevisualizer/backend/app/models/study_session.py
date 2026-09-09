from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.core.database import Base


class StudySession(Base):
    __tablename__ = "study_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    roadmap_id = Column(Integer, ForeignKey("roadmaps.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    goal = Column(Text, nullable=True)
    status = Column(String(50), default="active")  # active, completed, abandoned
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)
    duration_minutes = Column(Float, nullable=True)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="study_sessions")
    roadmap = relationship("Roadmap")
    topic = relationship("Topic")
    exploration_events = relationship("ExplorationEvent", back_populates="session", order_by="ExplorationEvent.sequence_order")


class ExplorationEvent(Base):
    __tablename__ = "exploration_events"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("study_sessions.id"), nullable=False)
    source_topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    source_topic_name = Column(String(255), nullable=False)  # For non-roadmap topics
    destination_topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    destination_topic_name = Column(String(255), nullable=False)
    sequence_order = Column(Integer, nullable=False)
    relationship_type = Column(String(50), nullable=True)  # same, related, unrelated
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=True)
    notes = Column(Text, nullable=True)
    duration_minutes = Column(Float, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    session = relationship("StudySession", back_populates="exploration_events")
    source_topic = relationship("Topic", foreign_keys=[source_topic_id])
    destination_topic = relationship("Topic", foreign_keys=[destination_topic_id])
    resource = relationship("Resource")


class Resource(Base):
    __tablename__ = "resources"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    url = Column(String(2048), nullable=True)
    resource_type = Column(String(50), nullable=False)  # youtube, documentation, blog, github, paper, book, course, other
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="resources")
    topic_resources = relationship("TopicResource", back_populates="resource")


class TopicResource(Base):
    __tablename__ = "topic_resources"
    
    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    topic = relationship("Topic", back_populates="resources")
    resource = relationship("Resource", back_populates="topic_resources")


class RabbitHole(Base):
    __tablename__ = "rabbit_holes"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("study_sessions.id"), nullable=False)
    divergence_point = Column(String(255), nullable=False)
    rejoin_point = Column(String(255), nullable=True)
    depth = Column(Integer, nullable=False)
    classification = Column(String(50), nullable=False)  # ON_PATH, RELATED, OPTIONAL, OFF_PATH, DEEP_RABBIT_HOLE
    topics_explored = Column(JSON, nullable=False)  # List of topic names
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    session = relationship("StudySession")


class SessionSummary(Base):
    __tablename__ = "session_summaries"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("study_sessions.id"), nullable=False)
    planned_path = Column(JSON, nullable=False)  # List of topic names
    actual_path = Column(JSON, nullable=False)  # List of topic names
    common_path = Column(JSON, nullable=True)
    divergence_point = Column(String(255), nullable=True)
    rejoin_point = Column(String(255), nullable=True)
    skipped_topics = Column(JSON, nullable=True)  # List of topic names
    extra_topics = Column(JSON, nullable=True)  # List of topic names
    rabbit_holes = Column(JSON, nullable=True)  # List of rabbit hole summaries
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    session = relationship("StudySession")
