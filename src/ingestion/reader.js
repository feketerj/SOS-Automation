/**
 * Document Reader Module
 * Reads a single file and emits a normalized document object
 * Part of SOS Assessment Automation Tool v4.2
 */

const fs = require('fs').promises;
const path = require('path');

class DocumentReader {
    constructor() {
        this.supportedTypes = ['.txt', '.json', '.csv', '.pdf', '.xlsx'];
    }

    /**
     * Read and normalize a document from file path
     * @param {string} filePath - Full path to document
     * @returns {Object} Normalized document object or error
     */
    async read(filePath) {
        try {
            // Validate file exists
            const stats = await fs.stat(filePath);
            if (!stats.isFile()) {
                return { 
                    status: 'DOESN\'T WORK', 
                    error: 'Path is not a file' 
                };
            }

            // Extract metadata
            const ext = path.extname(filePath).toLowerCase();
            const fileName = path.basename(filePath);
            
            // Check supported type
            if (!this.supportedTypes.includes(ext)) {
                return {
                    status: 'DOESN\'T WORK',
                    error: `Unsupported file type: ${ext}`
                };
            }

            // Read content
            const content = await fs.readFile(filePath, 'utf8');
            
            // Normalize document structure
            const document = {
                status: 'WORKS',
                metadata: {
                    filePath,
                    fileName,
                    fileType: ext,
                    size: stats.size,
                    modified: stats.mtime.toISOString(),
                    ingested: new Date().toISOString()
                },
                content: {
                    raw: content,
                    normalized: this.normalizeContent(content, ext),
                    lineCount: content.split('\n').length,
                    wordCount: content.split(/\s+/).filter(w => w.length > 0).length
                },
                analysis: {
                    hasContractLanguage: this.detectContractLanguage(content),
                    hasPricing: /\$[\d,]+/.test(content),
                    hasDeadline: /deadline|due date|response date/i.test(content),
                    hasNAICS: /NAICS:?\s*\d{6}/.test(content)
                }
            };

            return document;

        } catch (error) {
            return {
                status: 'DOESN\'T WORK',
                error: error.message
            };
        }
    }

    /**
     * Normalize content based on file type
     */
    normalizeContent(content, fileType) {
        switch (fileType) {
            case '.json':
                try {
                    return JSON.parse(content);
                } catch {
                    return content;
                }
            case '.csv':
                return content.split('\n').map(line => line.split(','));
            default:
                return content.trim();
        }
    }

    /**
     * Detect contract language indicators
     */
    detectContractLanguage(content) {
        const patterns = [
            /solicitation/i,
            /request for (proposal|quote|information)/i,
            /statement of work/i,
            /purchase order/i,
            /contract/i,
            /award/i
        ];
        return patterns.some(pattern => pattern.test(content));
    }
}

module.exports = DocumentReader;