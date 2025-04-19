FROM python:3.11-slim

WORKDIR /app

# Install cron
RUN apt-get update && apt-get install -y cron

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the sync script
COPY sync_sheets_data.py .

# Create the log file
RUN touch /var/log/sync.log

# Add crontab file
RUN echo "0 * * * * /usr/local/bin/python /app/sync_sheets_data.py >> /var/log/sync.log 2>&1" > /etc/cron.d/sync-cron
RUN chmod 0644 /etc/cron.d/sync-cron

# Run cron in the foreground
CMD ["cron", "-f"] 