#!/bin/bash

# Script to execute 'fetch_prs.py' every 5 minutes
while true; do
    python3 fetch_prs.py josephp1005/ai-b2b-saas
    sleep 300  # Sleep for 5 minutes (300 seconds)
done