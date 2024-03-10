from pathlib import Path
import tomllib
import json
import logging

import scrapy

from linkedin_profile_scraper_javier_munoz_tous.items import Profile


CONFIG_PATH = Path(__file__).resolve().parents[2] / "config.toml"


class LinkedinProfileSpider(scrapy.Spider):
    AUTOTHROTTLE_ENABLED = True
    AUTOTHROTTLE_START_DELAY = 10
    handle_httpstatus_list = [
        999
    ]  # Allows spider to handle 999 status code respones (Custom response from LinkedIn when IP gets blocked)
    rotate_user_agent = True  # Activates User Agent Rotation middleware

    name = "linkedin_profile"
    allowed_domains = ["linkedin.com"]

    def __init__(self, *args, **kwargs):
        super(LinkedinProfileSpider, self).__init__(*args, **kwargs)
        self.config = self.read_config()

    def read_config(self):
        try:
            with open(CONFIG_PATH, "rb") as file:
                config = tomllib.load(file)
            return config
        except FileNotFoundError:
            logging.error("Error: config.toml file not found!")
            return None

    def start_requests(self):
        if self.config:
            linkedin_profile_url = self.config.get("linkedin", {}).get(
                "LINKEDIN_PROFILE_URL"
            )
            if linkedin_profile_url:
                yield scrapy.Request(linkedin_profile_url, callback=self.parse)
            else:
                logging.error("Error: LINKEDIN_PROFILE_URL not found in config.")
        else:
            logging.error("Exiting...")

    def parse(self, response):
        logging.info(f"Scraping LinkedIn profile: {response.url}")

        # Extracting JSON data from script elements
        script_elements = response.xpath('//script[@type="application/ld+json"]')
        json_content = {}

        if not script_elements:
            yield scrapy.Request(url=response.url, dont_filter=True)

        for script in script_elements:
            json_str = script.xpath(".//text()").get()
            json_content.update(json.loads(json_str))

        # Processing the JSON content
        person_item = next(
            (
                item
                for item in json_content.get("@graph", [])
                if item.get("@type") == "Person"
            ),
            None,
        )

        if person_item:
            job_history_filtered = self.filter_jobs(
                person_item.get("alumniOf", []), "Organization"
            )
            education_history_filtered = self.filter_jobs(
                person_item.get("alumniOf", []), "EducationalOrganization"
            )

            # Creating profile item
            profile_item = Profile(
                name=person_item.get("name", ""),
                image_url=person_item.get("image", {}).get("contentUrl", None),
                location=person_item.get("address", {}).get("addressLocality", ""),
                job_history=job_history_filtered,
                education_history=education_history_filtered,
            )

            yield profile_item

    def transform_organization_data(self, data):
        return {
            "name": data.get("name", ""),
            "description": data.get("member", {}).get("description"),
            "startDate": data.get("member", {}).get("startDate"),
            "endDate": data.get("member", {}).get("endDate"),
        }

    def filter_jobs(self, jobs, job_type):
        filtered_jobs = []
        for job in jobs:
            if job.get("@type") == job_type:
                filtered_jobs.append(self.transform_organization_data(job))
        return filtered_jobs
