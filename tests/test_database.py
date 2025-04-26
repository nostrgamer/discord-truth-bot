"""Tests for the database component."""

import pytest
from discord_bot.database import Database
from datetime import datetime
import sqlite3
import os

@pytest.fixture
def test_db():
    """Create a test database instance using in-memory SQLite."""
    db = Database(db_path=":memory:")
    return db

def test_init_db(test_db):
    """Test database initialization creates the required table."""
    # Use the existing connection from test_db
    conn = test_db._get_connection()
    cursor = conn.cursor()
    
    # Check if monitoring_configs table exists
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='monitoring_configs'
    """)
    
    assert cursor.fetchone() is not None
    
    # Check table schema
    cursor.execute("PRAGMA table_info(monitoring_configs)")
    columns = cursor.fetchall()
    
    # Verify all required columns exist
    column_names = [col[1] for col in columns]
    assert "id" in column_names
    assert "username" in column_names
    assert "filter_keyword" in column_names
    assert "last_checked_timestamp" in column_names
    assert "last_post_id" in column_names
    assert "created_at" in column_names
    assert "is_active" in column_names

def test_add_monitoring_config(test_db):
    """Test adding a new monitoring configuration."""
    # Add a test configuration
    config_id = test_db.add_monitoring_config(
        username="test_user",
        filter_keyword="test_keyword"
    )
    
    assert config_id is not None
    assert config_id > 0
    
    # Verify the configuration was added using the existing connection
    conn = test_db._get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM monitoring_configs WHERE id = ?", (config_id,))
    row = cursor.fetchone()
    
    assert row is not None
    assert row[1] == "test_user"  # username
    assert row[2] == "test_keyword"  # filter_keyword
    assert row[6] == 1  # is_active

def test_get_monitoring_config(test_db):
    """Test retrieving the current monitoring configuration."""
    # Add a test configuration
    test_db.add_monitoring_config("test_user", "test_keyword")
    
    # Get the configuration
    config = test_db.get_monitoring_config()
    
    assert config is not None
    assert config['username'] == "test_user"
    assert config['filter_keyword'] == "test_keyword"
    assert config['is_active'] is True

def test_update_last_checked(test_db):
    """Test updating the last checked timestamp and post ID."""
    # Add a test configuration
    test_db.add_monitoring_config("test_user", "test_keyword")
    
    # Update last checked
    test_timestamp = datetime.now().isoformat()
    test_post_id = "test_post_123"
    test_db.update_last_checked(test_post_id, test_timestamp)
    
    # Verify the update
    config = test_db.get_monitoring_config()
    assert config['last_checked_timestamp'] == test_timestamp
    assert config['last_post_id'] == test_post_id

def test_deactivate_monitoring(test_db):
    """Test deactivating the current monitoring configuration."""
    # Add a test configuration
    test_db.add_monitoring_config("test_user", "test_keyword")
    
    # Verify it's active
    assert test_db.is_monitoring_active() is True
    
    # Deactivate monitoring
    test_db.deactivate_monitoring()
    
    # Verify it's inactive
    assert test_db.is_monitoring_active() is False

def test_is_monitoring_active(test_db):
    """Test checking if monitoring is active."""
    # Initially should be inactive
    assert test_db.is_monitoring_active() is False
    
    # Add a configuration
    test_db.add_monitoring_config("test_user", "test_keyword")
    assert test_db.is_monitoring_active() is True
    
    # Deactivate
    test_db.deactivate_monitoring()
    assert test_db.is_monitoring_active() is False

def test_multiple_configs_only_latest_active(test_db):
    """Test that only the latest configuration is active when multiple exist."""
    # Add first configuration
    test_db.add_monitoring_config("user1", "keyword1")
    
    # Add second configuration
    test_db.add_monitoring_config("user2", "keyword2")
    
    # Get current config
    config = test_db.get_monitoring_config()
    
    # Verify only the latest is returned
    assert config['username'] == "user2"
    assert config['filter_keyword'] == "keyword2"
    
    # Verify only one active configuration exists using the existing connection
    conn = test_db._get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM monitoring_configs WHERE is_active = 1")
    active_count = cursor.fetchone()[0]
    assert active_count == 1 