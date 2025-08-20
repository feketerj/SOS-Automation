/**
 * Scaffold Validation Tests
 * 
 * Validates that the project scaffolding is correctly implemented
 * per architecture.md specifications and v4.2 SOP compliance.
 */

const fs = require('fs');
const path = require('path');
const assert = require('assert');

// Test configuration
const PROJECT_ROOT = path.join(__dirname, '..', '..');
const SRC_ROOT = path.join(PROJECT_ROOT, 'src');
const BINARY_PROOF = { WORKS: 'WORKS', DOESNT_WORK: 'DOESN\'T WORK' };

/**
 * Test suite for scaffolding validation
 */
class ScaffoldTest {
    constructor() {
        this.tests = [];
        this.results = [];
    }

    /**
     * Add a test to the suite
     */
    addTest(name, testFn) {
        this.tests.push({ name, testFn });
    }

    /**
     * Run all tests
     */
    async runAll() {
        console.log('='.repeat(60));
        console.log('SCAFFOLD VALIDATION TEST SUITE');
        console.log('='.repeat(60));

        for (const test of this.tests) {
            try {
                await test.testFn();
                this.results.push({ name: test.name, status: 'PASS' });
                console.log(`✓ ${test.name}`);
            } catch (error) {
                this.results.push({ name: test.name, status: 'FAIL', error: error.message });
                console.log(`✗ ${test.name}: ${error.message}`);
            }
        }

        return this.printSummary();
    }

    /**
     * Print test summary
     */
    printSummary() {
        console.log('\n' + '='.repeat(60));
        const passed = this.results.filter(r => r.status === 'PASS').length;
        const failed = this.results.filter(r => r.status === 'FAIL').length;
        
        console.log(`Tests: ${passed} passed, ${failed} failed, ${this.tests.length} total`);
        
        if (failed === 0) {
            console.log(`BINARY PROOF: ${BINARY_PROOF.WORKS}`);
            return true;
        } else {
            console.log(`BINARY PROOF: ${BINARY_PROOF.DOESNT_WORK}`);
            return false;
        }
    }
}

// Initialize test suite
const suite = new ScaffoldTest();

// Test 1: Verify directory structure
suite.addTest('Directory structure exists', () => {
    const requiredDirs = [
        'src/core',
        'src/ingestion',
        'src/processing',
        'src/export',
        'src/ui',
        'src/config',
        'src/tests'
    ];

    for (const dir of requiredDirs) {
        const fullPath = path.join(PROJECT_ROOT, dir);
        assert(fs.existsSync(fullPath), `Missing directory: ${dir}`);
    }
});

// Test 2: Verify README files
suite.addTest('Module README files exist', () => {
    const modules = ['core', 'ingestion', 'processing', 'export', 'ui', 'config', 'tests'];
    
    for (const module of modules) {
        const readmePath = path.join(SRC_ROOT, module, 'README.md');
        assert(fs.existsSync(readmePath), `Missing README: ${module}/README.md`);
        
        // Verify README contains architecture reference
        const content = fs.readFileSync(readmePath, 'utf8');
        assert(content.includes('architecture.md'), `README missing architecture reference: ${module}`);
    }
});

// Test 3: Verify entry points
suite.addTest('Entry point files exist', () => {
    const entryPoints = [
        'src/main.js',
        'src/config/default.json',
        'src/tests/scaffold.test.js'
    ];

    for (const file of entryPoints) {
        const fullPath = path.join(PROJECT_ROOT, file);
        assert(fs.existsSync(fullPath), `Missing entry point: ${file}`);
    }
});

// Test 4: Verify architecture.md
suite.addTest('Architecture specification exists', () => {
    const archPath = path.join(PROJECT_ROOT, 'architecture.md');
    assert(fs.existsSync(archPath), 'Missing architecture.md');
    
    const content = fs.readFileSync(archPath, 'utf8');
    const lines = content.split('\n').length;
    assert(lines >= 500, `Architecture.md too short: ${lines} lines (minimum 500)`);
});

// Test 5: Verify v4.2 compliance files
suite.addTest('v4.2 compliance structure', () => {
    const requiredFiles = [
        'ops/state.md',
        'qa/session-traces',
        'continuity'
    ];

    for (const file of requiredFiles) {
        const fullPath = path.join(PROJECT_ROOT, file);
        assert(fs.existsSync(fullPath), `Missing v4.2 structure: ${file}`);
    }
});

// Test 6: Verify configuration
suite.addTest('Configuration is valid JSON', () => {
    const configPath = path.join(SRC_ROOT, 'config', 'default.json');
    const configContent = fs.readFileSync(configPath, 'utf8');
    
    try {
        const config = JSON.parse(configContent);
        assert(config.application, 'Missing application config');
        assert(config.v42_compliance, 'Missing v4.2 compliance config');
        assert(config.ingestion, 'Missing ingestion config');
        assert(config.processing, 'Missing processing config');
        assert(config.export, 'Missing export config');
        assert(config.ui, 'Missing UI config');
    } catch (error) {
        throw new Error(`Invalid JSON configuration: ${error.message}`);
    }
});

// Test 7: Verify main.js structure
suite.addTest('Main entry point is valid', () => {
    const mainPath = path.join(SRC_ROOT, 'main.js');
    const content = fs.readFileSync(mainPath, 'utf8');
    
    // Check for required components
    assert(content.includes('SOSAssessmentTool'), 'Missing SOSAssessmentTool class');
    assert(content.includes('generateSessionId'), 'Missing session ID generation');
    assert(content.includes('recordTrace'), 'Missing trace recording');
    assert(content.includes('BINARY_PROOF'), 'Missing binary proof constants');
    assert(content.includes('trustLevel'), 'Missing trust level management');
});

// Test 8: Verify Git repository
suite.addTest('Git repository is initialized', () => {
    const gitPath = path.join(PROJECT_ROOT, '.git');
    assert(fs.existsSync(gitPath), 'Git repository not initialized');
});

// Test 9: Verify ingestion pipeline
suite.addTest('Ingestion pipeline exists', () => {
    const pipelinePath = path.join(SRC_ROOT, 'ingestion_pipeline.py');
    assert(fs.existsSync(pipelinePath), 'Missing ingestion_pipeline.py');
    
    const content = fs.readFileSync(pipelinePath, 'utf8');
    assert(content.includes('IngestionPipeline'), 'Missing IngestionPipeline class');
    assert(content.includes('ingest_file'), 'Missing ingest_file method');
});

// Test 10: Verify ops state
suite.addTest('Ops state is properly configured', () => {
    const statePath = path.join(PROJECT_ROOT, 'ops', 'state.md');
    const content = fs.readFileSync(statePath, 'utf8');
    
    assert(content.includes('Phase: 0'), 'Incorrect phase in state.md');
    assert(content.includes('Trust Level: 80%'), 'Incorrect trust level in state.md');
    assert(content.includes('OPERATIONAL'), 'Terminal status not operational');
});

// Run tests if executed directly
if (require.main === module) {
    suite.runAll().then(success => {
        process.exit(success ? 0 : 1);
    }).catch(error => {
        console.error('Test suite error:', error);
        process.exit(1);
    });
}

module.exports = ScaffoldTest;