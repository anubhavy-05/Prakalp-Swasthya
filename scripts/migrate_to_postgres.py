#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Migration Script: JSON to PostgreSQL
Migrates clinic data from data/clinics.json to PostgreSQL database
"""

import os
import sys
import json
import logging
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import DatabaseManager, Clinic
from src.config_loader import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_location_key(location_key):
    """
    Parse location key to extract city and area
    Example: "Lucknow_Gomti_Nagar_Vikas_Khand" -> city="Lucknow", area="Gomti Nagar Vikas Khand"
    """
    parts = location_key.split('_')
    city = parts[0] if parts else None
    area = ' '.join(parts[1:]) if len(parts) > 1 else None
    return city, area


def migrate_clinics(json_file='data/clinics.json', database_url=None):
    """
    Migrate clinics from JSON file to PostgreSQL database
    
    Args:
        json_file: Path to clinics.json file
        database_url: PostgreSQL connection URL (optional, uses Config if not provided)
    
    Returns:
        dict: Migration statistics
    """
    logger.info("Starting clinic migration from JSON to PostgreSQL")
    
    # Initialize database
    if database_url:
        db_manager = DatabaseManager(database_url)
    else:
        db_manager = DatabaseManager(Config.DATABASE_URL)
    
    # Create tables
    logger.info("Creating database tables...")
    db_manager.create_tables()
    
    # Load JSON data
    logger.info(f"Loading clinic data from {json_file}")
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            clinics_data = json.load(f)
    except FileNotFoundError:
        logger.error(f"File not found: {json_file}")
        return {'success': False, 'error': 'File not found'}
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON format: {e}")
        return {'success': False, 'error': 'Invalid JSON format'}
    
    # Migration statistics
    stats = {
        'total_locations': len(clinics_data),
        'total_clinics': 0,
        'inserted': 0,
        'failed': 0,
        'errors': []
    }
    
    # Migrate clinics
    with db_manager.get_session() as session:
        for location_key, clinics_list in clinics_data.items():
            logger.info(f"Processing location: {location_key} ({len(clinics_list)} clinics)")
            
            # Parse location
            city, area = parse_location_key(location_key)
            
            for clinic_data in clinics_list:
                stats['total_clinics'] += 1
                
                try:
                    # Create Clinic object
                    clinic = Clinic(
                        name=clinic_data.get('name'),
                        address=clinic_data.get('address'),
                        city=city,
                        area=area,
                        location_key=location_key,
                        timing=clinic_data.get('timing'),
                        phone=clinic_data.get('phone'),
                        specialties=clinic_data.get('specialties', []),
                        fees=clinic_data.get('fees'),
                        latitude=clinic_data.get('latitude'),
                        longitude=clinic_data.get('longitude'),
                        is_active=True,
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    
                    # Add to session
                    session.add(clinic)
                    stats['inserted'] += 1
                    
                except Exception as e:
                    stats['failed'] += 1
                    error_msg = f"Failed to insert clinic '{clinic_data.get('name')}': {e}"
                    logger.error(error_msg)
                    stats['errors'].append(error_msg)
        
        # Commit all changes
        try:
            session.commit()
            logger.info("All clinics committed to database successfully")
        except Exception as e:
            logger.error(f"Failed to commit changes: {e}")
            session.rollback()
            stats['success'] = False
            stats['errors'].append(f"Commit failed: {e}")
            return stats
    
    # Success
    stats['success'] = True
    logger.info(f"Migration completed successfully!")
    logger.info(f"Statistics: {stats}")
    
    return stats


def verify_migration(database_url=None):
    """
    Verify migration by checking clinic count
    
    Args:
        database_url: PostgreSQL connection URL
    
    Returns:
        dict: Verification results
    """
    logger.info("Verifying migration...")
    
    # Initialize database
    if database_url:
        db_manager = DatabaseManager(database_url)
    else:
        db_manager = DatabaseManager(Config.DATABASE_URL)
    
    with db_manager.get_session() as session:
        clinic_count = session.query(Clinic).count()
        
        # Get sample clinics
        sample_clinics = session.query(Clinic).limit(5).all()
        
        logger.info(f"Total clinics in database: {clinic_count}")
        logger.info("Sample clinics:")
        for clinic in sample_clinics:
            logger.info(f"  - {clinic.name} ({clinic.city}, {clinic.area})")
        
        return {
            'total_clinics': clinic_count,
            'sample_clinics': [c.to_dict() for c in sample_clinics]
        }


def main():
    """Main entry point for migration script"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Migrate clinic data from JSON to PostgreSQL')
    parser.add_argument(
        '--json-file',
        default='data/clinics.json',
        help='Path to clinics.json file (default: data/clinics.json)'
    )
    parser.add_argument(
        '--database-url',
        help='PostgreSQL database URL (optional, uses Config.DATABASE_URL if not provided)'
    )
    parser.add_argument(
        '--verify-only',
        action='store_true',
        help='Only verify migration without migrating'
    )
    parser.add_argument(
        '--drop-tables',
        action='store_true',
        help='Drop existing tables before migration (CAUTION: deletes all data!)'
    )
    
    args = parser.parse_args()
    
    try:
        # Verify only
        if args.verify_only:
            results = verify_migration(args.database_url)
            print(f"\n✅ Verification complete: {results['total_clinics']} clinics found")
            return
        
        # Drop tables if requested
        if args.drop_tables:
            logger.warning("⚠️  Dropping all existing tables...")
            response = input("Are you sure? This will delete all data! (yes/no): ")
            if response.lower() != 'yes':
                logger.info("Migration cancelled")
                return
            
            db_manager = DatabaseManager(args.database_url or Config.DATABASE_URL)
            db_manager.drop_tables()
            logger.info("Tables dropped successfully")
        
        # Run migration
        stats = migrate_clinics(args.json_file, args.database_url)
        
        if stats.get('success'):
            print("\n" + "="*60)
            print("✅ MIGRATION SUCCESSFUL!")
            print("="*60)
            print(f"Total Locations: {stats['total_locations']}")
            print(f"Total Clinics: {stats['total_clinics']}")
            print(f"Successfully Inserted: {stats['inserted']}")
            print(f"Failed: {stats['failed']}")
            
            if stats['errors']:
                print("\nErrors:")
                for error in stats['errors'][:5]:  # Show first 5 errors
                    print(f"  - {error}")
            
            # Verify migration
            print("\nVerifying migration...")
            verify_results = verify_migration(args.database_url)
            print(f"✅ Verified: {verify_results['total_clinics']} clinics in database")
            print("="*60)
        else:
            print("\n❌ MIGRATION FAILED!")
            print("Errors:")
            for error in stats.get('errors', []):
                print(f"  - {error}")
    
    except Exception as e:
        logger.error(f"Migration failed: {e}", exc_info=True)
        print(f"\n❌ Migration failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
