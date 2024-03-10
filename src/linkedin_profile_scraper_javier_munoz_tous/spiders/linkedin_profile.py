import json

import scrapy

from linkedin_profile_scraper_javier_munoz_tous.items import Profile


class LinkedinProfileSpider(scrapy.Spider):
    AUTOTHROTTLE_ENABLED = True
    AUTOTHROTTLE_START_DELAY = 10
    handle_httpstatus_list = [999]
    rotate_user_agent = True

    name = "linkedin_profile"
    allowed_domains = ["linkedin.com"]
    start_urls = ["https://www.linkedin.com/in/javier-muñoz-tous/"]

    def parse(self, response):
        self.log(f"Scraping LinkedIn profile: {response.url}")

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

            # Dumping data into JSON file
            with open("linkedin_profile_data.json", "w") as json_file:
                json.dump(json_content, json_file, indent=4)
            self.log("Data dumped into linkedin_profile_data.json")

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
