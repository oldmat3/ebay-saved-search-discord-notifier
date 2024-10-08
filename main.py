from ebaysdk.finding import Connection as Finding
from datetime import datetime
import requests
import time
from ebaysdk.exception import ConnectionError

# eBay API credentials 
app_id = 'ks-auction-PRD-7fccb0fc9-71891308'

# Webhooks
webhook_urls = {
    'iPad Air 2 under $80': 'https://discord.com/api/webhooks/1290178978065285153/0e1ETgIbCVtkDftQpAbeREEXQcoaYK7bxVM0FfotOqv4yP2e5dVAqcFXbx6q91QvzQ9b',
    'iPad 5th Generation under $100': 'https://discord.com/api/webhooks/1290178989704351846/KF3yFkKOqu36K9qqEk5_jL28HoWpqGaLu8XzlbujKYSkpPycbI6mDNa2WSvv_7q0ytxk',
    'iPad 6th Generation under $120': 'https://discord.com/api/webhooks/1291003494136021013/jpP_7qOft1s9qYb4N1vD86Zun22xfISS1ydY4n90_z2m8g6xXpCTCFrANUsdpByephCP',
    'iPad Pro 1st Generation under $150': 'https://discord.com/api/webhooks/1290178988395859979/WtfE0FjH7H1ofteyFjcqIPRFdCSgiODfpiHG1kdjp0zVnjUSapPx8aJ2eQvBYcRSFlYv',
    'Status Updates': 'https://discord.com/api/webhooks/1291251367075119204/iIYyRVY4KNviTdfjr8FvuYGaaFcNqHKjW_N8jOm28pHqfYzqXrKSgddMc2GkkB_16irD'  # New webhook for hourly status
}

# To store previously checked listings
previous_listings = {}

# Keywords to check listing descriptions
keywords_to_check = ['screen line', 'broken', 'poor', 'inflated', 'untested', 'cracked', 'locked', 'lock', 'non-functioning', 'non functioning', 'hardware', 'for parts', 'parts only', 'box only', 'box']

# Send a message to Discord
def send_to_discord(title, price, url, search_name):
    # Select the correct webhook based on search_name
    discord_webhook_url = webhook_urls.get(search_name)

    if not discord_webhook_url:
        print(f"No webhook URL found for '{search_name}'")
        return

    data = {
        "content": f"**New Listing Found for '{search_name}'**\n**Title**: {title}\n**Price**: ${price}\n**URL**: {url}"
    }
    result = requests.post(discord_webhook_url, json=data)
    if result.status_code == 204:
        print(f"Message sent successfully to Discord for '{search_name}'")
    else:
        print(f"Failed to send message to Discord. Status code: {result.status_code}")

# Function to send a start notification to all webhooks
def send_start_notification():
    message = {
        "content": "**Bot has started!** The bot is now checking for new eBay listings."
    }
    for search_name, webhook_url in webhook_urls.items():
        result = requests.post(webhook_url, json=message)
        if result.status_code == 204:
            print(f"Start notification sent successfully to Discord for '{search_name}'")
        else:
            print(f"Failed to send start notification to Discord. Status code: {result.status_code}")

# Check new listings with URL comparison for new/old listings
def check_ebay_listings(search_name, search_params):
    global previous_listings

    # Connect to the eBay API
    api = Finding(appid=app_id, config_file=None, globalid="EBAY-AU")

    # Execute the search query
    try:
        response = api.execute('findItemsAdvanced', search_params)
    except ConnectionError as e:
        print(f"eBay API Connection Error: {e}")
        print(f"Detailed error response: {e.response.dict()}")
        return

    # Get the listings
    if hasattr(response.reply, 'searchResult') and hasattr(response.reply.searchResult, 'item'):
        items = response.reply.searchResult.item
        print(f"Total listings found for '{search_name}': {len(items)}")
    else:
        print(f"No listings found for '{search_name}'")
        return

    new_listings = []
    for item in items:
        title = item.title
        price = float(item.sellingStatus.currentPrice.value)
        url = item.viewItemURL.replace('ebay.com', 'ebay.com.au')
        start_time = item.listingInfo.startTime
        description = item.title

        # Find the 'MaxPrice' value
        max_price = None
        for filter_item in search_params['itemFilter']:
            if filter_item['name'] == 'MaxPrice':
                max_price = float(filter_item['value'])
                break
        
        if max_price is None:
            print(f"MaxPrice filter not found for '{search_name}'")
            continue

        if price > max_price:
            print(f"Listing for '{title}' exceeds max price: ${price}")
            continue

        if any(keyword in description.lower() for keyword in keywords_to_check):
            print(f"Keyword '{keywords_to_check}' found in listing for '{search_name}': {title}")
            continue

        # Create a unique listing entry
        listing_data = {
            'title': title,
            'price': price,
            'url': url,
            'start_time': start_time
        }
        new_listings.append(listing_data)

        # Print all available listings for diagnostics
        print(f"Listing - Title: {title}, Price: ${price}, URL: {url}, Start Time: {start_time}")

    # Continue with previous listing checks

    # Check if any new listings exist for this search
    if search_name in previous_listings:
        previous_urls = [listing['url'] for listing in previous_listings[search_name]]
        for listing in new_listings:
            if listing['url'] not in previous_urls:
                print(f"New listing found for '{search_name}': {listing['title']}")
                send_to_discord(listing['title'], listing['price'], listing['url'], search_name)
            else:
                print(f"Already checked listing for '{search_name}': {listing['title']}")
    else:
        print(f"First time search for '{search_name}', all listings are new.")
        # Notify about all new listings on the first run
        for listing in new_listings:
            send_to_discord(listing['title'], listing['price'], listing['url'], search_name)

    # Update the previous listings for this search
    previous_listings[search_name] = new_listings

# Search configurations
searches = [
    {
        'name': 'iPad Air 2 under $80',
        'params': {
            'keywords': 'ipad',
            'categoryId': '171485',  # Category for Tablets & eBook Readers
            'itemFilter': [
                {'name': 'ListingType', 'value': 'Auction'},
                {'name': 'MaxPrice', 'value': '80'},
                {'name': 'LocatedIn', 'value': 'AU'},  
                {'name': 'Condition', 'value': '3000'},  
            ],
            'aspectFilter': [
                {'aspectName': 'Model', 'aspectValueName': 'Apple iPad Air 2'}
            ],
            'sortOrder': 'StartTimeNewest',
            'paginationInput': {'entriesPerPage': 30}
        }
    },
    {
        'name': 'iPad 5th Generation under $100',
        'params': {
            'keywords': 'ipad',
            'categoryId': '171485', 
            'itemFilter': [
                {'name': 'ListingType', 'value': 'Auction'},
                {'name': 'MaxPrice', 'value': '100'},
                {'name': 'LocatedIn', 'value': 'AU'},  
                {'name': 'Condition', 'value': '3000'},  
            ],
            'aspectFilter': [
                {'aspectName': 'Model', 'aspectValueName': 'Apple iPad (5th Generation)'}
            ],
            'sortOrder': 'StartTimeNewest',
            'paginationInput': {'entriesPerPage': 30}
        }
    },
    {
        'name': 'iPad 6th Generation under $120',
        'params': {
            'keywords': 'ipad',
            'categoryId': '171485',  
            'itemFilter': [
                {'name': 'ListingType', 'value': 'Auction'},
                {'name': 'MaxPrice', 'value': '120'},
                {'name': 'LocatedIn', 'value': 'AU'},  
                {'name': 'Condition', 'value': '3000'}, 
            ],
            'aspectFilter': [
                {'aspectName': 'Model', 'aspectValueName': 'Apple iPad (6th Generation)'}
            ],
            'sortOrder': 'StartTimeNewest',
            'paginationInput': {'entriesPerPage': 30}
        }
    },
    {
        'name': 'iPad Pro 1st Generation under $150',
        'params': {
            'keywords': 'ipad',
            'categoryId': '171485',  
            'itemFilter': [
                {'name': 'ListingType', 'value': 'Auction'}, 
                {'name': 'MaxPrice', 'value': '150'}, 
                {'name': 'LocatedIn', 'value': 'AU'}, 
            ],
            'aspectFilter': [
                {'aspectName': 'Model', 'aspectValueName': 'Apple iPad Pro (1st Generation)'}
            ],
            'sortOrder': 'StartTimeNewest',
            'paginationInput': {'entriesPerPage': 30}
        }
    }
]

# Run the function every minute for all searches
if __name__ == "__main__":
    send_start_notification()  # Notify all webhooks that the bot has started
    while True:
        print("Checking for new eBay listings...")
        for search in searches:
            check_ebay_listings(search['name'], search['params'])
        time.sleep(60)  # Wait 1 minute before checking again
