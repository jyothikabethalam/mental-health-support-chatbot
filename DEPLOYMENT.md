# 🚀 Deployment Guide

## Overview
This guide covers different ways to deploy your Mental Health Chatbot so others can access it online.

## 🌟 Option 1: Streamlit Cloud (Recommended for Students)

**Pros:** Free, easy, automatic updates from GitHub
**Cons:** Limited resources, public repositories only

### Steps:
1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file path: `app.py`
   - Click "Deploy!"

3. **Configuration:**
   - Streamlit will automatically detect `requirements.txt`
   - Your app will be available at: `https://your-app-name.streamlit.app`

## 🔧 Option 2: Heroku

**Pros:** More control, custom domains, database add-ons
**Cons:** Paid plans for continuous usage

### Prerequisites:
- Heroku account
- Heroku CLI installed

### Steps:
1. **Create Heroku Files:**
   ```bash
   # Create Procfile
   echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile
   
   # Create runtime.txt (optional)
   echo "python-3.9.18" > runtime.txt
   ```

2. **Deploy to Heroku:**
   ```bash
   # Login to Heroku
   heroku login
   
   # Create Heroku app
   heroku create your-chatbot-name
   
   # Deploy
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

3. **Open your app:**
   ```bash
   heroku open
   ```

## 🐳 Option 3: Docker Deployment

**Pros:** Consistent environment, works anywhere
**Cons:** Requires Docker knowledge

### Steps:
1. **Create Dockerfile:**
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   EXPOSE 8501
   
   CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
   ```

2. **Build and Run:**
   ```bash
   # Build Docker image
   docker build -t mental-health-chatbot .
   
   # Run container
   docker run -p 8501:8501 mental-health-chatbot
   ```

## ☁️ Option 4: Cloud Platforms

### Google Cloud Platform (GCP)
```bash
# Install Google Cloud SDK
# Deploy to Cloud Run
gcloud run deploy --source .
```

### AWS (Amazon Web Services)
- Use AWS Elastic Beanstalk
- Upload your code as a ZIP file
- Configure Python environment

### Microsoft Azure
- Use Azure App Service
- Deploy directly from GitHub

## 🔒 Option 5: Self-Hosted (Advanced)

**For running on your own server:**

### Using nginx + gunicorn:
1. **Install dependencies:**
   ```bash
   sudo apt update
   sudo apt install nginx python3-pip
   ```

2. **Configure nginx:**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:8501;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

3. **Run with systemd:**
   ```bash
   # Create service file
   sudo nano /etc/systemd/system/chatbot.service
   ```
   
   ```ini
   [Unit]
   Description=Mental Health Chatbot
   After=network.target
   
   [Service]
   User=your-username
   WorkingDirectory=/path/to/your/app
   ExecStart=/path/to/venv/bin/streamlit run app.py
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

## 📊 Monitoring and Analytics

### Basic Monitoring:
- Check app logs regularly
- Monitor resource usage
- Set up uptime monitoring

### Streamlit Cloud:
- Built-in analytics dashboard
- Resource usage metrics
- Error tracking

### Heroku:
```bash
# View logs
heroku logs --tail

# Monitor metrics
heroku ps
```

## 🔐 Security Considerations

### Environment Variables:
```python
import os
# Use environment variables for sensitive data
SECRET_KEY = os.environ.get('SECRET_KEY', 'default-key')
```

### HTTPS:
- Most platforms provide HTTPS automatically
- For self-hosted: Use Let's Encrypt certificates

### Rate Limiting:
```python
# Add to your Streamlit app
import streamlit as st
from datetime import datetime, timedelta

# Simple rate limiting
if 'last_request' not in st.session_state:
    st.session_state.last_request = datetime.now()

time_diff = datetime.now() - st.session_state.last_request
if time_diff < timedelta(seconds=1):  # 1 second cooldown
    st.warning("Please wait before sending another message.")
```

## 🎯 Best Practices

1. **Environment Management:**
   - Use different environments for development/production
   - Keep dependencies updated
   - Use version pinning in requirements.txt

2. **Database Considerations:**
   - For production: Consider PostgreSQL instead of SQLite
   - Regular backups
   - Data privacy compliance

3. **Performance:**
   - Enable caching where appropriate
   - Optimize database queries
   - Monitor memory usage

4. **User Experience:**
   - Add loading indicators
   - Handle errors gracefully
   - Provide clear feedback

## 🆘 Deployment Troubleshooting

### Common Issues:

1. **Build Failures:**
   - Check requirements.txt formatting
   - Verify Python version compatibility
   - Review build logs for specific errors

2. **Runtime Errors:**
   - Check environment variables
   - Verify file paths
   - Monitor resource limits

3. **Database Issues:**
   - Ensure proper database setup
   - Check connection strings
   - Verify permissions

### Getting Help:
- Platform-specific documentation
- Community forums
- Support tickets for paid services

## 📈 Scaling Considerations

### When to Scale:
- High user traffic
- Slow response times
- Resource limitations

### Scaling Options:
- Upgrade to paid plans
- Use load balancers
- Implement caching
- Database optimization

---

**Remember:** Start simple with Streamlit Cloud, then scale up as needed based on your requirements and user base!
