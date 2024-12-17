# Notifier
A telegram-python bot used for scraping data from the websites of selected
fashion retailers, tracking items and notifying by telegram messages upon 
changes in price or availability.

#### Overview of the code

##### Core routines
| file | description | 
| -----------------------------  | ----------------------------- | 
| `notifier_bot.py` | Main functions of the bot (e.g. bot-user interaction, querying, adding & removing products, tracking, updating). 
| `notifier.ipynb` | Jupyter notebook used to start and stop the bot, manage persistence & control access. To be executed serverside


##### Extraction / Scraping
| file| description | 
| -----------------------------  | ----------------------------- | 
| `src/zara_scraper.py`    | Class for scraping data from Zara
| `src/zalando_scraper.py` | Class for scraping data from Zalando 
| `src/hm_scraper.py`      | Class for scraping data from H&M 
| `src/cos_scraper.py`     | Class for scraping data from COS
| `src/uniqlo_scraper.py`  | Class for scraping data from Uniqlo

##### Data Representation
| file| description | 
| -----------------------------  | ----------------------------- | 
| `product.py`         | Abstract base class for products from various retailers
| `zara_product.py`    | Class that encapsulates data about a product tracked from Zara
| `zalando_product.py` | Class that encapsulates data about a product tracked from Zalando 
| `hm_product.py`      | Class that encapsulates data about a product tracked from H&M
| `cos_product.py`     | Class that encapsulates data about a product tracked from COS
| `uniqlo_product.py`  | Class that encapsulates data about a product tracked from Uniqlo




