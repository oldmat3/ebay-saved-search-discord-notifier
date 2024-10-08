import requests
import json

def send_to_discord(webhook_url, message):
    """Send a message to a Discord webhook."""
    data = {
        "content": message
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
        response.raise_for_status()  # Check if the request was successful
        print("Message sent to Discord successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message to Discord: {e}")

def ebay_api_error_handler(error_response, webhook_url):
    """Handles eBay API connection error and sends 'rate limited' message to Discord if error 10001."""
    try:
        # Check if the error ID is '10001' (rate limit error)
        error = error_response.get('errorMessage', {}).get('error', {})
        
        if error.get('errorId') == '10001':
            # Send the "rate limited" message to the Discord webhook
            send_to_discord(webhook_url, "rate limited")
        else:
            print("No rate limit error detected.")
    
    except Exception as e:
        print(f"An error occurred while handling the eBay API error: {e}")

# Example usage:

# Replace this with your actual Discord webhook URL
discord_webhook_url = 'https://discord.com/api/webhooks/1291251367075119204/iIYyRVY4KNviTdfjr8FvuYGaaFcNqHKjW_N8jOm28pHqfYzqXrKSgddMc2GkkB_16irD'

# Example error response that you provided
error_response = {
    'errorMessage': {
        'error': {
            'errorId': '10001',
            'domain': 'Security',
            'severity': 'Error',
            'category': 'System',
            'message': 'Service call has exceeded the number of times the operation is allowed to be called',
            'subdomain': 'RateLimiter',
            'parameter': [
                {'_name': 'Param1', 'value': 'findItemsAdvanced'},
                {'_name': 'Param2', 'value': 'FindingService'}
            ]
        }
    }
}

# Call the error handler function
ebay_api_error_handler(error_response, discord_webhook_url)
