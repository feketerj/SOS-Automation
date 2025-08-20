#!/usr/bin/env node
/**
 * SOS Assessment Automation Tool - Main Entry Point
 * 
 * This application processes government contract opportunities through
 * a deterministic pipeline with v4.2 SOP compliance.
 * 
 * Architecture: /architecture.md
 * Configuration: /src/config/default.json
 * 
 * CLI Usage: node src/main.js --file "<path>" --session "<id>"
 */

const fs = require('fs').promises;
const path = require('path');
const { spawn } = require('child_process');

// Import pipeline modules
const DocumentReader = require('./ingestion/reader');
const ProcessingPipeline = require('./processing/pipeline');
const DecisionWriter = require('./export/writer');
const SessionManager = require('./core/session');

// v4.2 compliance constants
const TRUST_LEVEL_MIN = 25;
const SESSION_PREFIX = 'sess-';
const BINARY_PROOF = { WORKS: 'WORKS', DOESNT_WORK: 'DOESN\'T WORK' };

/**
 * Application class for SOS Assessment Automation Tool
 */
class SOSAssessmentTool {
    constructor() {
        this.trustLevel = 80; // Current trust level from continuity
        this.sessionId = this.generateSessionId();
        this.tracePoints = [];
        this.config = null;
    }

    /**
     * Generate unique session ID
     */
    generateSessionId() {
        const now = new Date();
        const timestamp = now.toTimeString().slice(0, 8).replace(/:/g, '');
        return `${SESSION_PREFIX}${timestamp}`;
    }

    /**
     * Load configuration
     */
    async loadConfig() {
        try {
            const configPath = path.join(__dirname, 'config', 'default.json');
            const configData = await fs.readFile(configPath, 'utf8');
            this.config = JSON.parse(configData);
            console.log(`[${this.sessionId}] Configuration loaded successfully`);
            return BINARY_PROOF.WORKS;
        } catch (error) {
            console.error(`[${this.sessionId}] Failed to load config:`, error.message);
            return BINARY_PROOF.DOESNT_WORK;
        }
    }

    /**
     * Record trace point for v4.2 compliance
     */
    recordTrace(point, details = '') {
        const trace = {
            point,
            timestamp: new Date().toISOString(),
            sessionId: this.sessionId,
            details
        };
        this.tracePoints.push(trace);
        console.log(`[TRACE] ${point}: ${details}`);
    }

    /**
     * Check trust level requirement
     */
    checkTrustLevel(required) {
        if (this.trustLevel < required) {
            console.error(`Trust level ${this.trustLevel}% insufficient (requires ${required}%)`);
            return false;
        }
        return true;
    }

    /**
     * Initialize ingestion module
     */
    async initializeIngestion() {
        if (!this.checkTrustLevel(TRUST_LEVEL_MIN)) {
            return BINARY_PROOF.DOESNT_WORK;
        }

        this.recordTrace('Creation', 'Ingestion module initialized');
        
        try {
            // Import ingestion module (Python bridge)
            const pythonProcess = spawn('python', [
                path.join(__dirname, 'ingestion_pipeline.py'),
                '--mode', 'init'
            ]);

            return new Promise((resolve) => {
                pythonProcess.on('close', (code) => {
                    if (code === 0) {
                        console.log('Ingestion module ready');
                        resolve(BINARY_PROOF.WORKS);
                    } else {
                        console.error('Ingestion module failed to initialize');
                        resolve(BINARY_PROOF.DOESNT_WORK);
                    }
                });
            });
        } catch (error) {
            console.error('Failed to initialize ingestion:', error.message);
            return BINARY_PROOF.DOESNT_WORK;
        }
    }

    /**
     * Initialize processing module
     */
    async initializeProcessing() {
        this.recordTrace('Processing', 'Processing module initialized');
        console.log('Processing module ready');
        return BINARY_PROOF.WORKS;
    }

    /**
     * Initialize export module
     */
    async initializeExport() {
        this.recordTrace('Export Ready', 'Export module initialized');
        console.log('Export module ready');
        return BINARY_PROOF.WORKS;
    }

    /**
     * Initialize UI module
     */
    async initializeUI() {
        this.recordTrace('UI Render', 'UI module initialized');
        console.log('UI module ready');
        return BINARY_PROOF.WORKS;
    }

    /**
     * Main application flow
     */
    async run() {
        console.log('='.repeat(60));
        console.log('SOS Assessment Automation Tool v4.2');
        console.log(`Session ID: ${this.sessionId}`);
        console.log(`Trust Level: ${this.trustLevel}%`);
        console.log('='.repeat(60));

        // Load configuration
        const configResult = await this.loadConfig();
        if (configResult === BINARY_PROOF.DOESNT_WORK) {
            console.error('Failed to load configuration. Exiting.');
            process.exit(1);
        }

        // Initialize modules
        const modules = [
            { name: 'Ingestion', init: () => this.initializeIngestion() },
            { name: 'Processing', init: () => this.initializeProcessing() },
            { name: 'Export', init: () => this.initializeExport() },
            { name: 'UI', init: () => this.initializeUI() }
        ];

        for (const module of modules) {
            console.log(`\nInitializing ${module.name} module...`);
            const result = await module.init();
            if (result === BINARY_PROOF.DOESNT_WORK) {
                console.error(`${module.name} module initialization failed`);
                this.recordTrace('Complete', `Failed at ${module.name}`);
                return BINARY_PROOF.DOESNT_WORK;
            }
        }

        this.recordTrace('Complete', 'All modules initialized successfully');

        // Save trace log
        await this.saveTraceLog();

        console.log('\n' + '='.repeat(60));
        console.log('BINARY PROOF:', BINARY_PROOF.WORKS);
        console.log('System ready for operation');
        console.log('='.repeat(60));

        return BINARY_PROOF.WORKS;
    }

    /**
     * Save trace log to file
     */
    async saveTraceLog() {
        const tracePath = path.join(
            __dirname, '..', 'qa', 'session-traces',
            `trace-${this.sessionId}.json`
        );
        
        try {
            await fs.writeFile(
                tracePath,
                JSON.stringify(this.tracePoints, null, 2)
            );
            console.log(`Trace log saved: ${tracePath}`);
        } catch (error) {
            console.error('Failed to save trace log:', error.message);
        }
    }
}

/**
 * Parse command line arguments
 */
function parseArgs() {
    const args = process.argv.slice(2);
    const params = {};
    
    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--file' && args[i + 1]) {
            params.file = args[i + 1];
            i++;
        } else if (args[i] === '--session' && args[i + 1]) {
            params.session = args[i + 1];
            i++;
        }
    }
    
    return params;
}

/**
 * CLI orchestration flow
 */
async function runCLI() {
    const args = parseArgs();
    
    // Validate required arguments
    if (!args.file) {
        console.error('Error: --file argument required');
        console.error('Usage: node src/main.js --file "<path>" --session "<id>"');
        process.exit(1);
    }
    
    // Initialize session
    const sessionManager = new SessionManager();
    const sessionId = sessionManager.createSession(args.session);
    
    console.log('='.repeat(60));
    console.log('SOS Assessment Automation Tool - CLI Mode');
    console.log(`Session: ${sessionId}`);
    console.log(`Trust Level: ${sessionManager.trustLevel}%`);
    console.log('='.repeat(60));
    
    try {
        // Step 1: Read document
        console.log('\n[1/3] Reading document...');
        sessionManager.recordTrace('Data Attach', `Reading file: ${args.file}`);
        
        const reader = new DocumentReader();
        const document = await reader.read(args.file);
        
        if (document.status === 'DOESN\'T WORK') {
            throw new Error(`Document read failed: ${document.error}`);
        }
        
        console.log(`✓ Document read: ${document.metadata.fileName}`);
        
        // Step 2: Process through pipeline
        console.log('\n[2/3] Processing through assessment pipeline...');
        sessionManager.recordProcessingTrace('pipeline-start', {
            fileName: document.metadata.fileName,
            fileType: document.metadata.fileType
        });
        
        const pipeline = new ProcessingPipeline();
        const decision = await pipeline.process(document);
        
        sessionManager.recordProcessingTrace('pipeline-complete', {
            recommendation: decision.recommendation,
            confidence: decision.confidence
        });
        
        console.log(`✓ Assessment complete: ${decision.recommendation} (${decision.confidence}% confidence)`);
        
        // Step 3: Export decision
        console.log('\n[3/3] Exporting decision...');
        sessionManager.recordTrace('Export Ready', 'Writing decision to file');
        
        const writer = new DecisionWriter();
        const exportResult = await writer.write(decision, sessionId);
        
        if (exportResult.status === 'DOESN\'T WORK') {
            throw new Error(`Export failed: ${exportResult.error}`);
        }
        
        console.log(`✓ Decision exported: ${exportResult.fileName}`);
        
        // Complete session
        sessionManager.completeSession();
        await sessionManager.saveTraces();
        
        // Output final JSON result
        const result = {
            status: BINARY_PROOF.WORKS,
            sessionId,
            file: args.file,
            decision: {
                recommendation: decision.recommendation,
                rationale: decision.rationale,
                confidence: decision.confidence
            },
            export: {
                path: exportResult.path,
                fileName: exportResult.fileName
            },
            traces: sessionManager.traces.map(t => t.point)
        };
        
        console.log('\n' + '='.repeat(60));
        console.log('RESULT:');
        console.log(JSON.stringify(result, null, 2));
        console.log('='.repeat(60));
        
        return result;
        
    } catch (error) {
        sessionManager.recordTrace('Error', error.message);
        await sessionManager.saveTraces();
        
        const result = {
            status: BINARY_PROOF.DOESNT_WORK,
            sessionId,
            error: error.message
        };
        
        console.error('\n' + '='.repeat(60));
        console.error('ERROR:');
        console.error(JSON.stringify(result, null, 2));
        console.error('='.repeat(60));
        
        process.exit(1);
    }
}

// Execute if run directly
if (require.main === module) {
    // Check if CLI mode (has --file argument)
    if (process.argv.includes('--file')) {
        runCLI().then(() => {
            process.exit(0);
        }).catch(error => {
            console.error('Fatal error:', error);
            process.exit(1);
        });
    } else {
        // Original interactive mode
        const app = new SOSAssessmentTool();
        app.run().then(result => {
            if (result === BINARY_PROOF.DOESNT_WORK) {
                process.exit(1);
            }
        }).catch(error => {
            console.error('Unexpected error:', error);
            process.exit(1);
        });
    }
}

module.exports = { SOSAssessmentTool, runCLI };