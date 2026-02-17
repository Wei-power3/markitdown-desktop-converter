/**
 * XML Helper Utilities for PPTX Processing
 * 
 * Provides utilities for parsing and extracting data from PPTX XML files.
 * Handles namespace-aware queries and common XML operations.
 * 
 * @class XMLHelper
 * @version 2.4.3
 * @date February 2026
 */

class XMLHelper {
    /**
     * Parse XML string to Document
     * @param {string} xmlString - XML string to parse
     * @returns {Document} Parsed XML document
     */
    static parseXML(xmlString) {
        const parser = new DOMParser();
        const xmlDoc = parser.parseFromString(xmlString, 'text/xml');
        
        // Check for parse errors
        const parserError = xmlDoc.querySelector('parsererror');
        if (parserError) {
            console.warn('XML parse error:', parserError.textContent);
        }
        
        return xmlDoc;
    }

    /**
     * Get text content from elements with specific tag name
     * @param {Element} element - Parent element
     * @param {string} tagName - Tag name to search for
     * @returns {string} Combined text content
     */
    static getElementText(element, tagName) {
        if (!element) return '';
        
        const elements = element.getElementsByTagName(tagName);
        const texts = [];
        
        for (const el of elements) {
            const text = el.textContent?.trim();
            if (text) texts.push(text);
        }
        
        return texts.join(' ');
    }

    /**
     * Get attribute value from element using selector
     * @param {Element} element - Parent element
     * @param {string} selector - CSS/namespace selector
     * @param {string} attrName - Attribute name
     * @returns {string} Attribute value or empty string
     */
    static getAttributeValue(element, selector, attrName) {
        try {
            // Try standard selector first
            let el = element.querySelector(selector);
            
            // If not found, try namespace-escaped version
            if (!el && selector.includes(':')) {
                const escapedSelector = selector.replace(/:/g, '\\:');
                el = element.querySelector(escapedSelector);
            }
            
            return el?.getAttribute(attrName) || '';
        } catch (e) {
            console.warn('Attribute query failed:', selector, e);
            return '';
        }
    }

    /**
     * Get all text nodes from element tree
     * @param {Element} element - Root element
     * @returns {Array<string>} Array of text content
     */
    static getAllTextNodes(element) {
        if (!element) return [];
        
        const textNodes = element.getElementsByTagName('a:t');
        return Array.from(textNodes)
            .map(node => node.textContent?.trim())
            .filter(text => text && text.length > 0);
    }

    /**
     * Find elements using namespace-aware selector
     * Handles both prefixed and non-prefixed namespaces
     * @param {Element} element - Parent element
     * @param {string} tagName - Tag name (with or without namespace prefix)
     * @returns {Array<Element>} Array of matching elements
     */
    static findElements(element, tagName) {
        if (!element) return [];
        
        // Try direct tag name
        let elements = element.getElementsByTagName(tagName);
        
        // If not found and tag has namespace prefix, try escaped version
        if (elements.length === 0 && tagName.includes(':')) {
            const escapedTag = tagName.replace(':', '\\:');
            try {
                const nodeList = element.querySelectorAll(escapedTag);
                elements = Array.from(nodeList);
            } catch (e) {
                // Fallback: try without namespace
                const localName = tagName.split(':').pop();
                elements = element.getElementsByTagName(localName);
            }
        }
        
        return Array.from(elements);
    }

    /**
     * Extract position information from shape
     * @param {Element} shape - Shape element
     * @returns {Object} {top, left, width, height}
     */
    static getShapePosition(shape) {
        try {
            // Try to find transform element
            const xfrm = shape.querySelector('p\\:spPr a\\:xfrm a\\:off, spPr xfrm off');
            
            if (xfrm) {
                return {
                    top: parseInt(xfrm.getAttribute('y') || '0'),
                    left: parseInt(xfrm.getAttribute('x') || '0')
                };
            }
            
            // Fallback to default
            return { top: 0, left: 0 };
        } catch (error) {
            console.warn('Failed to get shape position:', error);
            return { top: 0, left: 0 };
        }
    }

    /**
     * Clean text content for markdown
     * @param {string} text - Raw text content
     * @returns {string} Cleaned text
     */
    static cleanText(text) {
        if (!text) return '';
        
        return text
            .replace(/[\r\n]+/g, ' ')  // Replace line breaks with spaces
            .replace(/\s+/g, ' ')       // Normalize whitespace
            .trim();
    }

    /**
     * Extract all attributes from element as object
     * @param {Element} element - Element to extract from
     * @returns {Object} Attribute key-value pairs
     */
    static getAttributes(element) {
        if (!element || !element.attributes) return {};
        
        const attrs = {};
        for (const attr of element.attributes) {
            attrs[attr.name] = attr.value;
        }
        return attrs;
    }

    /**
     * Check if element exists in document
     * @param {Element} parent - Parent element
     * @param {string} selector - Element selector
     * @returns {boolean} True if element exists
     */
    static elementExists(parent, selector) {
        try {
            return parent.querySelector(selector) !== null;
        } catch (e) {
            // Try namespace-escaped version
            try {
                const escapedSelector = selector.replace(/:/g, '\\:');
                return parent.querySelector(escapedSelector) !== null;
            } catch (e2) {
                return false;
            }
        }
    }
}

// Export for use in HTML
if (typeof window !== 'undefined') {
    window.XMLHelper = XMLHelper;
}

// Export for Node.js (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = XMLHelper;
}
