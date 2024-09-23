
# eBay Listings Checker with Discord Notifications

This Python script checks eBay for new auction listings based on custom search criteria, and sends notifications of new listings to a specified Discord webhook. The script runs every minute and supports multiple search configurations.

1. Install Required Packages

First, you'll need to install the necessary dependencies:


pip install ebaysdk requests
# eBay Listings Checker with Discord Notifications

This Python script checks eBay for new auction listings based on custom search criteria, and sends notifications of new listings to a specified Discord webhook. The script runs every minute and supports multiple search configurations.

1. Install Required Packages

First, you'll need to install the necessary dependencies:

```bash
pip install ebaysdk requests
```

2. Create an eBay Developer Account

To use the eBay API, you'll need to create an eBay developer account and get your API keys.

Go to the eBay Developer Program.
Sign up or log in with your eBay account.
Create an application and get the App ID (this is used in the script to authenticate with the eBay API).

# eBay Listings Checker with Discord Notifications

This Python script checks eBay for new auction listings based on custom search criteria, and sends notifications of new listings to a specified Discord webhook. The script runs every minute and supports multiple search configurations.

1. Install Required Packages

First, you'll need to install the necessary dependencies:

```bash
pip install ebaysdk requests
```

2. Create an eBay Developer Account

To use the eBay API, you'll need to create an eBay developer account and get your API keys.

    Go to the eBay Developer Program.
    Sign up or log in with your eBay account.
    Create an application and get the App ID (this is used in the script to authenticate with the eBay API).

3. Create a Discord Webhook

To receive notifications in Discord:

    Go to your Discord server.
    Navigate to the channel settings.
    Under Integrations, create a new webhook.
    Copy the webhook URL for use in the script.

4. Adding Search Criteria
You can add new search criteria by copying the URL from an eBay search and extracting the relevant parameters. For example, the URL:

```perl
https://www.ebay.com.au/sch/i.html?_from=R40&_nkw=ipad&_sacat=171485&LH_Auction=1&Model=Apple%2520iPad%2520%25285th%2520Generation%2529&_dcat=171485&LH_PrefLoc=1&_udhi=80.0&rt=nc&LH_ItemCondition=3000
```

```python
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
```
You can either do this manually or use ChatGPT to extract the values from the URL.
