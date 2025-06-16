import asyncpg
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.pool: asyncpg.Pool = None
        
        # Database configuration - use env vars if available, otherwise defaults
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = int(os.getenv("DB_PORT", "5432"))
        self.database = os.getenv("DB_NAME", "dev")
        self.user = os.getenv("DB_USER", "devweatherappuser")
        self.password = os.getenv("DB_PASSWORD")
        self.schema = os.getenv("DB_SCHEMA", "weatherapp")
        
        # Pool configuration
        self.min_size = int(os.getenv("DB_MIN_POOL_SIZE", "5"))
        self.max_size = int(os.getenv("DB_MAX_POOL_SIZE", "20"))
        self.command_timeout = int(os.getenv("DB_COMMAND_TIMEOUT", "60"))
        
    async def create_pool(self):
        """Create database connection pool"""
        try:
            self.pool = await asyncpg.create_pool(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                server_settings={
                    'search_path': self.schema
                },
                min_size=self.min_size,
                max_size=self.max_size,
                command_timeout=self.command_timeout
            )
            logger.info(f"Database connection pool created successfully - Host: {self.host}:{self.port}, DB: {self.database}, Schema: {self.schema}")
        except Exception as e:
            logger.error(f"Failed to create database pool: {e}")
            raise
    
    async def close_pool(self):
        """Close database connection pool"""
        if self.pool:
            await self.pool.close()
            logger.info("Database connection pool closed")
    
    @asynccontextmanager
    async def get_connection(self) -> AsyncGenerator[asyncpg.Connection, None]:
        """Get a database connection from the pool"""
        if not self.pool:
            raise RuntimeError("Database pool not initialized")
        
        async with self.pool.acquire() as connection:
            yield connection

# Global database manager instance
db_manager = DatabaseManager()

# Convenience function to get a database connection
async def get_db_connection():
    """Get database connection for dependency injection"""
    async with db_manager.get_connection() as connection:
        yield connection
