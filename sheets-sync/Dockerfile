FROM python:3.11-slim

WORKDIR /app

# Install cron
RUN apt-get update && apt-get install -y cron

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the sync script
COPY sync_sheets_data.py .

# Copy the environment file
COPY .env.production /app/.env.production

# Create the log file
RUN touch /var/log/sync.log

# Create a startup script that uses the .env file
RUN echo '#!/bin/bash\n\
# Copy .env file to /etc/environment for cron\n\
cp /app/.env.production /etc/environment\n\
\n\
# Add cron job that sources environment\n\
echo "*/5 * * * * . /etc/environment; /usr/local/bin/python /app/sync_sheets_data.py >> /var/log/sync.log 2>&1" > /etc/cron.d/sync-cron\n\
chmod 0644 /etc/cron.d/sync-cron\n\
\n\
# Apply cron job\n\
crontab /etc/cron.d/sync-cron\n\
# Start cron\n\
exec cron -f' > /start.sh

RUN chmod +x /start.sh

# Use the startup script instead of cron directly
CMD ["/start.sh"] 