/**
 * PPTX Chart Extraction Module
 * 
 * Extracts chart data from PowerPoint files and converts to markdown tables.
 * Supports various chart types including bar, line, pie, area, and scatter.
 * 
 * Features:
 * - Parse chart XML from ppt/charts/ folder
 * - Extract series data (multiple series supported)
 * - Extract category labels
 * - Chart type detection
 * - Convert to markdown tables
 * - Statistics and metadata tracking
 * - Handle missing/malformed data
 * 
 * @class PPTXChartExtractor
 * @version 2.4.3
 * @date February 2026
 */

class PPTXChartExtractor {
    /**
     * Initialize chart extractor
     * @param {JSZip} zip - Loaded PPTX zip file
     */
    constructor(zip) {
        this.zip = zip;
        this.charts = [];
        this.chartFiles = this.findChartFiles();
    }

    /**
     * Find all chart files in PPTX
     * @returns {Array<string>} Array of chart file paths
     */
    findChartFiles() {
        return Object.keys(this.zip.files)
            .filter(name => name.match(/ppt\/charts\/chart\d+\.xml$/))
            .sort((a, b) => {
                const numA = parseInt(a.match(/chart(\d+)/)[1]);
                const numB = parseInt(b.match(/chart(\d+)/)[1]);
                return numA - numB;
            });
    }

    /**
     * Extract all charts from PPTX
     * @returns {Promise<Array>} Array of chart objects
     */
    async extractAll() {
        console.log(`[PPTXChartExtractor] Found ${this.chartFiles.length} charts in PPTX`);
        
        for (const chartPath of this.chartFiles) {
            const chartData = await this.extractChart(chartPath);
            if (chartData) {
                this.charts.push(chartData);
            }
        }
        
        console.log(`[PPTXChartExtractor] Successfully extracted ${this.charts.length} charts`);
        return this.charts;
    }

    /**
     * Extract single chart from XML file
     * @param {string} chartPath - Path to chart XML
     * @returns {Promise<Object|null>} Chart data object
     */
    async extractChart(chartPath) {
        try {
            const chartXml = await this.zip.files[chartPath].async('text');
            const xmlDoc = XMLHelper.parseXML(chartXml);
            
            // Extract chart title
            const title = this.extractTitle(xmlDoc);
            
            // Detect chart type
            const chartType = this.detectChartType(xmlDoc);
            
            // Extract series data
            const series = this.extractSeries(xmlDoc);
            
            // Extract categories
            const categories = this.extractCategories(xmlDoc, series);
            
            if (series.length === 0) {
                console.warn(`[PPTXChartExtractor] No data found in chart: ${chartPath}`);
                return null;
            }
            
            return {
                id: this.extractChartId(chartPath),
                title: title,
                type: chartType,
                series: series,
                categories: categories,
                path: chartPath,
                seriesCount: series.length,
                dataPointsCount: Math.max(...series.map(s => s.values.length))
            };
        } catch (error) {
            console.error(`[PPTXChartExtractor] Failed to extract chart ${chartPath}:`, error);
            return null;
        }
    }

    /**
     * Extract chart ID from path
     * @param {string} chartPath - Chart file path
     * @returns {string} Chart ID
     */
    extractChartId(chartPath) {
        const match = chartPath.match(/chart(\d+)/i);
        return match ? `chart${match[1]}` : 'chart';
    }

    /**
     * Extract chart title
     * @param {Document} xmlDoc - Parsed XML document
     * @returns {string} Chart title
     */
    extractTitle(xmlDoc) {
        // Try multiple selectors for title
        const titleSelectors = [
            'c\\:title c\\:tx c\\:strRef c\\:strCache c\\:pt c\\:v',
            'title tx strRef strCache pt v',
            'c\\:title c\\:tx c\\:rich c\\:p c\\:r c\\:t',
            'title tx rich p r t'
        ];
        
        for (const selector of titleSelectors) {
            try {
                const titleEl = xmlDoc.querySelector(selector);
                if (titleEl && titleEl.textContent) {
                    return titleEl.textContent.trim();
                }
            } catch (e) {
                // Try next selector
            }
        }
        
        // Fallback: try getElementsByTagName
        const vElements = xmlDoc.getElementsByTagName('c:v');
        if (vElements.length > 0) {
            return vElements[0].textContent?.trim() || 'Chart';
        }
        
        return 'Chart';
    }

    /**
     * Detect chart type from XML
     * @param {Document} xmlDoc - Parsed XML document
     * @returns {string} Chart type
     */
    detectChartType(xmlDoc) {
        const typeChecks = [
            { selector: 'c\\:barChart', type: 'bar' },
            { selector: 'c\\:lineChart', type: 'line' },
            { selector: 'c\\:pieChart', type: 'pie' },
            { selector: 'c\\:areaChart', type: 'area' },
            { selector: 'c\\:scatterChart', type: 'scatter' },
            { selector: 'c\\:radarChart', type: 'radar' },
            { selector: 'c\\:doughnutChart', type: 'doughnut' },
            { selector: 'c\\:bubbleChart', type: 'bubble' }
        ];
        
        for (const { selector, type } of typeChecks) {
            try {
                if (xmlDoc.querySelector(selector)) {
                    return type;
                }
            } catch (e) {
                // Try without namespace escape
                const plainSelector = selector.replace(/\\\\/g, '');
                if (xmlDoc.querySelector(plainSelector)) {
                    return type;
                }
            }
        }
        
        // Fallback: check with getElementsByTagName
        const chartTypes = ['barChart', 'lineChart', 'pieChart', 'areaChart', 'scatterChart'];
        for (const chartType of chartTypes) {
            if (xmlDoc.getElementsByTagName(`c:${chartType}`).length > 0) {
                return chartType.replace('Chart', '');
            }
        }
        
        return 'unknown';
    }

    /**
     * Extract series data from chart
     * @param {Document} xmlDoc - Parsed XML document
     * @returns {Array} Array of series objects
     */
    extractSeries(xmlDoc) {
        const series = [];
        
        // Find all series elements
        let seriesElements = [];
        
        try {
            seriesElements = Array.from(xmlDoc.querySelectorAll('c\\:ser'));
        } catch (e) {
            seriesElements = Array.from(xmlDoc.getElementsByTagName('c:ser'));
        }
        
        for (const ser of seriesElements) {
            // Get series name
            const name = this.extractSeriesName(ser, series.length);
            
            // Get values
            const values = this.extractSeriesValues(ser);
            
            if (values.length > 0) {
                series.push({ name, values });
            }
        }
        
        return series;
    }

    /**
     * Extract series name
     * @param {Element} seriesElement - Series XML element
     * @param {number} index - Series index (for fallback name)
     * @returns {string} Series name
     */
    extractSeriesName(seriesElement, index) {
        // Try to find series name
        const nameSelectors = [
            'c\\:tx c\\:v',
            'tx v',
            'c\\:tx c\\:strRef c\\:strCache c\\:pt c\\:v'
        ];
        
        for (const selector of nameSelectors) {
            try {
                const nameEl = seriesElement.querySelector(selector);
                if (nameEl && nameEl.textContent) {
                    return nameEl.textContent.trim();
                }
            } catch (e) {
                // Try next
            }
        }
        
        return `Series ${index + 1}`;
    }

    /**
     * Extract series values
     * @param {Element} seriesElement - Series XML element
     * @returns {Array<number>} Array of numeric values
     */
    extractSeriesValues(seriesElement) {
        const values = [];
        
        // Find value elements
        let valueElements = [];
        
        try {
            valueElements = Array.from(seriesElement.querySelectorAll('c\\:val c\\:numRef c\\:numCache c\\:pt c\\:v'));
        } catch (e) {
            // Fallback
            const numCache = seriesElement.querySelector('c\\:val c\\:numRef c\\:numCache') ||
                           seriesElement.getElementsByTagName('c:numCache')[0];
            if (numCache) {
                valueElements = Array.from(numCache.getElementsByTagName('c:v'));
            }
        }
        
        for (const el of valueElements) {
            const val = parseFloat(el.textContent);
            values.push(isNaN(val) ? 0 : val);
        }
        
        return values;
    }

    /**
     * Extract category labels
     * @param {Document} xmlDoc - Parsed XML document
     * @param {Array} series - Extracted series (for fallback)
     * @returns {Array<string>} Category labels
     */
    extractCategories(xmlDoc, series) {
        // Try to find category labels
        let catElements = [];
        
        try {
            catElements = Array.from(xmlDoc.querySelectorAll('c\\:cat c\\:strRef c\\:strCache c\\:pt c\\:v'));
        } catch (e) {
            // Fallback
            const strCache = xmlDoc.querySelector('c\\:cat c\\:strRef c\\:strCache') ||
                           xmlDoc.getElementsByTagName('c:strCache')[0];
            if (strCache) {
                catElements = Array.from(strCache.getElementsByTagName('c:v'));
            }
        }
        
        if (catElements.length > 0) {
            return catElements.map(el => el.textContent?.trim() || '');
        }
        
        // Fallback: generate numeric categories based on data length
        if (series.length > 0) {
            const maxLength = Math.max(...series.map(s => s.values.length));
            return Array.from({ length: maxLength }, (_, i) => `Category ${i + 1}`);
        }
        
        return [];
    }

    /**
     * Format chart as markdown table
     * @param {Object} chart - Chart data object
     * @param {Object} options - Formatting options
     * @returns {string} Markdown formatted table
     */
    formatChartMarkdown(chart, options = {}) {
        const {
            includeTitle = true,
            includeType = true,
            numberFormat = null,
            maxWidth = null
        } = options;
        
        let md = '\n\n';
        
        // Add chart title
        if (includeTitle) {
            md += `### Chart: ${chart.title}`;
            if (includeType && chart.type !== 'unknown') {
                md += ` (${chart.type})`;
            }
            md += '\n\n';
        }
        
        // Create table header
        const headers = ['Category', ...chart.series.map(s => s.name)];
        md += '| ' + headers.join(' | ') + ' |\n';
        md += '| ' + headers.map(() => '---').join(' | ') + ' |\n';
        
        // Create data rows
        const rowCount = Math.max(...chart.series.map(s => s.values.length));
        for (let i = 0; i < rowCount; i++) {
            const category = chart.categories[i] || `Row ${i + 1}`;
            const values = chart.series.map(s => {
                const val = s.values[i];
                if (val === undefined || val === null) return '';
                if (numberFormat) {
                    return this.formatNumber(val, numberFormat);
                }
                return val;
            });
            
            md += '| ' + [category, ...values].join(' | ') + ' |\n';
        }
        
        return md;
    }

    /**
     * Format number with specified format
     * @param {number} num - Number to format
     * @param {string} format - Format type ('decimal', 'percentage', 'currency')
     * @returns {string} Formatted number
     */
    formatNumber(num, format) {
        switch (format) {
            case 'decimal':
                return num.toFixed(2);
            case 'percentage':
                return `${(num * 100).toFixed(1)}%`;
            case 'currency':
                return `$${num.toFixed(2)}`;
            default:
                return String(num);
        }
    }

    /**
     * Get chart by ID
     * @param {string} chartId - Chart ID
     * @returns {Object|null} Chart object
     */
    getChartById(chartId) {
        return this.charts.find(c => c.id === chartId) || null;
    }

    /**
     * Get statistics about extracted charts
     * @returns {Object} Statistics object
     */
    getChartStats() {
        const byType = {};
        this.charts.forEach(chart => {
            byType[chart.type] = (byType[chart.type] || 0) + 1;
        });
        
        const totalSeries = this.charts.reduce((sum, c) => sum + c.seriesCount, 0);
        const totalDataPoints = this.charts.reduce((sum, c) => {
            return sum + c.series.reduce((s, series) => s + series.values.length, 0);
        }, 0);
        
        return {
            totalCharts: this.charts.length,
            byType: byType,
            totalSeries: totalSeries,
            totalDataPoints: totalDataPoints,
            averageSeriesPerChart: this.charts.length > 0 
                ? (totalSeries / this.charts.length).toFixed(1) 
                : 0
        };
    }

    /**
     * Export chart data as JSON
     * @param {string} chartId - Chart ID
     * @returns {string} JSON string
     */
    exportChartJSON(chartId) {
        const chart = this.getChartById(chartId);
        if (!chart) return null;
        
        return JSON.stringify(chart, null, 2);
    }

    /**
     * Export all charts as JSON
     * @returns {string} JSON string
     */
    exportAllChartsJSON() {
        return JSON.stringify(this.charts, null, 2);
    }
}

// Export for use in HTML
if (typeof window !== 'undefined') {
    window.PPTXChartExtractor = PPTXChartExtractor;
}

// Export for Node.js (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PPTXChartExtractor;
}
