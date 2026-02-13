#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Database Initialization Script
Sets up PostgreSQL database and creates all tables
"""

import os
import sys
import logging

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import DatabaseManager
from src.config_loader import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def init_database(database_url=None):
    """
    Initialize database and create all tables
    
    Args:
        database_url: PostgreSQL connection URL (optional, uses Config if not provided)
    """
    logger.info("Starting database initialization...")
    
    try:
        # Initialize database manager
        if database_url:
            db_manager = DatabaseManager(database_url)
        else:
            db_manager = DatabaseManager(Config.DATABASE_URL)
        
        logger.info(f"Connected to database: {Config.DATABASE_URL.split('@')[-1]}")
        
        # Create all tables
        logger.info("Creating database tables...")
        db_manager.create_tables()
        
        logger.info("✅ Database tables created successfully!")
        
        # Health check
        health = db_manager.health_check()
        logger.info(f"Database health check: {health}")
        
        return True
    
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}", exc_info=True)
        return False


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Initialize PostgreSQL database')
    parser.add_argument(
        '--database-url',
        help='PostgreSQL database URL (optional, uses Config.DATABASE_URL if not provided)'
    )
    parser.add_argument(
        '--drop-existing',
        action='store_true',
        help='Drop existing tables before creating new ones (CAUTION: deletes all data!)'
    )
    
    args = parser.parse_args()
    
    # Drop tables if requested
    if args.drop_existing:
        logger.warning("⚠️  Dropping all existing tables...")
        response = input("Are you sure? This will delete all data! (yes/no): ")
        if response.lower() != 'yes':
            logger.info("Cancelled")
            return
        
        try:
            db_manager = DatabaseManager(args.database_url or Config.DATABASE_URL)
            db_manager.drop_tables()
            logger.info("Tables dropped successfully")
        except Exception as e:
            logger.error(f"Failed to drop tables: {e}")
            sys.exit(1)
    
    # Initialize database
    success = init_database(args.database_url)
    
    if success:
        print("\n" + "="*60)
        print("✅ DATABASE INITIALIZATION SUCCESSFUL!")
        print("="*60)
        print("\nNext steps:")
        print("1. Run migration script to import clinic data:")
        print("   python scripts/migrate_to_postgres.py")
        print("\n2. Start your application:")
        print("   python app.py")
        print("="*60 + "\n")
    else:
        print("\n❌ Database initialization failed. Check logs for details.\n")
        sys.exit(1)


if __name__ == '__main__':
    main()
