// MarkItDown Web Converter - Frontend JavaScript

class MarkItDownApp {
    constructor() {
        this.queue = [];
        this.processing = false;
        this.initializeElements();
        this.attachEventListeners();
    }

    initializeElements() {
        this.dropZone = document.getElementById('dropZone');
        this.fileInput = document.getElementById('fileInput');
        this.queueContainer = document.getElementById('queueContainer');
        this.emptyQueue = document.getElementById('emptyQueue');
        this.queueCount = document.getElementById('queueCount');
        this.processBtn = document.getElementById('processBtn');
        this.clearBtn = document.getElementById('clearBtn');
    }

    attachEventListeners() {
        // Drag and drop
        this.dropZone.addEventListener('dragover', (e) => this.handleDragOver(e));
        this.dropZone.addEventListener('dragleave', (e) => this.handleDragLeave(e));
        this.dropZone.addEventListener('drop', (e) => this.handleDrop(e));
        
        // File input
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        
        // Buttons
        this.processBtn.addEventListener('click', () => this.processQueue());
        this.clearBtn.addEventListener('click', () => this.clearCompleted());
        
        // Click on drop zone
        this.dropZone.addEventListener('click', () => this.fileInput.click());
    }

    handleDragOver(e) {
        e.preventDefault();
        this.dropZone.classList.add('dragover');
    }

    handleDragLeave(e) {
        e.preventDefault();
        this.dropZone.classList.remove('dragover');
    }

    handleDrop(e) {
        e.preventDefault();
        this.dropZone.classList.remove('dragover');
        
        const files = Array.from(e.dataTransfer.files);
        this.uploadFiles(files);
    }

    handleFileSelect(e) {
        const files = Array.from(e.target.files);
        this.uploadFiles(files);
        e.target.value = ''; // Reset input
    }

    async uploadFiles(files) {
        const formData = new FormData();
        files.forEach(file => formData.append('files[]', file));

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            
            // Add uploaded files to queue
            data.uploaded.forEach(file => {
                this.addToQueue(file);
            });

            // Show errors if any
            if (data.errors.length > 0) {
                alert('Some files failed to upload:\n' + data.errors.join('\n'));
            }

        } catch (error) {
            alert('Upload failed: ' + error.message);
        }
    }

    addToQueue(file) {
        const queueItem = {
            id: file.id,
            filename: file.filename,
            path: file.path,
            size: file.size,
            status: 'queued',
            progress: 0,
            outputPath: null
        };

        this.queue.push(queueItem);
        this.renderQueueItem(queueItem);
        this.updateUI();
    }

    renderQueueItem(item) {
        this.emptyQueue.style.display = 'none';

        const itemDiv = document.createElement('div');
        itemDiv.className = 'queue-item';
        itemDiv.id = `item-${item.id}`;

        itemDiv.innerHTML = `
            <div class="status-icon" id="icon-${item.id}">⏸</div>
            <div class="file-info">
                <div class="file-name">${item.filename}</div>
                <div class="file-status" id="status-${item.id}">Queued</div>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" id="progress-${item.id}"></div>
            </div>
            <button class="remove-btn" onclick="app.removeFromQueue('${item.id}')">✕</button>
        `;

        this.queueContainer.appendChild(itemDiv);
    }

    removeFromQueue(id) {
        const item = this.queue.find(i => i.id === id);
        if (item && item.status === 'processing') {
            alert('Cannot remove item while processing');
            return;
        }

        this.queue = this.queue.filter(i => i.id !== id);
        document.getElementById(`item-${id}`).remove();
        this.updateUI();
    }

    updateUI() {
        const count = this.queue.length;
        this.queueCount.textContent = `${count} file${count !== 1 ? 's' : ''}`;
        
        const hasQueued = this.queue.some(i => i.status === 'queued');
        const hasCompleted = this.queue.some(i => i.status === 'complete');
        
        this.processBtn.disabled = !hasQueued || this.processing;
        this.clearBtn.disabled = !hasCompleted;

        if (this.queue.length === 0) {
            this.emptyQueue.style.display = 'block';
        }
    }

    async processQueue() {
        if (this.processing) return;

        this.processing = true;
        this.processBtn.textContent = '⏸ Processing...';
        this.processBtn.disabled = true;

        const queuedItems = this.queue.filter(i => i.status === 'queued');

        for (const item of queuedItems) {
            await this.processItem(item);
        }

        this.processing = false;
        this.processBtn.innerHTML = '<span class="btn-icon">▶</span> Start Processing';
        this.updateUI();
    }

    async processItem(item) {
        item.status = 'processing';
        this.updateItemUI(item, '⏳', 'Processing...', 30, 'status-processing');

        try {
            const response = await fetch('/convert', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ path: item.path })
            });

            if (!response.ok) {
                throw new Error('Conversion failed');
            }

            const data = await response.json();
            
            item.status = 'complete';
            item.outputPath = data.output_filename;
            
            this.updateItemUI(item, '✔', 'Complete', 100, 'status-complete');
            this.addDownloadButton(item);

        } catch (error) {
            item.status = 'error';
            this.updateItemUI(item, '✖', 'Error: ' + error.message, 0, 'status-error');
        }
    }

    updateItemUI(item, icon, statusText, progress, statusClass) {
        const iconEl = document.getElementById(`icon-${item.id}`);
        const statusEl = document.getElementById(`status-${item.id}`);
        const progressEl = document.getElementById(`progress-${item.id}`);

        if (iconEl) iconEl.textContent = icon;
        if (statusEl) {
            statusEl.textContent = statusText;
            statusEl.className = `file-status ${statusClass}`;
        }
        if (progressEl) progressEl.style.width = `${progress}%`;
    }

    addDownloadButton(item) {
        const itemDiv = document.getElementById(`item-${item.id}`);
        const removeBtn = itemDiv.querySelector('.remove-btn');
        
        const downloadBtn = document.createElement('button');
        downloadBtn.className = 'download-btn';
        downloadBtn.textContent = '⬇ Download';
        downloadBtn.onclick = () => this.downloadFile(item.outputPath);
        
        itemDiv.insertBefore(downloadBtn, removeBtn);
    }

    downloadFile(filename) {
        window.location.href = `/download/${filename}`;
    }

    clearCompleted() {
        const completedItems = this.queue.filter(i => i.status === 'complete');
        
        completedItems.forEach(item => {
            document.getElementById(`item-${item.id}`).remove();
        });

        this.queue = this.queue.filter(i => i.status !== 'complete');
        this.updateUI();
    }
}

// Initialize app
const app = new MarkItDownApp();

// Prevent default drag/drop behavior on whole page
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    document.body.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
    }, false);
});