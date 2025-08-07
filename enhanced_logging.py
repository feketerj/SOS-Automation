"""
Enhanced Logging and Error Handling Configuration for SOS Pipeline
Provides comprehensive debugging capabilities for future maintenance and upgrades
"""

import logging
import logging.handlers
import sys
import os
import traceback
import json
import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Callable
from functools import wraps
import time

class SOSLoggingConfig:
    """
    Centralized logging configuration for the entire SOS pipeline
    Provides multiple log levels, file rotation, and debugging capabilities
    """
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.setup_loggers()
    
    def setup_loggers(self):
        """Set up comprehensive logging system"""
        
        # Main application logger
        self.setup_main_logger()
        
        # API-specific logger
        self.setup_api_logger()
        
        # Filter-specific logger
        self.setup_filter_logger()
        
        # Error-specific logger
        self.setup_error_logger()
        
        # Performance logger
        self.setup_performance_logger()
    
    def setup_main_logger(self):
        """Main application logger with file rotation"""
        main_logger = logging.getLogger('sos_pipeline')
        main_logger.setLevel(logging.DEBUG)
        
        # Console handler for immediate feedback
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        
        # File handler with rotation for persistent logging
        file_handler = logging.handlers.RotatingFileHandler(
            self.log_dir / 'sos_pipeline.log',
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        
        main_logger.addHandler(console_handler)
        main_logger.addHandler(file_handler)
    
    def setup_api_logger(self):
        """API-specific logger for tracking API calls and responses"""
        api_logger = logging.getLogger('sos_pipeline.api')
        api_logger.setLevel(logging.DEBUG)
        
        api_handler = logging.handlers.RotatingFileHandler(
            self.log_dir / 'api_calls.log',
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3
        )
        api_formatter = logging.Formatter(
            '%(asctime)s - API - %(levelname)s - %(message)s'
        )
        api_handler.setFormatter(api_formatter)
        api_logger.addHandler(api_handler)
    
    def setup_filter_logger(self):
        """Filter-specific logger for tracking decision logic"""
        filter_logger = logging.getLogger('sos_pipeline.filter')
        filter_logger.setLevel(logging.DEBUG)
        
        filter_handler = logging.handlers.RotatingFileHandler(
            self.log_dir / 'filter_decisions.log',
            maxBytes=20*1024*1024,  # 20MB (lots of decision data)
            backupCount=5
        )
        filter_formatter = logging.Formatter(
            '%(asctime)s - FILTER - %(levelname)s - %(message)s'
        )
        filter_handler.setFormatter(filter_formatter)
        filter_logger.addHandler(filter_handler)
    
    def setup_error_logger(self):
        """Error-specific logger for tracking failures and exceptions"""
        error_logger = logging.getLogger('sos_pipeline.errors')
        error_logger.setLevel(logging.WARNING)
        
        error_handler = logging.handlers.RotatingFileHandler(
            self.log_dir / 'errors.log',
            maxBytes=5*1024*1024,  # 5MB
            backupCount=10  # Keep more error logs
        )
        error_formatter = logging.Formatter(
            '%(asctime)s - ERROR - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )
        error_handler.setFormatter(error_formatter)
        error_logger.addHandler(error_handler)
    
    def setup_performance_logger(self):
        """Performance logger for tracking execution times and bottlenecks"""
        perf_logger = logging.getLogger('sos_pipeline.performance')
        perf_logger.setLevel(logging.INFO)
        
        perf_handler = logging.handlers.RotatingFileHandler(
            self.log_dir / 'performance.log',
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3
        )
        perf_formatter = logging.Formatter(
            '%(asctime)s - PERF - %(message)s'
        )
        perf_handler.setFormatter(perf_formatter)
        perf_logger.addHandler(perf_handler)

class DebugTracker:
    """
    Tracks debugging information for pattern matching and filter decisions
    Helps identify why certain opportunities were or weren't caught
    """
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.debug_file = self.log_dir / "debug_decisions.jsonl"
        
    def log_filter_decision(self, opportunity_id: str, step: str, pattern: str, 
                          text_sample: str, matched: bool, context: Optional[Dict[str, Any]] = None):
        """Log detailed filter decision for debugging"""
        debug_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "opportunity_id": opportunity_id,
            "step": step,
            "pattern": pattern,
            "text_sample": text_sample[:200],  # Limit text sample size
            "matched": matched,
            "context": context or {}
        }
        
        with open(self.debug_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(debug_entry) + '\n')
    
    def log_pattern_miss(self, opportunity_id: str, expected_pattern: str, 
                        full_text: str, reason: str):
        """Log when an expected pattern wasn't matched"""
        miss_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "opportunity_id": opportunity_id,
            "type": "pattern_miss",
            "expected_pattern": expected_pattern,
            "text_length": len(full_text),
            "text_preview": full_text[:500],
            "reason": reason
        }
        
        with open(self.debug_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(miss_entry) + '\n')

def timing_decorator(func):
    """Decorator to track function execution times"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        perf_logger = logging.getLogger('sos_pipeline.performance')
        
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            perf_logger.info(f"{func.__name__} executed in {execution_time:.4f} seconds")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            perf_logger.warning(f"{func.__name__} failed after {execution_time:.4f} seconds: {str(e)}")
            raise
    
    return wrapper

def error_handler(func):
    """Decorator for comprehensive error handling and logging"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        error_logger = logging.getLogger('sos_pipeline.errors')
        
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_info = {
                "function": func.__name__,
                "args": str(args)[:200],  # Limit arg logging
                "kwargs": str(kwargs)[:200],
                "error_type": type(e).__name__,
                "error_message": str(e),
                "traceback": traceback.format_exc()
            }
            
            error_logger.error(f"Function {func.__name__} failed: {json.dumps(error_info, indent=2)}")
            raise
    
    return wrapper

class FilterDecisionLogger:
    """
    Specialized logger for tracking filter decisions with detailed context
    Helps understand why opportunities were classified as GO/NO-GO
    """
    
    def __init__(self):
        self.logger = logging.getLogger('sos_pipeline.filter')
        self.debug_tracker = DebugTracker()
    
    def log_phase_0_decision(self, opp_id: str, step: str, decision: bool, 
                           reasoning: str, text_context: str = ""):
        """Log Phase 0 preliminary gate decisions"""
        self.logger.info(f"PHASE_0 | {opp_id} | {step} | {'PASS' if decision else 'FAIL'} | {reasoning}")
        
        if text_context:
            self.debug_tracker.log_filter_decision(
                opp_id, f"phase_0_{step}", reasoning, text_context, decision
            )
    
    def log_phase_1_decision(self, opp_id: str, step: str, decision: bool, 
                           reasoning: str, matched_pattern: str = "", text_context: str = ""):
        """Log Phase 1 hard stop decisions"""
        self.logger.info(f"PHASE_1 | {opp_id} | {step} | {'PASS' if decision else 'FAIL'} | {reasoning}")
        
        if matched_pattern or text_context:
            self.debug_tracker.log_filter_decision(
                opp_id, f"phase_1_{step}", matched_pattern, text_context, not decision,
                {"reasoning": reasoning}
            )
    
    def log_final_decision(self, opp_id: str, decision: str, reasoning_summary: str):
        """Log final GO/NO-GO decision with complete reasoning"""
        self.logger.info(f"FINAL | {opp_id} | {decision} | {reasoning_summary}")
    
    def log_pattern_enhancement_opportunity(self, opp_id: str, missed_pattern: str, 
                                          suggestion: str, text_sample: str):
        """Log opportunities to enhance pattern matching"""
        self.logger.warning(f"ENHANCEMENT_OPP | {opp_id} | Missed: {missed_pattern} | Suggestion: {suggestion}")
        self.debug_tracker.log_pattern_miss(opp_id, missed_pattern, text_sample, suggestion)

def initialize_logging(log_level: str = "INFO"):
    """
    Initialize the complete logging system for the SOS pipeline
    Call this at the start of main_pipeline.py
    """
    
    # Set up comprehensive logging
    logging_config = SOSLoggingConfig()
    
    # Set global log level
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    logging.getLogger('sos_pipeline').setLevel(numeric_level)
    
    # Create summary log file for daily operations
    main_logger = logging.getLogger('sos_pipeline')
    main_logger.info("=" * 80)
    main_logger.info(f"SOS Pipeline started at {datetime.datetime.now()}")
    main_logger.info(f"Log level set to: {log_level}")
    main_logger.info("=" * 80)
    
    return logging_config

def create_session_summary(start_time: datetime.datetime, total_opportunities: int, 
                         go_count: int, no_go_count: int, errors_count: int):
    """Create a summary of the pipeline session for review"""
    
    session_logger = logging.getLogger('sos_pipeline')
    duration = datetime.datetime.now() - start_time
    
    summary = f"""
    ================== SESSION SUMMARY ==================
    Start Time: {start_time}
    Duration: {duration}
    Total Opportunities: {total_opportunities}
    GO Decisions: {go_count}
    NO-GO Decisions: {no_go_count}
    Success Rate: {(go_count/total_opportunities*100):.2f}% if total_opportunities > 0 else 'N/A'
    Errors Encountered: {errors_count}
    =====================================================
    """
    
    session_logger.info(summary)
    
    # Also write to a dedicated session log
    session_file = Path("logs") / "session_summaries.log"
    with open(session_file, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.datetime.now().isoformat()} - {summary}\n")

if __name__ == "__main__":
    # Demo of the logging system
    initialize_logging("DEBUG")
    
    main_logger = logging.getLogger('sos_pipeline')
    api_logger = logging.getLogger('sos_pipeline.api')
    filter_logger = logging.getLogger('sos_pipeline.filter')
    error_logger = logging.getLogger('sos_pipeline.errors')
    
    main_logger.info("Testing logging system")
    api_logger.info("API call test")
    filter_logger.info("Filter decision test")
    error_logger.error("Error logging test")
    
    print("Logging system initialized successfully!")
    print("Check the 'logs' directory for log files")
