/**
 * PPTX Shape Grouping Module
 * 
 * Handles grouped shapes in PowerPoint presentations.
 * Groups are processed by sorting shapes spatially (top-to-bottom, left-to-right).
 * 
 * Features:
 * - Detect and process grouped shapes (p:grpSp)
 * - Sort shapes by spatial position
 * - Extract text from grouped shapes
 * - Statistics tracking
 * 
 * @class PPTXGroupHandler
 * @version 2.4.3
 * @date February 2026
 */

class PPTXGroupHandler {
    /**
     * Initialize group handler
     */
    constructor() {
        this.groups = [];
        this.totalShapesProcessed = 0;
    }

    /**
     * Process slide XML to find and handle groups
     * @param {string} slideXml - Slide XML content
     * @returns {Promise<Array>} Array of group objects
     */
    async processSlide(slideXml) {
        try {
            const xmlDoc = XMLHelper.parseXML(slideXml);
            
            // Find all group shapes
            const groups = this.findGroupShapes(xmlDoc);
            
            for (const group of groups) {
                const groupData = this.processGroup(group);
                if (groupData) {
                    this.groups.push(groupData);
                }
            }
            
            return this.groups;
        } catch (error) {
            console.error('[PPTXGroupHandler] Error processing slide:', error);
            return [];
        }
    }

    /**
     * Find all group shape elements
     * @param {Document} xmlDoc - Parsed XML document
     * @returns {Array<Element>} Group shape elements
     */
    findGroupShapes(xmlDoc) {
        const groups = [];
        
        // Try different selectors
        const selectors = ['p\\:grpSp', 'grpSp'];
        
        for (const selector of selectors) {
            try {
                const elements = xmlDoc.querySelectorAll(selector);
                if (elements.length > 0) {
                    groups.push(...Array.from(elements));
                    break;
                }
            } catch (e) {
                // Try next selector
            }
        }
        
        // Fallback: getElementsByTagName
        if (groups.length === 0) {
            const tagGroups = xmlDoc.getElementsByTagName('p:grpSp');
            if (tagGroups.length > 0) {
                groups.push(...Array.from(tagGroups));
            }
        }
        
        return groups;
    }

    /**
     * Process a single group
     * @param {Element} groupElement - Group XML element
     * @returns {Object|null} Group data
     */
    processGroup(groupElement) {
        try {
            // Find shapes within group
            const shapes = this.findShapesInGroup(groupElement);
            
            // Sort shapes by position
            const sortedShapes = this.sortShapesByPosition(shapes);
            
            // Extract text from shapes
            const texts = sortedShapes.map(shape => this.extractTextFromShape(shape));
            
            this.totalShapesProcessed += shapes.length;
            
            return {
                shapeCount: shapes.length,
                texts: texts.filter(t => t.length > 0),
                combinedText: texts.filter(t => t.length > 0).join(' ')
            };
        } catch (error) {
            console.warn('[PPTXGroupHandler] Error processing group:', error);
            return null;
        }
    }

    /**
     * Find shapes within a group
     * @param {Element} groupElement - Group element
     * @returns {Array<Element>} Shape elements
     */
    findShapesInGroup(groupElement) {
        const shapes = [];
        
        // Try to find shapes (p:sp)
        try {
            const shapeElements = groupElement.querySelectorAll('p\\:sp');
            if (shapeElements.length > 0) {
                shapes.push(...Array.from(shapeElements));
            }
        } catch (e) {
            // Fallback
            const tagShapes = groupElement.getElementsByTagName('p:sp');
            if (tagShapes.length > 0) {
                shapes.push(...Array.from(tagShapes));
            }
        }
        
        return shapes;
    }

    /**
     * Sort shapes by spatial position (top-to-bottom, left-to-right)
     * @param {Array<Element>} shapes - Shape elements
     * @returns {Array<Element>} Sorted shape elements
     */
    sortShapesByPosition(shapes) {
        return shapes.sort((a, b) => {
            const posA = this.getShapePosition(a);
            const posB = this.getShapePosition(b);
            
            // Sort by top position first
            if (posA.top !== posB.top) {
                return posA.top - posB.top;
            }
            
            // Then by left position
            return posA.left - posB.left;
        });
    }

    /**
     * Get shape position
     * @param {Element} shape - Shape element
     * @returns {Object} {top, left}
     */
    getShapePosition(shape) {
        return XMLHelper.getShapePosition(shape);
    }

    /**
     * Extract text from shape
     * @param {Element} shape - Shape element
     * @returns {string} Text content
     */
    extractTextFromShape(shape) {
        const texts = XMLHelper.getAllTextNodes(shape);
        return texts.join(' ').trim();
    }

    /**
     * Get statistics
     * @returns {Object} Statistics object
     */
    getGroupStats() {
        const totalTexts = this.groups.reduce((sum, g) => sum + g.texts.length, 0);
        
        return {
            totalGroups: this.groups.length,
            totalShapes: this.totalShapesProcessed,
            totalTexts: totalTexts,
            averageShapesPerGroup: this.groups.length > 0 
                ? (this.totalShapesProcessed / this.groups.length).toFixed(1) 
                : 0
        };
    }

    /**
     * Clear processed groups
     */
    clear() {
        this.groups = [];
        this.totalShapesProcessed = 0;
    }
}

// Export for use in HTML
if (typeof window !== 'undefined') {
    window.PPTXGroupHandler = PPTXGroupHandler;
}

// Export for Node.js (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PPTXGroupHandler;
}
