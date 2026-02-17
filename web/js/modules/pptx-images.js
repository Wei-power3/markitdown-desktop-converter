/**
 * PPTX Image Extraction Module
 * 
 * Extracts images from PowerPoint files with alt text and metadata.
 * Supports base64 embedding and tracks comprehensive statistics.
 * 
 * Features:
 * - Extract images from ppt/media/ folder
 * - Parse alt text from slide XML (p:cNvPr descr attribute)
 * - Base64 encoding with data URI generation
 * - Image size and format tracking
 * - Slide-to-image mapping
 * - Markdown formatting with alt text
 * 
 * @class PPTXImageExtractor
 * @version 2.4.3
 * @date February 2026
 */

class PPTXImageExtractor {
    /**
     * Initialize image extractor
     * @param {JSZip} zip - Loaded PPTX zip file
     */
    constructor(zip) {
        this.zip = zip;
        this.images = [];
        this.imageMap = new Map();  // Map image IDs to image data
        this.slideImageMap = new Map();  // Map slide numbers to image arrays
    }

    /**
     * Extract all images from PPTX
     * @returns {Promise<Array>} Array of image objects
     */
    async extractAll() {
        try {
            // Find all media files (images)
            const mediaFiles = Object.keys(this.zip.files)
                .filter(name => this.isImageFile(name));
            
            console.log(`[PPTXImageExtractor] Found ${mediaFiles.length} images in PPTX`);
            
            // Extract each image
            for (const mediaPath of mediaFiles) {
                const imgData = await this.extractImage(mediaPath);
                if (imgData) {
                    this.images.push(imgData);
                    this.imageMap.set(imgData.id, imgData);
                }
            }
            
            // Enhance with alt text from slides
            await this.enhanceWithSlideData();
            
            console.log(`[PPTXImageExtractor] Successfully extracted ${this.images.length} images`);
            return this.images;
        } catch (error) {
            console.error('[PPTXImageExtractor] Error extracting images:', error);
            throw error;
        }
    }

    /**
     * Check if file is an image
     * @param {string} filename - File path
     * @returns {boolean} True if image file
     */
    isImageFile(filename) {
        const imagePattern = /ppt\/media\/(image\d+)\.(png|jpg|jpeg|gif|svg|webp|bmp|tiff?)/i;
        return imagePattern.test(filename);
    }

    /**
     * Extract single image from PPTX
     * @param {string} mediaPath - Path to image in PPTX
     * @returns {Promise<Object>} Image data object
     */
    async extractImage(mediaPath) {
        try {
            const filename = mediaPath.split('/').pop();
            const imageId = this.extractImageId(filename);
            
            // Get image binary data
            const imageBlob = await this.zip.files[mediaPath].async('arraybuffer');
            
            // Convert to base64
            const base64Data = Base64Helper.arrayBufferToBase64(imageBlob);
            const mimeType = Base64Helper.getImageMimeType(filename);
            const dataURI = Base64Helper.createDataURI(base64Data, mimeType);
            
            // Get image dimensions (if possible)
            const dimensions = await this.getImageDimensions(dataURI);
            
            return {
                id: imageId,
                filename: filename,
                path: mediaPath,
                base64: base64Data,
                mimeType: mimeType,
                dataURI: dataURI,
                size: imageBlob.byteLength,
                sizeFormatted: Base64Helper.formatSize(imageBlob.byteLength),
                width: dimensions.width,
                height: dimensions.height,
                altText: filename,  // Default, will be enhanced
                shapeName: '',
                slides: []  // Which slides contain this image
            };
        } catch (error) {
            console.error(`[PPTXImageExtractor] Failed to extract ${mediaPath}:`, error);
            return null;
        }
    }

    /**
     * Extract image ID from filename
     * @param {string} filename - Image filename (e.g., "image1.png")
     * @returns {string} Image ID (e.g., "image1")
     */
    extractImageId(filename) {
        const match = filename.match(/(image\d+)/i);
        return match ? match[1].toLowerCase() : filename;
    }

    /**
     * Get image dimensions
     * @param {string} dataURI - Image data URI
     * @returns {Promise<Object>} {width, height}
     */
    async getImageDimensions(dataURI) {
        return new Promise((resolve) => {
            const img = new Image();
            img.onload = () => {
                resolve({ width: img.width, height: img.height });
            };
            img.onerror = () => {
                resolve({ width: 0, height: 0 });
            };
            img.src = dataURI;
        });
    }

    /**
     * Enhance images with alt text and metadata from slides
     * @returns {Promise<void>}
     */
    async enhanceWithSlideData() {
        // Get all slide files
        const slideFiles = Object.keys(this.zip.files)
            .filter(name => name.match(/ppt\/slides\/slide\d+\.xml$/))
            .sort((a, b) => {
                const numA = parseInt(a.match(/slide(\d+)/)[1]);
                const numB = parseInt(b.match(/slide(\d+)/)[1]);
                return numA - numB;
            });
        
        // Process each slide
        for (let i = 0; i < slideFiles.length; i++) {
            const slideNumber = i + 1;
            await this.enhanceFromSlide(slideFiles[i], slideNumber);
        }
    }

    /**
     * Enhance images with data from a specific slide
     * @param {string} slidePath - Path to slide XML
     * @param {number} slideNumber - Slide number (1-based)
     * @returns {Promise<void>}
     */
    async enhanceFromSlide(slidePath, slideNumber) {
        try {
            const slideXml = await this.zip.files[slidePath].async('text');
            const xmlDoc = XMLHelper.parseXML(slideXml);
            
            // Find all picture elements
            const pics = this.findPictureElements(xmlDoc);
            
            const slideImages = [];
            
            for (const pic of pics) {
                const imageData = this.extractPictureData(pic);
                
                if (imageData) {
                    // Try to match with extracted image
                    const matchedImage = this.findMatchingImage(imageData);
                    
                    if (matchedImage) {
                        // Update alt text if available
                        if (imageData.altText) {
                            matchedImage.altText = imageData.altText;
                        }
                        if (imageData.shapeName) {
                            matchedImage.shapeName = imageData.shapeName;
                        }
                        
                        // Track which slides contain this image
                        if (!matchedImage.slides.includes(slideNumber)) {
                            matchedImage.slides.push(slideNumber);
                        }
                        
                        slideImages.push(matchedImage);
                    }
                }
            }
            
            // Store slide-to-image mapping
            if (slideImages.length > 0) {
                this.slideImageMap.set(slideNumber, slideImages);
            }
        } catch (error) {
            console.warn(`[PPTXImageExtractor] Failed to enhance slide ${slideNumber}:`, error);
        }
    }

    /**
     * Find all picture elements in slide XML
     * @param {Document} xmlDoc - Parsed XML document
     * @returns {Array<Element>} Array of picture elements
     */
    findPictureElements(xmlDoc) {
        const pics = [];
        
        // Try different namespace variations
        const selectors = [
            'p\\:pic',
            'pic',
            '[name="pic"]'
        ];
        
        for (const selector of selectors) {
            try {
                const elements = xmlDoc.querySelectorAll(selector);
                if (elements.length > 0) {
                    pics.push(...Array.from(elements));
                    break;
                }
            } catch (e) {
                // Try next selector
            }
        }
        
        // Fallback: use getElementsByTagName
        if (pics.length === 0) {
            const tagPics = xmlDoc.getElementsByTagName('p:pic');
            if (tagPics.length > 0) {
                pics.push(...Array.from(tagPics));
            }
        }
        
        return pics;
    }

    /**
     * Extract picture data from XML element
     * @param {Element} pic - Picture XML element
     * @returns {Object|null} Picture data
     */
    extractPictureData(pic) {
        try {
            // Try to find cNvPr (non-visual properties)
            let cNvPr = pic.querySelector('p\\:nvPicPr p\\:cNvPr');
            if (!cNvPr) {
                cNvPr = pic.querySelector('nvPicPr cNvPr');
            }
            if (!cNvPr) {
                // Try without namespace
                const nvPicPr = pic.querySelector('[name="nvPicPr"]');
                if (nvPicPr) {
                    cNvPr = nvPicPr.querySelector('[name="cNvPr"]');
                }
            }
            
            if (!cNvPr) return null;
            
            // Extract attributes
            const descr = cNvPr.getAttribute('descr') || '';
            const name = cNvPr.getAttribute('name') || '';
            const id = cNvPr.getAttribute('id') || '';
            
            // Try to find relationship to image file
            const blip = pic.querySelector('a\\:blip, blip');
            const embedId = blip?.getAttribute('r:embed') || blip?.getAttribute('embed') || '';
            
            return {
                altText: descr,
                shapeName: name,
                shapeId: id,
                embedId: embedId
            };
        } catch (error) {
            console.warn('[PPTXImageExtractor] Error extracting picture data:', error);
            return null;
        }
    }

    /**
     * Find matching image in extracted images
     * @param {Object} imageData - Picture data from XML
     * @returns {Object|null} Matched image object
     */
    findMatchingImage(imageData) {
        // Try to match by shape name
        if (imageData.shapeName) {
            const byName = this.images.find(img => {
                const imgId = img.id.toLowerCase();
                const shapeName = imageData.shapeName.toLowerCase();
                return shapeName.includes(imgId) || imgId.includes(shapeName);
            });
            if (byName) return byName;
        }
        
        // Try to match by embed ID
        if (imageData.embedId) {
            const byEmbed = this.images.find(img => {
                return imageData.embedId.includes(img.id);
            });
            if (byEmbed) return byEmbed;
        }
        
        // Fallback: return first unmatched image
        return this.images.find(img => img.slides.length === 0);
    }

    /**
     * Get images for a specific slide
     * @param {number} slideNumber - Slide number (1-based)
     * @returns {Array} Array of images in slide
     */
    getImagesForSlide(slideNumber) {
        return this.slideImageMap.get(slideNumber) || [];
    }

    /**
     * Get statistics about extracted images
     * @returns {Object} Statistics object
     */
    getImageStats() {
        const totalSize = this.images.reduce((sum, img) => sum + img.size, 0);
        const withAltText = this.images.filter(img => 
            img.altText && img.altText !== img.filename
        ).length;
        
        // Count by format
        const byFormat = {};
        this.images.forEach(img => {
            const ext = img.filename.split('.').pop().toLowerCase();
            byFormat[ext] = (byFormat[ext] || 0) + 1;
        });
        
        return {
            totalImages: this.images.length,
            totalSize: totalSize,
            totalSizeFormatted: Base64Helper.formatSize(totalSize),
            withAltText: withAltText,
            withoutAltText: this.images.length - withAltText,
            averageSize: this.images.length > 0 ? Math.round(totalSize / this.images.length) : 0,
            byFormat: byFormat,
            slidesWithImages: this.slideImageMap.size
        };
    }

    /**
     * Format image as markdown
     * @param {Object} image - Image object
     * @param {boolean} useBase64 - Whether to embed as base64
     * @returns {string} Markdown formatted image
     */
    formatImageMarkdown(image, useBase64 = true) {
        // Clean alt text for markdown
        let altText = image.altText || image.filename;
        altText = altText
            .replace(/[\r\n\[\]]/g, ' ')  // Remove problematic characters
            .replace(/\s+/g, ' ')           // Normalize whitespace
            .trim();
        
        // Limit alt text length
        if (altText.length > 200) {
            altText = altText.substring(0, 197) + '...';
        }
        
        if (useBase64) {
            return `![${altText}](${image.dataURI})`;
        } else {
            return `![${altText}](${image.filename})`;
        }
    }

    /**
     * Format all images for a slide as markdown
     * @param {number} slideNumber - Slide number
     * @param {boolean} useBase64 - Whether to embed as base64
     * @returns {string} Markdown string
     */
    formatSlideImages(slideNumber, useBase64 = true) {
        const images = this.getImagesForSlide(slideNumber);
        if (images.length === 0) return '';
        
        let md = '';
        images.forEach((img, index) => {
            md += this.formatImageMarkdown(img, useBase64);
            if (index < images.length - 1) {
                md += '\n\n';  // Separate multiple images
            }
        });
        
        return md;
    }

    /**
     * Export all images as separate files (for download)
     * @returns {Array} Array of {filename, blob} objects
     */
    exportImages() {
        return this.images.map(img => ({
            filename: img.filename,
            blob: this.base64ToBlob(img.base64, img.mimeType)
        }));
    }

    /**
     * Convert base64 to Blob
     * @param {string} base64 - Base64 string
     * @param {string} mimeType - MIME type
     * @returns {Blob} Blob object
     */
    base64ToBlob(base64, mimeType) {
        const byteCharacters = atob(base64);
        const byteArrays = [];
        
        for (let offset = 0; offset < byteCharacters.length; offset += 512) {
            const slice = byteCharacters.slice(offset, offset + 512);
            const byteNumbers = new Array(slice.length);
            
            for (let i = 0; i < slice.length; i++) {
                byteNumbers[i] = slice.charCodeAt(i);
            }
            
            const byteArray = new Uint8Array(byteNumbers);
            byteArrays.push(byteArray);
        }
        
        return new Blob(byteArrays, { type: mimeType });
    }
}

// Export for use in HTML
if (typeof window !== 'undefined') {
    window.PPTXImageExtractor = PPTXImageExtractor;
}

// Export for Node.js (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PPTXImageExtractor;
}
