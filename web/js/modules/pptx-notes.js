/**
 * PPTX Speaker Notes Extraction Module
 * 
 * Extracts speaker notes from PowerPoint presentations.
 * Notes are stored in separate XML files (ppt/notesSlides/notesSlide*.xml)
 * 
 * Features:
 * - Extract speaker notes from notesSlide XML files
 * - Text parsing and cleaning
 * - Per-slide caching for performance
 * - Batch extraction for all slides
 * - Statistics tracking
 * - Markdown formatting
 * 
 * @class PPTXNotesExtractor
 * @version 2.4.3
 * @date February 2026
 */

class PPTXNotesExtractor {
    /**
     * Initialize notes extractor
     * @param {JSZip} zip - Loaded PPTX zip file
     */
    constructor(zip) {
        this.zip = zip;
        this.notesCache = new Map();  // Cache extracted notes
        this.notesFiles = this.findNotesFiles();
    }

    /**
     * Find all notes slide files in PPTX
     * @returns {Array<string>} Array of notes file paths
     */
    findNotesFiles() {
        return Object.keys(this.zip.files)
            .filter(name => name.match(/ppt\/notesSlides\/notesSlide\d+\.xml$/))
            .sort((a, b) => {
                const numA = parseInt(a.match(/notesSlide(\d+)/)[1]);
                const numB = parseInt(b.match(/notesSlide(\d+)/)[1]);
                return numA - numB;
            });
    }

    /**
     * Extract speaker notes for a specific slide
     * @param {number} slideNumber - Slide number (1-based)
     * @returns {Promise<string|null>} Notes text or null if no notes
     */
    async extractForSlide(slideNumber) {
        // Check cache first
        if (this.notesCache.has(slideNumber)) {
            return this.notesCache.get(slideNumber);
        }
        
        const notesPath = `ppt/notesSlides/notesSlide${slideNumber}.xml`;
        
        // Check if notes file exists
        if (!this.zip.files[notesPath]) {
            this.notesCache.set(slideNumber, null);
            return null;
        }
        
        try {
            const notesXml = await this.zip.files[notesPath].async('text');
            const notes = this.parseNotesXml(notesXml, slideNumber);
            
            // Cache the result
            this.notesCache.set(slideNumber, notes);
            
            return notes;
        } catch (error) {
            console.error(`[PPTXNotesExtractor] Failed to extract notes for slide ${slideNumber}:`, error);
            this.notesCache.set(slideNumber, null);
            return null;
        }
    }

    /**
     * Parse notes from XML content
     * @param {string} xmlContent - Notes XML content
     * @param {number} slideNumber - Slide number for logging
     * @returns {string|null} Parsed notes text
     */
    parseNotesXml(xmlContent, slideNumber) {
        try {
            const xmlDoc = XMLHelper.parseXML(xmlContent);
            
            // Extract all text nodes
            const textElements = XMLHelper.getAllTextNodes(xmlDoc);
            
            if (textElements.length === 0) {
                return null;
            }
            
            // Filter out slide content (usually the first few elements)
            // Speaker notes typically start after the slide preview text
            const notes = this.filterSlideContent(textElements);
            
            if (notes.length === 0) {
                return null;
            }
            
            // Join and clean the notes
            const notesText = notes.join(' ').trim();
            
            return notesText.length > 0 ? notesText : null;
        } catch (error) {
            console.warn(`[PPTXNotesExtractor] Error parsing notes XML for slide ${slideNumber}:`, error);
            return null;
        }
    }

    /**
     * Filter out slide content from text elements
     * @param {Array<string>} textElements - Array of text strings
     * @returns {Array<string>} Filtered text elements
     */
    filterSlideContent(textElements) {
        // Heuristic: Usually the first 1-3 elements are slide titles/content
        // Speaker notes start after that
        
        // If we have very few elements, return all
        if (textElements.length <= 2) {
            return textElements;
        }
        
        // Skip first element (usually slide title)
        const filtered = textElements.slice(1);
        
        // Additional filtering: remove very short elements (likely formatting)
        return filtered.filter(text => text.length > 3);
    }

    /**
     * Extract notes for all slides
     * @param {number} totalSlides - Total number of slides
     * @returns {Promise<Array>} Array of {slideNumber, notes} objects
     */
    async extractAll(totalSlides) {
        const allNotes = [];
        
        for (let i = 1; i <= totalSlides; i++) {
            const notes = await this.extractForSlide(i);
            allNotes.push({
                slideNumber: i,
                notes: notes,
                hasNotes: notes !== null
            });
        }
        
        console.log(`[PPTXNotesExtractor] Extracted notes from ${allNotes.filter(n => n.hasNotes).length}/${totalSlides} slides`);
        
        return allNotes;
    }

    /**
     * Extract notes for multiple specific slides
     * @param {Array<number>} slideNumbers - Array of slide numbers
     * @returns {Promise<Array>} Array of {slideNumber, notes} objects
     */
    async extractForSlides(slideNumbers) {
        const results = [];
        
        for (const slideNum of slideNumbers) {
            const notes = await this.extractForSlide(slideNum);
            results.push({
                slideNumber: slideNum,
                notes: notes,
                hasNotes: notes !== null
            });
        }
        
        return results;
    }

    /**
     * Check if a slide has notes
     * @param {number} slideNumber - Slide number
     * @returns {Promise<boolean>} True if slide has notes
     */
    async hasNotes(slideNumber) {
        const notes = await this.extractForSlide(slideNumber);
        return notes !== null && notes.length > 0;
    }

    /**
     * Get count of slides with notes
     * @returns {number} Number of slides with notes
     */
    getSlidesWithNotesCount() {
        return Array.from(this.notesCache.values())
            .filter(notes => notes !== null && notes.length > 0)
            .length;
    }

    /**
     * Get statistics about notes
     * @returns {Object} Statistics object
     */
    getNotesStats() {
        const notesArray = Array.from(this.notesCache.values())
            .filter(notes => notes !== null);
        
        const totalCharacters = notesArray
            .reduce((sum, notes) => sum + (notes?.length || 0), 0);
        
        const totalWords = notesArray
            .reduce((sum, notes) => {
                if (!notes) return sum;
                return sum + notes.split(/\s+/).filter(w => w.length > 0).length;
            }, 0);
        
        const averageLength = notesArray.length > 0 
            ? Math.round(totalCharacters / notesArray.length) 
            : 0;
        
        return {
            totalSlides: this.notesCache.size,
            slidesWithNotes: notesArray.length,
            slidesWithoutNotes: this.notesCache.size - notesArray.length,
            totalCharacters: totalCharacters,
            totalWords: totalWords,
            averageLength: averageLength,
            shortestNotes: this.getShortestNotesLength(notesArray),
            longestNotes: this.getLongestNotesLength(notesArray)
        };
    }

    /**
     * Get length of shortest notes
     * @param {Array<string>} notesArray - Array of notes
     * @returns {number} Length of shortest notes
     */
    getShortestNotesLength(notesArray) {
        if (notesArray.length === 0) return 0;
        return Math.min(...notesArray.map(n => n?.length || 0));
    }

    /**
     * Get length of longest notes
     * @param {Array<string>} notesArray - Array of notes
     * @returns {number} Length of longest notes
     */
    getLongestNotesLength(notesArray) {
        if (notesArray.length === 0) return 0;
        return Math.max(...notesArray.map(n => n?.length || 0));
    }

    /**
     * Format notes as markdown for a slide
     * @param {string|null} notes - Notes text
     * @param {Object} options - Formatting options
     * @returns {string} Markdown formatted notes
     */
    formatNotesMarkdown(notes, options = {}) {
        if (!notes || notes.length === 0) {
            return '';
        }
        
        const {
            heading = '### Speaker Notes',
            includeHeading = true,
            wrapInQuote = false,
            maxLength = null
        } = options;
        
        let md = '';
        
        // Add heading
        if (includeHeading) {
            md += `\n\n${heading}\n\n`;
        }
        
        // Truncate if needed
        let notesText = notes;
        if (maxLength && notes.length > maxLength) {
            notesText = notes.substring(0, maxLength - 3) + '...';
        }
        
        // Wrap in quote block if requested
        if (wrapInQuote) {
            const lines = notesText.split('\n');
            md += lines.map(line => `> ${line}`).join('\n');
        } else {
            md += notesText;
        }
        
        md += '\n';
        
        return md;
    }

    /**
     * Format notes for multiple slides
     * @param {Array<Object>} notesData - Array of {slideNumber, notes} objects
     * @param {Object} options - Formatting options
     * @returns {string} Markdown formatted notes
     */
    formatMultipleNotes(notesData, options = {}) {
        let md = '';
        
        notesData.forEach(({ slideNumber, notes }) => {
            if (notes && notes.length > 0) {
                md += `\n\n#### Slide ${slideNumber} Notes\n\n`;
                md += this.formatNotesMarkdown(notes, { ...options, includeHeading: false });
            }
        });
        
        return md;
    }

    /**
     * Clear notes cache
     */
    clearCache() {
        this.notesCache.clear();
    }

    /**
     * Export all notes as plain text
     * @returns {string} All notes concatenated
     */
    exportAllNotes() {
        const notesArray = [];
        
        // Sort by slide number
        const sortedEntries = Array.from(this.notesCache.entries())
            .sort((a, b) => a[0] - b[0]);
        
        sortedEntries.forEach(([slideNumber, notes]) => {
            if (notes && notes.length > 0) {
                notesArray.push(`Slide ${slideNumber}:`);
                notesArray.push(notes);
                notesArray.push(''); // Empty line
            }
        });
        
        return notesArray.join('\n');
    }

    /**
     * Search notes for text
     * @param {string} searchText - Text to search for
     * @param {boolean} caseSensitive - Case sensitive search
     * @returns {Array} Array of {slideNumber, notes, matches} objects
     */
    searchNotes(searchText, caseSensitive = false) {
        const results = [];
        const searchPattern = caseSensitive 
            ? searchText 
            : searchText.toLowerCase();
        
        this.notesCache.forEach((notes, slideNumber) => {
            if (!notes) return;
            
            const notesText = caseSensitive ? notes : notes.toLowerCase();
            
            if (notesText.includes(searchPattern)) {
                results.push({
                    slideNumber: slideNumber,
                    notes: notes,
                    matches: this.countMatches(notesText, searchPattern)
                });
            }
        });
        
        return results;
    }

    /**
     * Count occurrences of pattern in text
     * @param {string} text - Text to search in
     * @param {string} pattern - Pattern to search for
     * @returns {number} Number of matches
     */
    countMatches(text, pattern) {
        return (text.match(new RegExp(pattern, 'g')) || []).length;
    }
}

// Export for use in HTML
if (typeof window !== 'undefined') {
    window.PPTXNotesExtractor = PPTXNotesExtractor;
}

// Export for Node.js (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PPTXNotesExtractor;
}
