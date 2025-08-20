/**
 * Decision Writer Module
 * Persists decision objects to export directory
 * Part of SOS Assessment Automation Tool v4.2
 */

const fs = require('fs').promises;
const path = require('path');

class DecisionWriter {
    constructor() {
        this.exportBase = path.join(__dirname, '..', '..', 'export', 'decisions');
    }

    /**
     * Write decision object to JSON file
     * @param {Object} decision - Decision object from pipeline
     * @param {string} sessionId - Session identifier
     * @returns {Object} Result with file path or error
     */
    async write(decision, sessionId) {
        try {
            // Ensure export directory exists
            await this.ensureDirectory(this.exportBase);

            // Generate filename
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
            const fileName = `${sessionId}_${timestamp}.json`;
            const filePath = path.join(this.exportBase, fileName);

            // Add export metadata
            const exportData = {
                ...decision,
                export: {
                    sessionId,
                    fileName,
                    exportPath: filePath,
                    exportedAt: new Date().toISOString(),
                    format: 'json',
                    version: '1.0.0'
                }
            };

            // Write to file
            await fs.writeFile(
                filePath,
                JSON.stringify(exportData, null, 2),
                'utf8'
            );

            // Return success result
            return {
                status: 'WORKS',
                path: filePath,
                fileName,
                size: JSON.stringify(exportData).length,
                message: `Decision exported successfully to ${fileName}`
            };

        } catch (error) {
            return {
                status: 'DOESN\'T WORK',
                error: error.message,
                message: 'Failed to export decision'
            };
        }
    }

    /**
     * Ensure directory exists, create if not
     */
    async ensureDirectory(dirPath) {
        try {
            await fs.access(dirPath);
        } catch {
            await fs.mkdir(dirPath, { recursive: true });
        }
    }

    /**
     * Generate summary report from decision
     * @param {Object} decision - Decision object
     * @returns {string} Text summary
     */
    generateSummary(decision) {
        const lines = [
            '='.repeat(60),
            'SOS ASSESSMENT DECISION SUMMARY',
            '='.repeat(60),
            `Timestamp: ${decision.timestamp}`,
            `File: ${decision.document.fileName}`,
            `Recommendation: ${decision.recommendation}`,
            `Confidence: ${decision.confidence}%`,
            '',
            'Rationale:',
            decision.rationale,
            '',
            'Next Steps:',
            ...decision.nextSteps.map((step, i) => `${i + 1}. ${step}`),
            '='.repeat(60)
        ];

        return lines.join('\n');
    }

    /**
     * Export decision in multiple formats
     * @param {Object} decision - Decision object
     * @param {string} sessionId - Session identifier
     * @param {Array} formats - Export formats ['json', 'txt', 'csv']
     */
    async exportMultiple(decision, sessionId, formats = ['json']) {
        const results = [];

        for (const format of formats) {
            switch (format) {
                case 'json':
                    results.push(await this.write(decision, sessionId));
                    break;
                case 'txt':
                    results.push(await this.writeText(decision, sessionId));
                    break;
                case 'csv':
                    results.push(await this.writeCSV(decision, sessionId));
                    break;
                default:
                    results.push({
                        status: 'DOESN\'T WORK',
                        error: `Unsupported format: ${format}`
                    });
            }
        }

        return results;
    }

    /**
     * Write text summary
     */
    async writeText(decision, sessionId) {
        try {
            await this.ensureDirectory(this.exportBase);
            
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
            const fileName = `${sessionId}_${timestamp}.txt`;
            const filePath = path.join(this.exportBase, fileName);
            
            const summary = this.generateSummary(decision);
            await fs.writeFile(filePath, summary, 'utf8');

            return {
                status: 'WORKS',
                path: filePath,
                fileName,
                format: 'txt'
            };
        } catch (error) {
            return {
                status: 'DOESN\'T WORK',
                error: error.message
            };
        }
    }

    /**
     * Write CSV row
     */
    async writeCSV(decision, sessionId) {
        try {
            await this.ensureDirectory(this.exportBase);
            
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
            const fileName = `${sessionId}_${timestamp}.csv`;
            const filePath = path.join(this.exportBase, fileName);
            
            const headers = 'SessionID,Timestamp,File,Recommendation,Confidence,Rationale';
            const row = [
                sessionId,
                decision.timestamp,
                decision.document.fileName,
                decision.recommendation,
                decision.confidence,
                `"${decision.rationale.replace(/"/g, '""')}"`
            ].join(',');
            
            await fs.writeFile(filePath, `${headers}\n${row}`, 'utf8');

            return {
                status: 'WORKS',
                path: filePath,
                fileName,
                format: 'csv'
            };
        } catch (error) {
            return {
                status: 'DOESN\'T WORK',
                error: error.message
            };
        }
    }
}

module.exports = DecisionWriter;