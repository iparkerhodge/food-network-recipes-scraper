# Food Network Recipe Scraper
#### A simple web scraper to get all of the recipes from Food Network

## Usage (Mac OS only)
###### Requirements
- Python 3
- Pip
- Docker
- Scrapy
- Splash

###### Recommendations
You may want to use Anaconda or some other environment manager.

#### Installations
1. Clone this repository from within your desired directory.
2. Check that Python 3 is installed `python3 --version`
3. Check that Pip is installed `pip --version`
4. Install Scrapy. If using Anaconda run `conda install -c conda-forge scrapy`. Or `pip install Scrapy` otherwise.
5. Install Splash. If you do not have docker installed on your system, first install [Docker](https://www.docker.com/). Then, from your terminal run `docker pull scrapinghub/splash` to get a Splash image.
6. Run `pip install scrapy-splash` to get the scrapy-splash library.

#### Running the scraper
1. First, start Splash with `docker run -p 8050:8050 scrapinghub/splash`
2. Then run the spider with `scrapy crawl recipes -o test.json` to get a test output from the spider.
