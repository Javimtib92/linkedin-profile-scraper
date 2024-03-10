import json

import scrapy

from linkedin_profile_scraper_javier_munoz_tous.items import Profile  

class LinkedinProfileSpider(scrapy.Spider):
    name = "linkedin_profile"
    allowed_domains = ["linkedin.com"]
    start_urls = ["https://www.linkedin.com/in/javier-muñoz-tous/"]
     

    def parse(self, response):
        self.log(f"Scraping LinkedIn profile: {response.url}")

       # There's only one script element with application/ld+json on the profile page
        script_elements = response.xpath('//script[@type="application/ld+json"]')

        for script in script_elements:
            json_str = script.xpath('.//text()').get()
            json_content = json.loads(json_str)

            with open('linkedin_profile_data.json', 'w') as json_file:
                json.dump(json_content, json_file, indent=4)
            self.log("Data dumped into linkedin_profile_data.json")

            person_item = None
            for item in json_content["@graph"]:
                if item.get("@type") == "Person":
                    person_item = item
                    break

            job_history_filtered = []
            for job in person_item.get("alumniOf", []):
                if job.get("@type") == "Organization":
                    job_history_filtered.append(job)

            profile_item = Profile(
                name=person_item['name'],
                location=person_item['address']['addressLocality'],
                job_history=job_history_filtered
            )


            print(profile_item);
            
            yield profile_item