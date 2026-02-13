# -*- coding: utf-8 -*-
"""
Database Connection Manager
Handles PostgreSQL connections with connection pooling
"""

import os
import logging
from contextlib import contextmanager
from sqlalchemy import create_engine, event, exc
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import Pool
from .models import Base

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Database Manager for PostgreSQL connections
    Implements connection pooling and session management
    """
    
    def __init__(self, database_url=None):
        """
        Initialize database manager
        
        Args:
            database_url: PostgreSQL connection URL
                         Format: postgresql://user:password@host:port/database
        """
        self.database_url = database_url or os.getenv('DATABASE_URL')
        
        if not self.database_url:
            raise ValueError(
                "Database URL not provided. Set DATABASE_URL environment variable "
                "or pass database_url parameter."
            )
        
        # Handle Heroku/Render postgres:// URLs (convert to postgresql://)
        if self.database_url.startswith('postgres://'):
            self.database_url = self.database_url.replace('postgres://', 'postgresql://', 1)
        
        # Create engine with connection pooling
        self.engine = create_engine(
            self.database_url,
            pool_size=10,  # Maximum number of connections in pool
            max_overflow=20,  # Additional connections if pool is full
            pool_timeout=30,  # Timeout for getting connection from pool
            pool_recycle=3600,  # Recycle connections after 1 hour
            pool_pre_ping=True,  # Verify connections before using
            echo=False  # Set to True for SQL query logging
        )
        
        # Add connection pool event listeners
        self._add_pool_listeners()
        
        # Create session factory
        session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(session_factory)
        
        logger.info("Database manager initialized successfully")
    
    def _add_pool_listeners(self):
        """Add event listeners for connection pool monitoring"""
        
        @event.listens_for(Pool, "connect")
        def receive_connect(dbapi_conn, connection_record):
            logger.debug("New database connection established")
        
        @event.listens_for(Pool, "checkout")
        def receive_checkout(dbapi_conn, connection_record, connection_proxy):
            logger.debug("Connection checked out from pool")
        
        @event.listens_for(Pool, "checkin")
        def receive_checkin(dbapi_conn, connection_record):
            logger.debug("Connection returned to pool")
    
    def create_tables(self):
        """Create all tables in the database"""
        try:
            Base.metadata.create_all(self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
            raise
    
    def drop_tables(self):
        """Drop all tables from the database (use with caution!)"""
        try:
            Base.metadata.drop_all(self.engine)
            logger.warning("All database tables dropped")
        except Exception as e:
            logger.error(f"Error dropping tables: {e}")
            raise
    
    @contextmanager
    def get_session(self):
        """
        Context manager for database sessions
        
        Usage:
            with db_manager.get_session() as session:
                # Use session here
                session.add(new_object)
                session.commit()
        """
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()
    
    def get_db_session(self):
        """
        Get a new database session
        Remember to close the session after use!
        
        Returns:
            SQLAlchemy Session object
        """
        return self.Session()
    
    def close_session(self, session):
        """Close a database session"""
        if session:
            session.close()
    
    def health_check(self):
        """
        Check database connection health
        
        Returns:
            dict: Status information
        """
        try:
            with self.get_session() as session:
                # Execute simple query
                session.execute("SELECT 1")
            
            return {
                'status': 'healthy',
                'database': 'connected',
                'pool_size': self.engine.pool.size(),
                'checked_out': self.engine.pool.checkedout()
            }
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {
                'status': 'unhealthy',
                'error': str(e)
            }
    
    def close(self):
        """Close all database connections"""
        self.Session.remove()
        self.engine.dispose()
        logger.info("Database connections closed")


# Global database manager instance
_db_manager = None


def init_db(database_url=None):
    """
    Initialize global database manager
    
    Args:
        database_url: PostgreSQL connection URL
    
    Returns:
        DatabaseManager instance
    """
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager(database_url)
    return _db_manager


def get_db_manager():
    """
    Get global database manager instance
    
    Returns:
        DatabaseManager instance
    """
    global _db_manager
    if _db_manager is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return _db_manager


def get_db_session():
    """
    Get a new database session from global manager
    
    Returns:
        SQLAlchemy Session
    """
    return get_db_manager().get_db_session()


@contextmanager
def db_session():
    """
    Context manager for database sessions using global manager
    
    Usage:
        from database import db_session
        
        with db_session() as session:
            clinics = session.query(Clinic).all()
    """
    db_manager = get_db_manager()
    with db_manager.get_session() as session:
        yield session
