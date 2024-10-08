import requests

# eBay API endpoint for checking rate limit status
url = "https://api.ebay.com/developer/analytics/v1_beta/rate_limit/"

# eBay API credentials (replace with your actual credentials)
headers = {
    "Authorization": "Bearer v^1.1#i^1#f^0#I^3#r^0#p^1#t^H4sIAAAAAAAAAOVYXWwUVRTebbclhUKLGDGbBtZBfCjO7p396+7YXVz6ky4/3ZYtBYoFZ2futGNnZ4a5d9yuxKRppA8E/E3rQ3lAguHBKOIDxqA0khiCVQNIgKJGQqIhViPgTxNjxZnptmwLAmFX08R92cy55577fd89594zA3qKSyr7GvrG5lvnFOzrAT0FVis1D5QUF61YUFhgL7KALAfrvp5He2y9hVeqEZMUFXo9RIosIejoTooSok1jiNBUiZYZJCBaYpIQ0Zil45F1a2m3E9CKKmOZlUXCEa0NETDg91NuD5WAfjYR8Ad1qzQZs0UOEb4qD8/xPhCkQBXPen36OEIajEoIMxIOEW7g9pIUIEGgBXhpKkB7/c4qqqqNcLRCFQmypLs4ARE24dLmXDUL652hMghBFetBiHA0Uh+PRaK1dY0t1a6sWOGMDnHMYA1Nf6qROehoZUQN3nkZZHrTcY1lIUKEKzyxwvSgdGQSzH3AN6XmKcAH+QBgOZbzQE8wL1LWy2qSwXfGYVgEjuRNVxpKWMDpuymqq5F4BrI489Soh4jWOoy/Zo0RBV6AaoioWxXZHGlqIsJdiGQ01qBKNq2vJfVMYROAZ4NkFRUIUh4QyKwwESaj74wlamSJE4wQyNEo41VQhwtnigKyRNGdYlJMjfDYgJLt558UD+h+rsnt03CnZGwoTOoKOMzHu0s/NRtjVUhoGE5FmDlgahMiGEUROGLmoJmEmbzpRiGiE2OFdrlSqZQz5XHKaofLDQDl2rRubZzthEmGmPIVjFq/+wRSMKmwUJ+JBBqnFR1Lt56kOgCpgwj7gDfgDmZ0nw4rPNN6iyGLs2t6KeSrNPwJL08FfZyX4yEIgnxURjiTnC4DBkwwaTLJqF0QKyLDQpLV00xLQlXgaI+Pd3sCPCQ5f5AnvUGeJxM+zk9SPIQAwkSCDQb+FwVyrykeh6wKcT5zPPf8rmn0NyTZlHdj3erN7tWwbsU6l7u1Xq7tEFNCM9epRbGnqWHN9lXehubQvVbBbcnXiIKuTIu+/r8ggFHrOYjQICMMuZzoxVlZgU2yKLDp2bXBHpVrYlScjkNR1A05kYwoSjSvZ3Tu9O71fLg/wnm/lP7rC+m2rJCRq7OLlTEf6QEYRXAad46TlZMumdF7DcO0zUScYWfU+v3xFvQedVax1klOsBW4iebSaVJ2omdZpwqRrKl6X+2MGS1Xi9wFJf0iw6osilBtpXIu5GRSw0xChLOtovOQ4AIzy25Zqsod8Pgpyu3PiRdr3qHbZtuRlLcz+Jb22Vb5zw20a/p7fNhi/qhe63HQaz1WYLWCarCcWgYeKS7cYCsstSMBQ6fA8E4kdEj666kKnV0wrTCCWrDIcn1/f0ONvS42ULmjJX1q8ISlNOszwr528PDUh4SSQmpe1lcFUHFzpIgqWzzf7aUACAAvFfD628Cym6M26iHbg7CseKz6Mgx91H8wntg4sHRoYbcPzJ9yslqLLLZeq6VLqhwSK4Z3V1T030geXPlqbGvZUBkaOdK66/Q816d7ly92l47NfRtt+P6TS50fN5/9sf2o+tKSc65vF1z55gL88oEP/jg0GoGr7aXLj9q3jPe9VTIifnVp8yFH+YHhk4ta1UXvjp6/3FHcV35kz4oXLEvHPy96ee/V/T+P72m7Rp/flFzSfXH84vP7b+w49su1M1+PjBwutx37LrVr15zrK39PKVfxdvub711/SrV/ce74mZXVp3+d8+Spi4uf3ukZGNz5zqUtZ5+oqOfnPvfnGye2HtYOXRhNVBx4fyh8suDwmh17XyNe3z384W6pfcFvw7GxWPtjLyqPt10Y5H/6YXRssL+c3fpKhLaxf322cGIv/wa7RiAE4BEAAA==",
    "Content-Type": "application/json"
}

# Send GET request to the eBay API
response = requests.get(url, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    rate_limit_data = response.json()
    
    # Extract the relevant rate limit information
    rate_limits = rate_limit_data.get("rateLimits", [])
    
    if rate_limits:
        # Loop through the rate limits and find the "remaining" and "reset" values
        for limit in rate_limits:
            for resource in limit.get("resources", []):
                for rate in resource.get("rates", []):
                    requests_left = rate.get("remaining", "N/A")
                    reset_time = rate.get("reset", "N/A")
                    
                    # Print the rate limit information
                    print(f"Resource: {resource['name']}")
                    print(f"Requests Left: {requests_left}")
                    print(f"Time Until Reset: {reset_time}")
                    print("-" * 40)
    else:
        print("No rate limit information found.")
else:
    # Handle errors
    print(f"Error: {response.status_code} - {response.text}")
