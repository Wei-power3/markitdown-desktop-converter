/**
 * DOCX Converter - Client-Side Word to Markdown
 * 
 * Uses Mammoth.js to extract content from DOCX files.
 * Works entirely in the browser without server-side processing.
 * 
 * @class DOCXConverter
 * @version 2.4.3
 * @date February 2026
 */

class DOCXConverter {
    constructor() {
        this.stats = {
            totalParagraphs: 0,
            totalText: 0,
            hasImages: false,
            hasTables: false,
            processingTime: 0
        };
    }

    /**
     * Convert DOCX file to Markdown
     * @param {File} file - The DOCX file to convert
     * @returns {Promise<Object>} { markdown: string, stats: object }
     */
    async convert(file) {
        const startTime = Date.now();
        
        try {
            // Check if Mammoth.js is loaded
            if (typeof mammoth === 'undefined') {
                throw new Error('Mammoth.js library not loaded. Please include Mammoth.js from CDN.');
            }

            const arrayBuffer = await file.arrayBuffer();
            
            // Convert DOCX to Markdown using Mammoth
            const result = await mammoth.convertToMarkdown(
                { arrayBuffer: arrayBuffer },
                {
                    styleMap: [
                        "p[style-name='Heading 1'] => # :fresh",
                        "p[style-name='Heading 2'] => ## :fresh",
                        "p[style-name='Heading 3'] => ### :fresh",
                        "p[style-name='Heading 4'] => #### :fresh",
                        "p[style-name='Heading 5'] => ##### :fresh",
                        "p[style-name='Heading 6'] => ###### :fresh"
                    ]
                }
            );
            
            let markdown = `# ${file.name}\n\n`;
            markdown += `*Converted with MarkItDown v2.4.3*\n\n`;
            markdown += `---\n\n`;
            markdown += result.value + '\n';
            
            // Calculate stats
            this.stats.totalText = result.value.length;
            this.stats.totalParagraphs = result.value.split('\n\n').length;
            this.stats.hasImages = result.value.includes('![');
            this.stats.hasTables = result.value.includes('|');
            this.stats.processingTime = Date.now() - startTime;
            
            // Log any warnings
            if (result.messages && result.messages.length > 0) {
                console.warn('DOCX conversion warnings:', result.messages);
            }
            
            return {
                markdown: markdown.trim(),
                stats: this.stats,
                warnings: result.messages || []
            };
        } catch (error) {
            console.error('DOCX conversion error:', error);
            throw new Error(`Failed to convert DOCX: ${error.message}`);
        }
    }

    /**
     * Get statistics object
     * @returns {Object} Statistics
     */
    getStats() {
        return { ...this.stats };
    }
}

// Export for use in HTML
if (typeof window !== 'undefined') {
    window.DOCXConverter = DOCXConverter;
}

// Export for Node.js (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DOCXConverter;
}
