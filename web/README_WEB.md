# MarkItDown Web Converter

## 🌐 Browser-Based Version - No Admin Rights Needed!

Run MarkItDown in your web browser - perfect for corporate/managed laptops.

---

## 🚀 Super Simple Setup (3 Steps)

### Step 1: Download the Code

**Download ZIP:**
https://github.com/Wei-power3/markitdown-desktop-converter/archive/refs/heads/web-version.zip

1. Click the link above
2. Save the ZIP file
3. Extract to `Desktop` or `Documents`

### Step 2: Install Dependencies

Open Command Prompt in the `web` folder:

```bash
cd Desktop\markitdown-desktop-converter-web-version\web
pip install -r requirements.txt
```

**Wait 2-3 minutes** for installation to complete.

### Step 3: Start the Server

```bash
python app.py
```

You'll see:
```
🚀 MarkItDown Web Converter Starting...
📍 Open your browser and go to:
   http://localhost:5000
```

---

## 🎉 That's It!

1. **Open your browser** (Chrome, Edge, Firefox)
2. **Go to**: `http://localhost:5000`
3. **Drag and drop** your PDF or PowerPoint files
4. **Click "Start Processing"**
5. **Download** your Markdown files

---

## 📸 What You'll See

### Beautiful Web Interface

```
┌──────────────────────────────────────────┐
│  📄 MarkItDown Web Converter          │
│  Convert PDF and PowerPoint to Markdown │
├──────────────────────────────────────────┤
│                                        │
│          📁 Drag & Drop Files         │
│                  or                   │
│            [Browse Files]             │
│                                        │
│      Supported: PDF, PPTX, PPT         │
├──────────────────────────────────────────┤
│  Processing Queue (2 files)           │
│                                        │
│  ✔ report.pdf         [⬇ Download]   │
│  ⏳ slides.pptx        [====----]    │
│                                        │
│  [▶ Start] [Clear Completed]         │
└──────────────────────────────────────────┘
```

---

## ✅ Features

- 🌐 **Works in any browser** - Chrome, Edge, Firefox, Safari
- 📦 **Batch processing** - Convert multiple files at once
- 📄 **Drag & drop** - Easy file uploads
- 👨‍💻 **No admin rights** - Runs on corporate laptops
- 💾 **Auto-download** - Get Markdown files instantly
- 🎨 **Modern UI** - Beautiful, responsive design

---

## 💻 Daily Usage

### Every time you want to convert files:

```bash
# 1. Open Command Prompt
# 2. Navigate to web folder
cd Desktop\markitdown-desktop-converter-web-version\web

# 3. Start server
python app.py

# 4. Open browser to http://localhost:5000
# 5. Convert your files
# 6. Press Ctrl+C in Command Prompt to stop server when done
```

---

## 🔧 Create a Shortcut (Optional)

Make launching easier:

1. Create file: `LaunchWebConverter.bat`
2. Put this inside:

```batch
@echo off
cd /d "%USERPROFILE%\Desktop\markitdown-desktop-converter-web-version\web"
python app.py
pause
```

3. Double-click the `.bat` file to launch!
4. Browser will open automatically to `http://localhost:5000`

---

## ❓ Troubleshooting

### Server won't start

**Error**: "Address already in use"

**Solution**: Port 5000 is busy. Change port:

```python
# Edit app.py, last line:
app.run(debug=True, host='127.0.0.1', port=5001)  # Use 5001 instead
```

Then visit `http://localhost:5001`

### Can't install dependencies

**Error**: "Access denied" or "Permission denied"

**Solution**: Install to user directory:

```bash
pip install --user -r requirements.txt
```

### Browser can't connect

**Solution**: 
1. Check server is running (you should see output in Command Prompt)
2. Try `http://127.0.0.1:5000` instead
3. Check firewall isn't blocking local connections

---

## 🔒 Security Note

- **Runs 100% locally** - No files uploaded to internet
- **Localhost only** - Only accessible from your computer
- **No data collection** - Everything stays on your machine

---

## 🌟 Why Web Version?

### Perfect for:
- ✅ Corporate/managed laptops
- ✅ Machines with `.exe` restrictions
- ✅ Users without admin rights
- ✅ Cross-platform compatibility (Windows, Mac, Linux)

### Advantages:
- Works in any modern browser
- No installation needed
- Easy to update (just replace files)
- Familiar interface (like any web app)

---

## 👥 Sharing with Team

If your whole team needs this:

### Option 1: Local Network (Advanced)
Run on one computer, access from others on same network:

```python
# Edit app.py, last line:
app.run(debug=False, host='0.0.0.0', port=5000)
```

Others access via: `http://YOUR_IP:5000`

### Option 2: Deploy to Cloud (Advanced)
Deploy to Heroku, AWS, or Azure for internet access

---

## 🚀 Next Steps

1. **Try it now** - Convert a test PDF
2. **Bookmark** `http://localhost:5000` in browser
3. **Create shortcut** for easy access
4. **Share** this guide with colleagues

---

## 📞 Need Help?

- **Issues**: https://github.com/Wei-power3/markitdown-desktop-converter/issues
- **Documentation**: See parent README.md

---

**Made with ❤️ for users with restricted laptops!**