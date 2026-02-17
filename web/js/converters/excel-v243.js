/**
 * Excel v2.4.3 Converter - Enhanced Multi-Sheet Support
 * 
 * Features:
 * - Multi-sheet processing with sheet name headers
 * - Formula preservation (displayed as markdown code)
 * - Merged cell detection and reporting
 * - Enhanced statistics (sheets, formulas, merged cells)
 * - Better empty cell handling
 * 
 * @class ExcelConverterV243
 * @version 2.4.3
 * @date February 2026
 */

class ExcelConverterV243 {
    constructor() {
        this.stats = {
            totalSheets: 0,
            totalTables: 0,
            totalCells: 0,
            formulas: 0,
            mergedCells: 0,
            emptyCells: 0,
            processedCells: 0
        };
    }

    /**
     * Convert Excel file to Markdown
     * @param {File} file - The Excel file to convert
     * @returns {Object} { markdown: string, stats: object }
     */
    async convert(file) {
        try {
            const arrayBuffer = await file.arrayBuffer();
            const workbook = XLSX.read(arrayBuffer, { 
                cellFormula: true,  // Preserve formulas
                cellStyles: true,   // Get formatting info
                sheetStubs: false   // Don't process completely empty cells
            });
            
            let markdown = `# ${file.name}\n\n`;
            markdown += `*Converted with MarkItDown v2.4.3 - Enhanced Excel Support*\n\n`;
            markdown += `Document created: ${new Date().toLocaleDateString()}\n\n`;
            markdown += `---\n\n`;
            
            this.stats.totalSheets = workbook.SheetNames.length;
            
            // Process each sheet
            for (const sheetName of workbook.SheetNames) {
                const worksheet = workbook.Sheets[sheetName];
                markdown += this.convertSheet(worksheet, sheetName);
            }
            
            // Add document summary
            markdown += this.generateSummary();
            
            return {
                markdown: markdown.trim(),
                stats: this.stats
            };
        } catch (error) {
            console.error('Excel conversion error:', error);
            throw new Error(`Failed to convert Excel file: ${error.message}`);
        }
    }

    /**
     * Convert a single worksheet to Markdown
     * @param {Object} worksheet - SheetJS worksheet object
     * @param {string} sheetName - Name of the sheet
     * @returns {string} Markdown representation
     */
    convertSheet(worksheet, sheetName) {
        let md = `## ${sheetName}\n\n`;
        
        // Check if sheet has data
        if (!worksheet['!ref']) {
            md += `*This sheet is empty*\n\n`;
            return md;
        }
        
        // Track merged cells
        const merges = worksheet['!merges'] || [];
        this.stats.mergedCells += merges.length;
        this.stats.totalTables++;
        
        // Get range
        const range = XLSX.utils.decode_range(worksheet['!ref']);
        const rows = [];
        
        // Extract all rows
        for (let R = range.s.r; R <= range.e.r; ++R) {
            const row = [];
            let hasData = false;
            
            for (let C = range.s.c; C <= range.e.c; ++C) {
                const cellAddress = XLSX.utils.encode_cell({ r: R, c: C });
                const cell = worksheet[cellAddress];
                
                let cellValue = '';
                
                if (cell) {
                    this.stats.totalCells++;
                    this.stats.processedCells++;
                    hasData = true;
                    
                    // Check if cell has formula
                    if (cell.f) {
                        this.stats.formulas++;
                        cellValue = `\`=${cell.f}\``;  // Display formula in code format
                    } else {
                        cellValue = this.formatCellValue(cell);
                    }
                } else {
                    this.stats.emptyCells++;
                }
                
                row.push(cellValue);
            }
            
            // Only add rows with data
            if (hasData) {
                rows.push(row);
            }
        }
        
        // Create markdown table
        if (rows.length > 0) {
            // Header row
            md += '| ' + rows[0].join(' | ') + ' |\n';
            
            // Separator row
            md += '| ' + rows[0].map(() => '---').join(' | ') + ' |\n';
            
            // Data rows
            for (let i = 1; i < rows.length; i++) {
                md += '| ' + rows[i].join(' | ') + ' |\n';
            }
            
            md += '\n';
            
            // Add sheet metadata
            const metadata = [];
            if (merges.length > 0) {
                metadata.push(`${merges.length} merged cell(s)`);
            }
            if (this.stats.formulas > 0) {
                const sheetFormulas = this.countSheetFormulas(worksheet);
                if (sheetFormulas > 0) {
                    metadata.push(`${sheetFormulas} formula(s)`);
                }
            }
            
            if (metadata.length > 0) {
                md += `*Sheet contains: ${metadata.join(', ')}*\n\n`;
            }
        } else {
            md += '*No data found in this sheet*\n\n';
        }
        
        return md;
    }

    /**
     * Format cell value based on cell type
     * @param {Object} cell - SheetJS cell object
     * @returns {string} Formatted cell value
     */
    formatCellValue(cell) {
        // Handle null/undefined
        if (!cell.v && cell.v !== 0) return '';
        
        // Number formatting
        if (cell.t === 'n') {
            // Check if it's a date (has a date format)
            if (cell.w && cell.w.match(/\d{1,2}\/\d{1,2}\/\d{2,4}/)) {
                return cell.w;  // Use formatted date
            }
            // Check for percentage
            if (cell.w && cell.w.includes('%')) {
                return cell.w;
            }
            // Check for currency
            if (cell.w && (cell.w.includes('$') || cell.w.includes('€') || cell.w.includes('£'))) {
                return cell.w;
            }
            // Regular number
            return String(cell.v);
        }
        
        // Boolean
        if (cell.t === 'b') {
            return cell.v ? 'TRUE' : 'FALSE';
        }
        
        // Error
        if (cell.t === 'e') {
            return `#ERROR`;
        }
        
        // String - escape markdown special characters
        const str = String(cell.v || '');
        return str
            .replace(/\|/g, '\\|')   // Escape pipes for markdown tables
            .replace(/\n/g, ' ')      // Replace newlines with spaces
            .replace(/\r/g, '')       // Remove carriage returns
            .trim();
    }

    /**
     * Count formulas in a specific sheet
     * @param {Object} worksheet - SheetJS worksheet object
     * @returns {number} Number of formulas
     */
    countSheetFormulas(worksheet) {
        let count = 0;
        for (const cellAddress in worksheet) {
            if (cellAddress[0] === '!') continue; // Skip metadata
            const cell = worksheet[cellAddress];
            if (cell && cell.f) count++;
        }
        return count;
    }

    /**
     * Generate document summary
     * @returns {string} Summary markdown
     */
    generateSummary() {
        let summary = `---\n\n## Document Summary\n\n`;
        summary += `| Metric | Value |\n`;
        summary += `|--------|-------|\n`;
        summary += `| Total Sheets | ${this.stats.totalSheets} |\n`;
        summary += `| Total Tables | ${this.stats.totalTables} |\n`;
        summary += `| Total Cells | ${this.stats.totalCells} |\n`;
        summary += `| Formulas | ${this.stats.formulas} |\n`;
        summary += `| Merged Cells | ${this.stats.mergedCells} |\n`;
        summary += `| Empty Cells | ${this.stats.emptyCells} |\n`;
        
        return summary;
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
    window.ExcelConverterV243 = ExcelConverterV243;
}

// Export for Node.js (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ExcelConverterV243;
}
