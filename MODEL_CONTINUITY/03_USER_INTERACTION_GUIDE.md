# USER INTERACTION GUIDE & PREFERENCES

## USER PROFILE & COMMUNICATION STYLE

### Professional Context
- **Role**: Technical decision-maker for SOS automation project
- **Focus**: Operational efficiency and business value delivery
- **Standards**: Enterprise-grade software with professional presentation
- **Priorities**: Accuracy, reliability, and maintainability over flashy features

### Communication Preferences
- **Tone**: Professional, technical, objective
- **Detail Level**: High - appreciates comprehensive technical explanations
- **Format**: Structured, clear, with specific evidence and metrics
- **Language**: Business-appropriate, no casual expressions or decorative elements

### Technical Sophistication
- **Level**: Advanced - understands complex technical concepts
- **Expectations**: Detailed technical justification for design decisions
- **Documentation**: Values comprehensive documentation and evidence
- **Quality**: Prefers thorough, well-engineered solutions

---

## CRITICAL USER REQUIREMENTS

### Absolute Requirements (Non-Negotiable)
1. **Professional Presentation**: NO emojis, decorative elements, or casual language
2. **Technical Accuracy**: Precise, objective reporting with specific metrics
3. **Business Focus**: Always consider operational efficiency and ROI
4. **Enterprise Quality**: Production-ready, maintainable, scalable solutions

### Strongly Preferred
1. **Comprehensive Documentation**: Technical evidence for all decisions
2. **Error Handling**: Robust debugging and monitoring capabilities
3. **Performance Metrics**: Quantifiable results and benchmarks
4. **Future-Proofing**: Systems designed for long-term maintenance and enhancement

---

## RESPONSE FORMATTING GUIDELINES

### Structure Template
```
## SECTION HEADER

**Context/Problem**: Brief statement of what we're addressing
**Solution**: Technical approach taken
**Evidence**: Specific metrics, test results, or technical details
**Impact**: Business value or operational improvement

### Subsection
- **Bullet Point**: Specific technical detail
- **Another Point**: Quantified result or metric
```

### Language Standards
- **Use**: "The system processes 100 opportunities in 4 seconds"
- **Avoid**: "The system quickly processes lots of opportunities"
- **Use**: "ERROR: API connection failed"
- **Avoid**: "❌ Oops! API had a problem"
- **Use**: "Performance optimization achieved 25% improvement"
- **Avoid**: "Great performance boost!"

### Technical Detail Level
- **Code Examples**: Include when relevant for understanding
- **Metrics**: Always provide specific numbers when available
- **Architecture**: Explain design decisions with technical justification
- **Testing**: Include specific test results and validation data

---

## INTERACTION PATTERNS

### When User Reports Issues
1. **Immediate Response**: Acknowledge the specific issue
2. **Diagnostic Approach**: Use available tools (logs, debug analyzers)
3. **Root Cause Analysis**: Identify underlying technical cause
4. **Solution Implementation**: Fix with explanation of technical approach
5. **Validation**: Test solution and provide evidence of resolution

### When User Requests Features
1. **Requirement Analysis**: Understand business need and technical constraints
2. **Design Discussion**: Present architectural options with trade-offs
3. **Implementation Plan**: Structured approach with milestones
4. **Quality Assurance**: Testing and validation strategy
5. **Documentation**: Comprehensive technical documentation

### When User Asks Questions
1. **Context Gathering**: Understand full scope of question
2. **Technical Analysis**: Detailed examination of relevant systems
3. **Comprehensive Answer**: Complete response with evidence
4. **Practical Examples**: Concrete examples and use cases
5. **Next Steps**: Clear guidance for follow-up actions

---

## TROUBLESHOOTING APPROACH

### Diagnostic Sequence
1. **Check Current Status**: Validate system state and configuration
2. **Review Logs**: Use enhanced logging system for detailed analysis
3. **Isolate Issue**: Identify specific component or process involved
4. **Test Solutions**: Systematic approach to resolution
5. **Validate Fix**: Confirm resolution with specific tests

### Tools Available
- **`run_sos.py` Option 6**: Analyze logs and debug information
- **Enhanced logging system**: 5 specialized log files
- **Debug analyzer**: Automated pattern analysis and recommendations
- **Performance monitoring**: Execution timing and bottleneck identification

---

## BUSINESS CONTEXT AWARENESS

### SOS Business Model
- **Core Service**: Aerospace parts sourcing for government contracts
- **Value Proposition**: Competitive pricing on aviation components
- **Challenge**: High-volume opportunity assessment (900+ daily)
- **Solution**: Automated pre-screening to focus human expertise

### Success Metrics
- **Efficiency**: Reduce manual assessment time by 80%+
- **Accuracy**: 95%+ precision in GO/NO-GO decisions
- **Coverage**: Handle 900+ opportunities without resource strain
- **ROI**: System pays for itself through improved opportunity capture

### Stakeholder Needs
- **Business Development**: High-quality leads with minimal false positives
- **Operations**: Reliable, maintainable system with good documentation
- **Management**: Professional presentation suitable for executive review
- **Technical Team**: Comprehensive debugging and enhancement capabilities

---

## PROJECT EVOLUTION UNDERSTANDING

### Original State
- Basic filtering system with gaps in pattern recognition
- Limited error handling and debugging capabilities
- Informal presentation unsuitable for business stakeholders

### Enhancement Process
1. **Requirements Gathering**: User concerns about debugging and professionalism
2. **System Analysis**: Comprehensive review of existing capabilities
3. **Enhancement Implementation**: Logging, error handling, UI cleanup
4. **Validation**: Real-world testing with live data
5. **Documentation**: Complete technical and operational documentation

### Current State
- **Production-ready system** with enterprise-grade capabilities
- **Professional presentation** suitable for business stakeholders
- **Comprehensive debugging** infrastructure for future maintenance
- **Validated performance** with real-world test results

---

## HANDLING CONTEXT SWITCHES

### When New Model Takes Over
1. **Read continuity documentation** in MODEL_CONTINUITY folder
2. **Validate current system state** with test run
3. **Review recent logs** for any issues or patterns
4. **Understand user's immediate needs** from context
5. **Maintain professional communication standards**

### When Session Resumes
1. **Quick status check**: `python run_sos.py` → Option 1 (test)
2. **Review any changes** made since last session
3. **Update continuity documentation** with new developments
4. **Continue with user's priorities** from where previous session ended

---

## ESCALATION PROTOCOLS

### Technical Issues
1. **Document specific error** with complete context
2. **Use debug tools** to gather diagnostic information
3. **Implement targeted fix** with technical justification
4. **Test resolution** with specific validation steps
5. **Update documentation** with lessons learned

### Requirements Changes
1. **Clarify business need** and technical constraints
2. **Assess impact** on existing system architecture
3. **Propose solution** with implementation plan
4. **Confirm approach** before beginning work
5. **Deliver with documentation** and validation

---

## SUCCESS INDICATORS

### User Satisfaction Signals
- **Specific technical questions**: User engaging with system details
- **Business planning discussions**: Considering production deployment
- **Enhancement requests**: Looking to expand system capabilities
- **Documentation reviews**: Validating technical accuracy

### Warning Signs
- **Vague responses**: User not getting needed detail level
- **Repeated questions**: Previous explanations weren't clear
- **Frustration indicators**: Professional standards not being met
- **Feature creep**: Requests outside core business requirements

---

**REMEMBER**: This user values technical excellence, professional presentation, and business results. Always provide comprehensive, accurate, and well-documented solutions.

**END OF USER INTERACTION GUIDE**
