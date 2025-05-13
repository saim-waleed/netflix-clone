import os
import requests
from urllib.parse import urlparse

def download_image(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {save_path}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

# Create directories if they don't exist
os.makedirs('static/images', exist_ok=True)

# Netflix assets
images = {
    'netflix-logo.png': 'https://assets.nflxext.com/en_us/layout/ecweb/netflix-logo.png',
    'avatar.png': 'https://occ-0-2794-2219.1.nflxso.net/dnm/api/v6/K6hjPJd6cR6FpVELC5Pd6ovHRSk/AAAABY20DrC9-11ewwAs6nfEgb1vrORxRPP9IGmlW1WtKuaLIz8VxCx5NryzDK3_ez064IsBGdXjVUT59G5IRuFdqZlCJCneepU.png',
    'featured-thumbnail.jpg': 'https://occ-0-2794-2219.1.nflxso.net/dnm/api/v6/E8vDc_W8CLv7-yMQu8KMEC7Rrr8/AAAABWG8h5uCXRBZNLWZoTh-gO_RwxPNOPwUwkH1VGRz-HV-E9EfkGRrV4n2t4yGbOGqHrEC9cBGCJHBLEs1sdF5IvF5iUYbGpgG.jpg',
    'movie1.jpg': 'https://occ-0-2794-2219.1.nflxso.net/dnm/api/v6/6gmvu2hxdfnQ55LZZjyzYR4kzGk/AAAABd-iJOnLkBO7tPRFS6VNfDmHioAqvaD630vP1dKmMVTLPoz5MXFFzAxb0yQ6f1XJ1ZT_2pdEgHxeK5poCKZUxV2wHc1XLuBbkHE.jpg',
    'movie2.jpg': 'https://occ-0-2794-2219.1.nflxso.net/dnm/api/v6/6gmvu2hxdfnQ55LZZjyzYR4kzGk/AAAABQf9P_q9zfEG9Qs5HF5Hm5BiGiTMQg9EBy_GxpK4N0B7JbV5Ej9IKH-qh2ABfDhLiWJdGhyXuPMgMJXHFx5pl9gWE_KJzjL3cB4.jpg',
    'movie3.jpg': 'https://occ-0-2794-2219.1.nflxso.net/dnm/api/v6/6gmvu2hxdfnQ55LZZjyzYR4kzGk/AAAABSNtJvu8215Gl8GlVv_EEDFMgltlMgvQGUb_8wpfUL6BKCLHa7mZGCjxhGz3nmRQDHupZ8hG8rLB_F-2jU5GBXaTEEYx6_NWGQU.jpg',
}

# Download each image
for filename, url in images.items():
    save_path = os.path.join('static/images', filename)
    download_image(url, save_path)

print("Image download completed!") 