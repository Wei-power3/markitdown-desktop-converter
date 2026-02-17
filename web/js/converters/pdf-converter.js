/**
 * PDF Converter - Client-Side PDF to Markdown
 * 
 * Uses PDF.js (Mozilla) to extract text from PDF files.
 * Works entirely in the browser without server-side processing.
 * 
 * @class PDFConverter
 * @version 2.4.3
 * @date February 2026
 */

class PDFConverter {
    constructor() {
        this.stats = {
            totalPages: 0,
            totalText: 0,
            processingTime: 0
        };
    }

    /**
     * Convert PDF file to Markdown
     * @param {File} file - The PDF file to convert
     * @returns {Promise<Object>} { markdown: string, stats: object }
     */
    async convert(file) {
        const startTime = Date.now();
        
        try {
            // Check if PDF.js is loaded
            if (typeof pdfjsLib === 'undefined') {
                throw new Error('PDF.js library not loaded. Please include PDF.js from CDN.');
            }

            const arrayBuffer = await file.arrayBuffer();
            const loadingTask = pdfjsLib.getDocument({ data: arrayBuffer });
            const pdf = await loadingTask.promise;
            
            this.stats.totalPages = pdf.numPages;
            
            let markdown = `# ${file.name}\n\n`;
            markdown += `*Converted with MarkItDown v2.4.3*\n\n`;
            markdown += `Document: **${pdf.numPages} pages**\n\n`;
            markdown += `---\n\n`;
            
            // Extract text from each page
            for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
                const page = await pdf.getPage(pageNum);
                const textContent = await page.getTextContent();
                
                markdown += `## Page ${pageNum}\n\n`;
                
                // Combine text items
                const pageText = textContent.items
                    .map(item => item.str)
                    .join(' ')
                    .trim();
                
                if (pageText) {
                    markdown += pageText + '\n\n';
                    this.stats.totalText += pageText.length;
                } else {
                    markdown += `*No text content found on this page*\n\n`;
                }
            }
            
            this.stats.processingTime = Date.now() - startTime;
            
            return {
                markdown: markdown.trim(),
                stats: this.stats
            };
        } catch (error) {
            console.error('PDF conversion error:', error);
            throw new Error(`Failed to convert PDF: ${error.message}`);
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
    window.PDFConverter = PDFConverter;
}

// Export for Node.js (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PDFConverter;
}
