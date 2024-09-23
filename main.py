from ebaysdk.finding import Connection as Finding
from datetime import datetime
import requests
import time

# eBay API credentials 
app_id = 'YourActualAppIDFromEBay'
# Discord webhook URL
discord_webhook_url = 'https://discord.com/api/webhooks/your-webhook-id'

# To store previously checked listings for each search
previous_listings = {}

# send a message to Discord
def send_to_discord(title, price, url, search_name):
    data = {
        "content": f"**New Listing Found for '{search_name}'!**\n**Title**: {title}\n**Price**: ${price}\n**URL**: {url}"
    }
    result = requests.post(discord_webhook_url, json=data)
    if result.status_code == 204:
        print(f"Message sent successfully to Discord for '{search_name}'")
    else:
        print(f"Failed to send message to Discord. Status code: {result.status_code}")

# check new listings
def check_ebay_listings(search_name, search_params):
    global previous_listings

    # connect to the eBay API
    api = Finding(appid=app_id, config_file=None, siteid="15")  # siteid 15 is for eBay Australia

    # Execute the search query
    response = api.execute('findItemsAdvanced', search_params)

    # Get the listings
    new_listings = []
    items = response.reply.searchResult.item

    for item in items:
        title = item.title
        price = item.sellingStatus.currentPrice.value
        url = item.viewItemURL
        start_time = item.listingInfo.startTime

        # Create a unique listing entry
        listing_data = {
            'title': title,
            'price': price,
            'url': url,
            'start_time': start_time
        }
        new_listings.append(listing_data)

    # Check if any new listings exist for this specific search
    if search_name in previous_listings:
        for listing in new_listings:
            if listing not in previous_listings[search_name]:
                print(f"New listing found for '{search_name}': {listing['title']}")
                send_to_discord(listing['title'], listing['price'], listing['url'], search_name)
            else:
                print(f"Already checked listing for '{search_name}': {listing['title']}")

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
        'name': 'iPad 5th Generation under $80',
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
                {'aspectName': 'Model', 'aspectValueName': 'Apple iPad (5th Generation)'}
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
