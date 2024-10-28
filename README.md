# Web Scraping Local Poject
### 2023

This was a local project that aimed to streamline the job I used to work at. 

#### Scope
The webapp provided, by a former employer (not disclosed), to manage our workload was slow, poorly designed and un-optimized.
#### Challenges Addressed
-Long processing queue from the network request to HTML rendering.

-The DOM inspection revealed the paged loaded the full case on-request and each update triggered an Ajax call to perform CRUD and, afterwards, reloaded the entire site. This, as well as JS rendered dynamic contents and a deeply nested DOM tree created a really bad user experience and hindered performance

### Temporary Solution
- Phase 1: Web scraping script developed to trigger a data export from the work site to a local document for inspection.
- Phase 2: local development of an LAMP Stack (Laravel 9) API and it's JS powered metric-rendering dashboard and custom template.

#### Notes:
- The .env variables are redacted due to privacy concerns and NDA compliance.
- The scraped application is not disclosed due to the nature of the domain knowledge. 
- This is for demonstration purposes only.
- This is being published on request by the interested party. 

#### This may not execute due to:
- Latest refactoring due to privacy concerns
- Login access was granted with the company's intranet and AD.
- No testing was performed 'Post-Privacy Refactoring' 

### Requirements:
- The file 'requirements.txt' contains the external packages
- The Chrome driver is required and not included (download the proper according to your OS and current Chrome Version)
- Chrome versioning and the chrome driver compatibility may vary, you might be required to downgrade your browser

#### Disclaimer:
This project was developed with the sole purpose to continue learning python, API integration and to streamline repetitive tasks. 
Although are a lot of improvements and optimazion refactoring that can be done, this project is archived and no longer in use.
