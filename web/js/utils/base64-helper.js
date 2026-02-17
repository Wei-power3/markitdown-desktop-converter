/**
 * Base64 Encoding Utilities
 * 
 * Provides utilities for encoding images and files to Base64 format,
 * detecting MIME types, and generating data URIs.
 * 
 * @class Base64Helper
 * @version 2.4.3
 * @date February 2026
 */

class Base64Helper {
    /**
     * Convert File/Blob to Base64 string
     * @param {Blob|File} blob - File or Blob to convert
     * @returns {Promise<string>} Base64 string (without data URI prefix)
     */
    static async fileToBase64(blob) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onloadend = () => {
                // Remove data URI prefix (e.g., "data:image/png;base64,")
                const base64 = reader.result.split(',')[1];
                resolve(base64);
            };
            reader.onerror = reject;
            reader.readAsDataURL(blob);
        });
    }

    /**
     * Convert ArrayBuffer to Base64 string
     * @param {ArrayBuffer} buffer - ArrayBuffer to convert
     * @returns {string} Base64 string
     */
    static arrayBufferToBase64(buffer) {
        let binary = '';
        const bytes = new Uint8Array(buffer);
        const len = bytes.byteLength;
        
        for (let i = 0; i < len; i++) {
            binary += String.fromCharCode(bytes[i]);
        }
        
        return btoa(binary);
    }

    /**
     * Get MIME type from filename
     * @param {string} filename - File name with extension
     * @returns {string} MIME type
     */
    static getImageMimeType(filename) {
        const ext = filename.split('.').pop().toLowerCase();
        
        const mimeTypes = {
            // Images
            'png': 'image/png',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'gif': 'image/gif',
            'svg': 'image/svg+xml',
            'webp': 'image/webp',
            'bmp': 'image/bmp',
            'ico': 'image/x-icon',
            'tiff': 'image/tiff',
            'tif': 'image/tiff'
        };
        
        return mimeTypes[ext] || 'image/png';  // Default to PNG
    }

    /**
     * Get MIME type for any file
     * @param {string} filename - File name with extension
     * @returns {string} MIME type
     */
    static getMimeType(filename) {
        const ext = filename.split('.').pop().toLowerCase();
        
        const mimeTypes = {
            // Images
            'png': 'image/png',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'gif': 'image/gif',
            'svg': 'image/svg+xml',
            'webp': 'image/webp',
            
            // Documents
            'pdf': 'application/pdf',
            'doc': 'application/msword',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'xls': 'application/vnd.ms-excel',
            'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'ppt': 'application/vnd.ms-powerpoint',
            'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            
            // Text
            'txt': 'text/plain',
            'csv': 'text/csv',
            'html': 'text/html',
            'css': 'text/css',
            'js': 'text/javascript',
            'json': 'application/json',
            'xml': 'application/xml',
            
            // Archives
            'zip': 'application/zip',
            'tar': 'application/x-tar',
            'gz': 'application/gzip'
        };
        
        return mimeTypes[ext] || 'application/octet-stream';
    }

    /**
     * Create data URI from Base64 data
     * @param {string} base64Data - Base64 encoded data
     * @param {string} mimeType - MIME type
     * @returns {string} Complete data URI
     */
    static createDataURI(base64Data, mimeType) {
        return `data:${mimeType};base64,${base64Data}`;
    }

    /**
     * Decode Base64 string to ArrayBuffer
     * @param {string} base64 - Base64 string
     * @returns {ArrayBuffer} Decoded data
     */
    static base64ToArrayBuffer(base64) {
        const binaryString = atob(base64);
        const bytes = new Uint8Array(binaryString.length);
        
        for (let i = 0; i < binaryString.length; i++) {
            bytes[i] = binaryString.charCodeAt(i);
        }
        
        return bytes.buffer;
    }

    /**
     * Get file size from Base64 string
     * @param {string} base64 - Base64 string
     * @returns {number} Size in bytes
     */
    static getBase64Size(base64) {
        // Remove padding
        const padding = (base64.match(/=/g) || []).length;
        
        // Calculate size (3 bytes per 4 base64 characters)
        return (base64.length * 3) / 4 - padding;
    }

    /**
     * Format file size to human readable string
     * @param {number} bytes - Size in bytes
     * @returns {string} Formatted size (e.g., "1.5 MB")
     */
    static formatSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    /**
     * Check if Base64 string is valid
     * @param {string} str - String to check
     * @returns {boolean} True if valid Base64
     */
    static isValidBase64(str) {
        try {
            return btoa(atob(str)) === str;
        } catch (err) {
            return false;
        }
    }

    /**
     * Extract MIME type from data URI
     * @param {string} dataURI - Data URI string
     * @returns {string} MIME type or empty string
     */
    static getMimeFromDataURI(dataURI) {
        const match = dataURI.match(/^data:([^;]+);/);
        return match ? match[1] : '';
    }

    /**
     * Extract Base64 data from data URI
     * @param {string} dataURI - Data URI string
     * @returns {string} Base64 string or empty string
     */
    static getBase64FromDataURI(dataURI) {
        const parts = dataURI.split(',');
        return parts.length > 1 ? parts[1] : '';
    }
}

// Export for use in HTML
if (typeof window !== 'undefined') {
    window.Base64Helper = Base64Helper;
}

// Export for Node.js (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Base64Helper;
}
