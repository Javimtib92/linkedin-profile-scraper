# Disclaimer

This web scraper is built solely for educational purposes and as a proof of concept. Scraping LinkedIn is against their terms of service, and the use of this tool for scraping LinkedIn profiles or any other website without permission is not allowed. The intention of this project is to demonstrate the capabilities of the Scrapy framework and to provide a learning resource for web scraping techniques. I do not encourage or condone any unauthorized use of this tool.

Please use it responsibly and respect the terms and conditions of the websites you interact with.

# Managing Python Environment

To manage a virtual Python environment and install pip dependencies, I recommend using pyenv. pyenv allows you to switch between different versions of Python and create isolated virtual environments for your projects.

Installation Guide:

You can follow the installation guide provided in the pyenv repository on GitHub: [pyenv Installation Guide](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation)

The reason why I used pyenv is because I can set it up to automatically activate/deactivate python virtual environment when `cd` into the project.

# Installing required dependencies

`pip install -r requirements.txt`

# Customizing LinkedIn Profile URL:

To use the web scraper with your own LinkedIn profile, follow these steps:

1. Open the config.toml file located in the project directory.
2. Locate the [linkedin] section within the file.
3. Uncomment the line that starts with LINKEDIN_PROFILE_URL
4. Replace the placeholder URL "https://www.linkedin.com/in/example-profile/" with your own LinkedIn profile URL.

After completing these steps, the web scraper will use the specified LinkedIn profile URL for data extraction.

## Example:

```toml
[linkedin]
LINKEDIN_PROFILE_URL = "https://www.linkedin.com/in/your-profile/"
```

Ensure that the URL you provide points to your LinkedIn profile to avoid any issues during scraping.

# How to run the web scraper

Navigate to the `src` folder and run the following in your terminal:

```shell
scrapy crawl linkedin_profile
```

If it runs succesfully it will output a json file named `profile.json` in `src/output` folder.

If you want to specify a different configuration for the output you can change it in the `settings.py` file.

```python
FEEDS = {
    "output/profile.json": { # You can change this key if you want to specify a different output directory
        "format": "json",
        "encoding": "utf8",
        "store_empty": False,
        "item_classes": ["linkedin_profile_scraper_javier_munoz_tous.items.Profile"],
        "fields": None,
        "indent": 4,
        "item_export_kwargs": {
            "export_empty_fields": True,
        },
    },
}
```

# Proxy and User Agent Rotation Middlewares

This project is prepared to use a Proxy and User Agent rotation to prevent being blocked from LinkedIn. To activate this behavior modify `DOWNLOADER_MIDDLEWARES` config in `src/linkedin_profile_scraper_javier_munoz_tous/settings.py` and uncomment the commented middlewares.

```python
DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": 90,
    # Uncomment to use proxy and user agent rotation middlewares
    # "scrapy_proxies.RandomProxy": 100,
    # "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": 110,
    # "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
    # "linkedin_profile_scraper_javier_munoz_tous.middlewares.RotateUserAgentMiddleware": 400,
}
```

The list of proxies to be used can be modified in `src/linkedin_profile_scraper_javier_munoz_tous/proxy/list.txt`

The `RotateUserAgentMiddleware` can be found in `src/linkedin_profile_scraper_javier_munoz_tous/middlewares.py`

To know more about random proxy middleware refer to [scrapy-proxies
repository](https://github.com/aivarsk/scrapy-proxies)

# Project Structure

This project can serve as a boilerplate for other web scraping projects using scrapy. There is a lot of auto-generated code created by Scrapy that I didn't remove for reference purposes.
