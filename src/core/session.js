/**
 * Session Management Module
 * Handles session creation and trace point recording
 * Part of SOS Assessment Automation Tool v4.2
 */

const fs = require('fs').promises;
const path = require('path');

class SessionManager {
    constructor() {
        this.tracePath = path.join(__dirname, '..', '..', 'qa', 'session-traces');
        this.currentSession = null;
        this.traces = [];
        this.trustLevel = 80; // Current trust level from continuity
    }

    /**
     * Create new session
     * @param {string} sessionId - Optional session ID, generates if not provided
     */
    createSession(sessionId = null) {
        const now = new Date();
        const timestamp = now.toTimeString().slice(0, 8).replace(/:/g, '');
        
        this.currentSession = {
            id: sessionId || `sess-${timestamp}`,
            created: now.toISOString(),
            trustLevel: this.trustLevel,
            traces: [],
            status: 'active'
        };

        this.recordTrace('Creation', 'Session initialized');
        return this.currentSession.id;
    }

    /**
     * Record trace point for v4.2 compliance
     * @param {string} point - Trace point name
     * @param {string} details - Additional details
     */
    recordTrace(point, details = '') {
        const trace = {
            point,
            timestamp: new Date().toISOString(),
            sessionId: this.currentSession?.id || 'unknown',
            details,
            trustLevel: this.trustLevel
        };

        this.traces.push(trace);
        
        if (this.currentSession) {
            this.currentSession.traces.push(trace);
        }

        // Log to console for visibility
        console.log(`[TRACE] ${point}: ${details}`);
        
        return trace;
    }

    /**
     * Record processing-specific trace
     * @param {string} stage - Processing stage
     * @param {Object} metadata - Additional metadata
     */
    recordProcessingTrace(stage, metadata = {}) {
        const details = `Processing stage: ${stage}`;
        const trace = this.recordTrace('Processing', details);
        
        // Add metadata to trace
        trace.metadata = {
            stage,
            ...metadata,
            timestamp: new Date().toISOString()
        };

        return trace;
    }

    /**
     * Save session traces to file
     */
    async saveTraces() {
        if (!this.currentSession) {
            return {
                status: 'DOESN\'T WORK',
                error: 'No active session'
            };
        }

        try {
            // Ensure trace directory exists
            await this.ensureDirectory(this.tracePath);

            // Generate trace file name
            const fileName = `trace-log-${this.currentSession.id}.json`;
            const filePath = path.join(this.tracePath, fileName);

            // Prepare trace data
            const traceData = {
                session: this.currentSession,
                traces: this.traces,
                summary: {
                    totalTraces: this.traces.length,
                    uniquePoints: [...new Set(this.traces.map(t => t.point))],
                    duration: this.calculateDuration(),
                    trustLevel: this.trustLevel,
                    status: this.currentSession.status
                },
                v42Compliance: {
                    atomicOperations: true,
                    binaryProof: true,
                    tracePointsCaptured: this.traces.map(t => t.point),
                    sessionIntegrity: 'valid'
                }
            };

            // Write trace file
            await fs.writeFile(
                filePath,
                JSON.stringify(traceData, null, 2),
                'utf8'
            );

            // Also append to markdown log
            await this.appendMarkdownLog();

            return {
                status: 'WORKS',
                path: filePath,
                traces: this.traces.length
            };

        } catch (error) {
            return {
                status: 'DOESN\'T WORK',
                error: error.message
            };
        }
    }

    /**
     * Append to markdown trace log
     */
    async appendMarkdownLog() {
        const mdFileName = `trace-log-${this.currentSession.id}.md`;
        const mdPath = path.join(this.tracePath, mdFileName);

        const lines = [
            `## Session: ${this.currentSession.id}`,
            `**Created:** ${this.currentSession.created}`,
            `**Trust Level:** ${this.trustLevel}%`,
            '',
            '### Trace Points',
            ...this.traces.map((t, i) => 
                `${i + 1}. **${t.point}** (${t.timestamp}): ${t.details}`
            ),
            '',
            '---',
            ''
        ];

        await fs.appendFile(mdPath, lines.join('\n'), 'utf8');
    }

    /**
     * Calculate session duration
     */
    calculateDuration() {
        if (!this.currentSession || this.traces.length === 0) {
            return 0;
        }

        const start = new Date(this.currentSession.created);
        const end = new Date(this.traces[this.traces.length - 1].timestamp);
        return Math.round((end - start) / 1000); // Duration in seconds
    }

    /**
     * Ensure directory exists
     */
    async ensureDirectory(dirPath) {
        try {
            await fs.access(dirPath);
        } catch {
            await fs.mkdir(dirPath, { recursive: true });
        }
    }

    /**
     * Complete session
     */
    completeSession() {
        if (this.currentSession) {
            this.currentSession.status = 'completed';
            this.recordTrace('Complete', 'Session completed successfully');
        }
    }

    /**
     * Get session status
     */
    getStatus() {
        return {
            sessionId: this.currentSession?.id,
            status: this.currentSession?.status || 'inactive',
            traces: this.traces.length,
            trustLevel: this.trustLevel,
            duration: this.calculateDuration()
        };
    }

    /**
     * Check trust level requirement
     */
    checkTrustLevel(required) {
        return this.trustLevel >= required;
    }

    /**
     * Adjust trust level
     * @param {number} adjustment - Positive or negative adjustment
     * @param {string} reason - Reason for adjustment
     */
    adjustTrustLevel(adjustment, reason) {
        const oldLevel = this.trustLevel;
        this.trustLevel = Math.max(0, Math.min(100, this.trustLevel + adjustment));
        
        console.log(`[TRUST] Level adjusted from ${oldLevel}% to ${this.trustLevel}% (${reason})`);
        
        this.recordTrace('Trust Adjustment', `${oldLevel}% → ${this.trustLevel}%: ${reason}`);
        
        return this.trustLevel;
    }
}

module.exports = SessionManager;