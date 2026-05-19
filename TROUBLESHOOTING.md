# 🔧 Troubleshooting Guide

## Common Issues and Solutions

### 1. Installation Issues

#### Problem: `pip: command not found`
**Solution:**
```bash
# Install pip (if not already installed)
# On macOS:
brew install python3
# On Ubuntu/Debian:
sudo apt-get install python3-pip
# On Windows: Download Python from python.org
```

#### Problem: `Permission denied` when installing packages
**Solution:**
```bash
# Use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# OR use --user flag
pip install --user -r requirements.txt
```

#### Problem: `externally-managed-environment` error
**Solution:**
```bash
# Always use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Runtime Issues

#### Problem: `ModuleNotFoundError: No module named 'streamlit'`
**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate
# Reinstall requirements
pip install -r requirements.txt
```

#### Problem: `sqlite3.OperationalError: table mood_tracking has no column named conversation_context`
**Solution:**
```bash
# Delete the existing database file
rm chatbot.db
# Restart the application
streamlit run app.py
```

#### Problem: Streamlit app won't start or shows "connection refused"
**Solution:**
```bash
# Kill any existing streamlit processes
pkill -f streamlit
# Start with headless mode
streamlit run app.py --server.headless true
# Or specify a different port
streamlit run app.py --server.port 8502
```

### 3. Performance Issues

#### Problem: App is slow or unresponsive
**Solution:**
- Clear chat history using the "Clear Chat History" button
- Restart the Streamlit server
- Check if you have sufficient RAM (minimum 2GB recommended)

#### Problem: NLTK download errors
**Solution:**
```python
# Run this in Python console
import nltk
nltk.download('vader_lexicon')
```

### 4. Deployment Issues

#### Problem: Streamlit Cloud deployment fails
**Solution:**
- Ensure `requirements.txt` is in the root directory
- Check that all imports are correctly specified
- Verify Python version compatibility (3.8+)

#### Problem: Heroku deployment issues
**Solution:**
```bash
# Create Procfile
echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile
# Add runtime.txt
echo "python-3.9.0" > runtime.txt
```

### 5. Database Issues

#### Problem: Database corruption or errors
**Solution:**
```bash
# Backup existing data (if needed)
cp chatbot.db chatbot_backup.db
# Delete corrupted database
rm chatbot.db
# Restart application (will create new database)
streamlit run app.py
```

### 6. Browser Issues

#### Problem: Chatbot interface not loading
**Solution:**
- Clear browser cache and cookies
- Try a different browser (Chrome, Firefox, Safari)
- Disable browser extensions temporarily
- Check if localhost:8501 is accessible

#### Problem: Styling issues or broken layout
**Solution:**
- Hard refresh the page (Ctrl+F5 or Cmd+Shift+R)
- Check browser console for JavaScript errors
- Ensure you're using a modern browser version

## Getting Help

If you're still experiencing issues:

1. **Check the logs**: Look at the terminal output for error messages
2. **Search existing issues**: Check if someone else has reported the same problem
3. **Create a detailed issue report** including:
   - Operating system and version
   - Python version (`python --version`)
   - Error messages (full traceback)
   - Steps to reproduce the issue

## System Requirements

**Minimum Requirements:**
- Python 3.8+
- 2GB RAM
- 500MB free disk space
- Modern web browser

**Recommended:**
- Python 3.9+
- 4GB RAM
- 1GB free disk space
- Chrome or Firefox browser

## Performance Tips

1. **Regular Maintenance:**
   - Clear chat history periodically
   - Restart the app if it becomes slow
   - Keep your Python environment updated

2. **Optimization:**
   - Close unnecessary browser tabs
   - Use the latest version of Streamlit
   - Monitor system resources

3. **Best Practices:**
   - Always use virtual environments
   - Keep dependencies updated
   - Regular backups of important data
