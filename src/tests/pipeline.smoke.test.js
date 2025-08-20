/**
 * Pipeline Smoke Test
 * Validates basic end-to-end pipeline functionality
 * Part of SOS Assessment Automation Tool v4.2
 */

const assert = require('assert');
const path = require('path');
const fs = require('fs');

// Import modules to test
const DocumentReader = require('../ingestion/reader');
const ProcessingPipeline = require('../processing/pipeline');
const DecisionWriter = require('../export/writer');
const SessionManager = require('../core/session');

/**
 * Smoke test suite for processing pipeline
 */
class PipelineSmokeTest {
    constructor() {
        this.testResults = [];
        this.sessionId = `test-${Date.now()}`;
    }

    /**
     * Run all smoke tests
     */
    async runAll() {
        console.log('='.repeat(60));
        console.log('PIPELINE SMOKE TEST');
        console.log('='.repeat(60));
        
        try {
            await this.testEndToEndPipeline();
            await this.testDecisionShape();
            await this.testExportFile();
            
            this.printSummary();
            return this.testResults.every(r => r.passed);
            
        } catch (error) {
            console.error('Test suite error:', error);
            return false;
        }
    }

    /**
     * Test 1: End-to-end pipeline execution
     */
    async testEndToEndPipeline() {
        const testName = 'End-to-end pipeline';
        
        try {
            // Setup
            const fixturePath = path.join(__dirname, '..', '..', 'fixtures', 'sample.txt');
            const sessionManager = new SessionManager();
            const sessionId = sessionManager.createSession(this.sessionId);
            
            // Read document
            const reader = new DocumentReader();
            const document = await reader.read(fixturePath);
            assert.strictEqual(document.status, 'WORKS', 'Document read failed');
            
            // Process through pipeline
            const pipeline = new ProcessingPipeline();
            const decision = await pipeline.process(document);
            assert.strictEqual(decision.status, 'WORKS', 'Pipeline processing failed');
            
            // Export decision
            const writer = new DecisionWriter();
            const exportResult = await writer.write(decision, sessionId);
            assert.strictEqual(exportResult.status, 'WORKS', 'Export failed');
            
            // Complete session
            sessionManager.completeSession();
            
            this.testResults.push({
                name: testName,
                passed: true,
                details: `Pipeline executed successfully for ${document.metadata.fileName}`
            });
            
            console.log(`✓ ${testName}`);
            
        } catch (error) {
            this.testResults.push({
                name: testName,
                passed: false,
                error: error.message
            });
            console.log(`✗ ${testName}: ${error.message}`);
        }
    }

    /**
     * Test 2: Decision object shape validation
     */
    async testDecisionShape() {
        const testName = 'Decision object structure';
        
        try {
            const fixturePath = path.join(__dirname, '..', '..', 'fixtures', 'sample.txt');
            
            // Read and process
            const reader = new DocumentReader();
            const document = await reader.read(fixturePath);
            
            const pipeline = new ProcessingPipeline();
            const decision = await pipeline.process(document);
            
            // Validate decision shape
            assert(decision.recommendation, 'Missing recommendation');
            assert(decision.rationale, 'Missing rationale');
            assert(typeof decision.confidence === 'number', 'Missing or invalid confidence');
            assert(Array.isArray(decision.nextSteps), 'Missing or invalid nextSteps');
            
            // Validate recommendation is one of expected values
            const validRecommendations = ['Go', 'No-Go', 'Further Analysis'];
            assert(
                validRecommendations.includes(decision.recommendation),
                `Invalid recommendation: ${decision.recommendation}`
            );
            
            this.testResults.push({
                name: testName,
                passed: true,
                details: `Decision shape valid: ${decision.recommendation}`
            });
            
            console.log(`✓ ${testName}`);
            
        } catch (error) {
            this.testResults.push({
                name: testName,
                passed: false,
                error: error.message
            });
            console.log(`✗ ${testName}: ${error.message}`);
        }
    }

    /**
     * Test 3: Export file creation
     */
    async testExportFile() {
        const testName = 'Export file creation';
        
        try {
            const fixturePath = path.join(__dirname, '..', '..', 'fixtures', 'sample.txt');
            const testSessionId = `smoke-test-${Date.now()}`;
            
            // Process fixture
            const reader = new DocumentReader();
            const document = await reader.read(fixturePath);
            
            const pipeline = new ProcessingPipeline();
            const decision = await pipeline.process(document);
            
            // Export
            const writer = new DecisionWriter();
            const exportResult = await writer.write(decision, testSessionId);
            
            // Verify file exists
            assert(fs.existsSync(exportResult.path), 'Export file not created');
            
            // Verify file content
            const content = fs.readFileSync(exportResult.path, 'utf8');
            const exportedData = JSON.parse(content);
            
            assert.strictEqual(
                exportedData.recommendation,
                decision.recommendation,
                'Exported recommendation mismatch'
            );
            
            // Clean up test file
            fs.unlinkSync(exportResult.path);
            
            this.testResults.push({
                name: testName,
                passed: true,
                details: `File created and verified: ${exportResult.fileName}`
            });
            
            console.log(`✓ ${testName}`);
            
        } catch (error) {
            this.testResults.push({
                name: testName,
                passed: false,
                error: error.message
            });
            console.log(`✗ ${testName}: ${error.message}`);
        }
    }

    /**
     * Print test summary
     */
    printSummary() {
        console.log('\n' + '='.repeat(60));
        
        const passed = this.testResults.filter(r => r.passed).length;
        const failed = this.testResults.filter(r => !r.passed).length;
        const total = this.testResults.length;
        
        console.log(`Tests: ${passed} passed, ${failed} failed, ${total} total`);
        
        if (failed === 0) {
            console.log('BINARY PROOF: WORKS');
        } else {
            console.log('BINARY PROOF: DOESN\'T WORK');
            console.log('\nFailed tests:');
            this.testResults
                .filter(r => !r.passed)
                .forEach(r => console.log(`  - ${r.name}: ${r.error}`));
        }
        
        console.log('='.repeat(60));
    }
}

// Run if executed directly
if (require.main === module) {
    const test = new PipelineSmokeTest();
    test.runAll().then(success => {
        process.exit(success ? 0 : 1);
    });
}

module.exports = PipelineSmokeTest;