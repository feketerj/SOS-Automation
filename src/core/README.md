# Core Utilities Module

## Purpose
Shared utilities and common functionality used across all modules.

## Components
- `logger.py`: Centralized logging infrastructure
- `metrics.py`: Performance metrics collection
- `cache.py`: Caching layer implementation
- `database.py`: Database connection management
- `exceptions.py`: Custom exception definitions
- `validators.py`: Common validation functions
- `formatters.py`: Data formatting utilities

## Architecture Reference
See [/architecture.md](/architecture.md#6-core-utilities-srccore) for detailed specifications.

## v4.2 Compliance
- All operations return binary proof (WORKS/DOESN'T WORK)
- Atomic operations with rollback capability
- Trust level enforcement
- Session trace point recording