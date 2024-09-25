from ebaysdk.finding import Connection as Finding
from datetime import datetime
import requests
import time
from ebaysdk.exception import ConnectionError

# eBay API credentials 
app_id = ''
# Discord webhook URL
discord_webhook_url = ''

# To store previously checked listings for each search
previous_listings = {}

# Send a message to Discord
def send_to_discord(title, price, url, search_name):
    data = {
        "content": f"**New Listing Found for '{search_name}'!**\n**Title**: {title}\n**Price**: ${price}\n**URL**: {url}"
    }
    result = requests.post(discord_webhook_url, json=data)
    if result.status_code == 204:
        print(f"Message sent successfully to Discord for '{search_name}'")
    else:
        print(f"Failed to send message to Discord. Status code: {result.status_code}")

# Check new listings
def check_ebay_listings(search_name, search_params):
    global previous_listings

    # Connect to the eBay API
    api = Finding(appid=app_id, config_file=None, globalid="EBAY-AU")  # Only set the globalid for eBay Australia

    # Execute the search query
    try:
        response = api.execute('findItemsAdvanced', search_params)
    except ConnectionError as e:
        print(f"eBay API Connection Error: {e}")
        print(f"Detailed error response: {e.response.dict()}")  # Print detailed error response for debugging
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
        price = item.sellingStatus.currentPrice.value
        url = item.viewItemURL.replace('ebay.com', 'ebay.com.au')  # Update URL to point to eBay Australia
        start_time = item.listingInfo.startTime

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

    # Check if any new listings exist for this specific search
    if search_name in previous_listings:
        for listing in new_listings:
            if listing not in previous_listings[search_name]:
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
                {'name': 'LocatedIn', 'value': 'AU'},  # Australia only
                {'name': 'Condition', 'value': '3000'},  # Used condition
            ],
            'aspectFilter': [
                {'aspectName': 'Model', 'aspectValueName': 'Apple iPad Air 2'}
            ],
            'sortOrder': 'StartTimeNewest',
            'paginationInput': {'entriesPerPage': 10}
        }
    },
    {
        'name': 'iPad 5th Generation under $100',
        'params': {
            'keywords': 'ipad',
            'categoryId': '171485',  # Category for Tablets & eBook Readers
            'itemFilter': [
                {'name': 'ListingType', 'value': 'Auction'},
                {'name': 'MaxPrice', 'value': '100'},
                {'name': 'LocatedIn', 'value': 'AU'},  # Australia only
                {'name': 'Condition', 'value': '3000'},  # Used condition
            ],
            'aspectFilter': [
                {'aspectName': 'Model', 'aspectValueName': 'Apple iPad (5th Generation)'}
            ],
            'sortOrder': 'StartTimeNewest',
            'paginationInput': {'entriesPerPage': 10}
        }
    },
    {
        'name': 'iPad 6th Generation under $120',
        'params': {
            'keywords': 'ipad',
            'categoryId': '171485',  # Category for Tablets & eBook Readers
            'itemFilter': [
                {'name': 'ListingType', 'value': 'Auction'},
                {'name': 'MaxPrice', 'value': '120'},
                {'name': 'LocatedIn', 'value': 'AU'},  # Australia only
                {'name': 'Condition', 'value': '3000'},  # Used condition
            ],
            'aspectFilter': [
                {'aspectName': 'Model', 'aspectValueName': 'Apple iPad (6th Generation)'}
            ],
            'sortOrder': 'StartTimeNewest',
            'paginationInput': {'entriesPerPage': 10}
        }
    },
    {
        'name': 'iPad Pro 1st Generation under $150',
        'params': {
            'keywords': 'ipad',
            'categoryId': '171485',  # Category for Tablets & eBook Readers
            'itemFilter': [
                {'name': 'ListingType', 'value': 'Auction'},  # Auction listings only
                {'name': 'MaxPrice', 'value': '150'},  # Maximum price of $150
                {'name': 'LocatedIn', 'value': 'AU'},  # Australia only
            ],
            'aspectFilter': [
                {'aspectName': 'Model', 'aspectValueName': 'Apple iPad Pro (1st Generation)'}
            ],
            'sortOrder': 'StartTimeNewest',
            'paginationInput': {'entriesPerPage': 10}
        }
    }
]

# Run the function every minute for all searches
if __name__ == "__main__":
    while True:
        print("Checking for new eBay listings...")
        for search in searches:
            search_name = search['name']
            search_params = search['params']
            check_ebay_listings(search_name, search_params)
        print("Waiting for 60 seconds before the next check...")
        time.sleep(60)  # Wait for 60 seconds before checking again
