import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_favicon_url(website_url):
    try:
        # Fetch the website content
        response = requests.get(website_url)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the link to the favicon
        icon_link = soup.find("link", rel=lambda x: x and 'icon' in x.lower())
        if icon_link:
            favicon_url = urljoin(website_url, icon_link['href'])
            print(f"Found favicon link: {favicon_url}")
            return favicon_url
        
        # Additional common favicon locations
        common_favicon_paths = [
            '/favicon.ico',
            '/favicon.png',
            '/favicon.svg',
            '/favicon.jpg'
        ]

        for path in common_favicon_paths:
            fallback_url = urljoin(website_url, path)
            try:
                # Check if the fallback URL actually exists
                check_response = requests.head(fallback_url)
                if check_response.status_code == 200:
                    print(f"Found favicon at fallback location: {fallback_url}")
                    return fallback_url
            except requests.RequestException:
                continue

        print("No favicon found.")
        return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching favicon: {e}")
        return None

# Example usage
website_url = "https://docs.godotengine.org/en/stable/index.html"  # Use a known website
favicon = get_favicon_url(website_url)
print(f"Favicon URL: {favicon}")
