/**
 * Processing Pipeline Module
 * Runs SOS Initial Checklist assessment on normalized documents
 * Part of SOS Assessment Automation Tool v4.2
 */

class ProcessingPipeline {
    constructor() {
        this.rules = this.initializeRules();
    }

    /**
     * Initialize assessment rules (SOS Initial Checklist placeholders)
     */
    initializeRules() {
        return [
            {
                id: 'rule_001',
                name: 'Source Approval Required (SAR)',
                check: (doc) => {
                    // TODO: Implement comprehensive SAR pattern matching
                    const sarPatterns = /source approval|SAR|approved vendor|qualified supplier/i;
                    return sarPatterns.test(doc.content.raw);
                },
                weight: 'critical',
                noGoTrigger: true
            },
            {
                id: 'rule_002', 
                name: 'Commercial Item Check',
                check: (doc) => {
                    // TODO: Implement commercial item detection
                    const commercialPatterns = /commercial item|COTS|commercial off-the-shelf|FAR Part 12/i;
                    return commercialPatterns.test(doc.content.raw);
                },
                weight: 'high',
                noGoTrigger: false
            },
            {
                id: 'rule_003',
                name: 'Set-Aside Detection',
                check: (doc) => {
                    // TODO: Implement set-aside detection
                    const setAsidePatterns = /small business set-aside|8\(a\)|SDVOSB|WOSB|HUBZone/i;
                    return setAsidePatterns.test(doc.content.raw);
                },
                weight: 'medium',
                noGoTrigger: false
            },
            {
                id: 'rule_004',
                name: 'OEM Restriction',
                check: (doc) => {
                    // TODO: Implement OEM restriction detection
                    const oemPatterns = /OEM only|original equipment manufacturer|brand name only/i;
                    return oemPatterns.test(doc.content.raw);
                },
                weight: 'critical',
                noGoTrigger: true
            },
            {
                id: 'rule_005',
                name: 'Technical Data Package',
                check: (doc) => {
                    // TODO: Implement TDP availability check
                    const tdpPatterns = /technical data package|TDP|drawings available|specifications provided/i;
                    return tdpPatterns.test(doc.content.raw);
                },
                weight: 'high',
                noGoTrigger: false
            },
            {
                id: 'rule_006',
                name: 'Contract Value Assessment',
                check: (doc) => {
                    // TODO: Implement value threshold check
                    const valueMatch = doc.content.raw.match(/\$[\d,]+/);
                    if (valueMatch) {
                        const value = parseInt(valueMatch[0].replace(/[$,]/g, ''));
                        return value > 25000; // Simplified threshold
                    }
                    return false;
                },
                weight: 'low',
                noGoTrigger: false
            }
        ];
    }

    /**
     * Process document through assessment pipeline
     * @param {Object} document - Normalized document from reader
     * @returns {Object} Decision object with recommendation and rationale
     */
    async process(document) {
        if (document.status === 'DOESN\'T WORK') {
            return {
                status: 'DOESN\'T WORK',
                error: 'Invalid document input',
                recommendation: 'Error',
                rationale: 'Document could not be processed'
            };
        }

        // Run rules
        const results = [];
        let noGoTriggered = false;
        let criticalIssues = [];
        let opportunities = [];

        for (const rule of this.rules) {
            const passed = rule.check(document);
            results.push({
                ruleId: rule.id,
                ruleName: rule.name,
                passed,
                weight: rule.weight
            });

            if (!passed && rule.noGoTrigger) {
                noGoTriggered = true;
                criticalIssues.push(rule.name);
            }

            if (passed && rule.weight === 'high') {
                opportunities.push(rule.name);
            }
        }

        // Determine recommendation
        let recommendation;
        let rationale;

        if (noGoTriggered) {
            recommendation = 'No-Go';
            rationale = `Critical issues detected: ${criticalIssues.join(', ')}. This opportunity has restrictions that prevent pursuit.`;
        } else if (opportunities.length > 0) {
            recommendation = 'Go';
            rationale = `Opportunity identified with favorable conditions: ${opportunities.join(', ')}. Recommend proceeding with assessment.`;
        } else {
            recommendation = 'Further Analysis';
            rationale = 'No critical issues or clear opportunities detected. Additional review recommended to determine viability.';
        }

        // Build decision object
        const decision = {
            status: 'WORKS',
            timestamp: new Date().toISOString(),
            document: {
                fileName: document.metadata.fileName,
                fileType: document.metadata.fileType,
                processed: document.metadata.ingested
            },
            assessment: {
                rulesApplied: results.length,
                ruleResults: results,
                criticalIssues: criticalIssues.length,
                opportunities: opportunities.length
            },
            recommendation,
            rationale,
            confidence: this.calculateConfidence(results),
            nextSteps: this.determineNextSteps(recommendation)
        };

        return decision;
    }

    /**
     * Calculate confidence score based on rule results
     */
    calculateConfidence(results) {
        const total = results.length;
        const criticalRules = results.filter(r => r.weight === 'critical');
        const criticalPassed = criticalRules.filter(r => r.passed).length;
        
        if (criticalRules.length > 0) {
            return Math.round((criticalPassed / criticalRules.length) * 100);
        }
        
        const passed = results.filter(r => r.passed).length;
        return Math.round((passed / total) * 100);
    }

    /**
     * Determine next steps based on recommendation
     */
    determineNextSteps(recommendation) {
        switch (recommendation) {
            case 'Go':
                return [
                    'Download solicitation documents',
                    'Perform detailed technical review',
                    'Assess competitive landscape',
                    'Prepare bid/no-bid recommendation'
                ];
            case 'No-Go':
                return [
                    'Archive opportunity for reference',
                    'Document reasons for no-go',
                    'Monitor for potential changes'
                ];
            case 'Further Analysis':
                return [
                    'Request additional information',
                    'Contact contracting officer',
                    'Review similar past opportunities',
                    'Escalate for manual review'
                ];
            default:
                return ['Manual review required'];
        }
    }
}

module.exports = ProcessingPipeline;