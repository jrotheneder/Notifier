## Notifier - Price & Availability Tracking Bot 

####   Description 
A bot used for scraping data from the websites of selected
fashion retailers, tracking items and notifying by telegram messages upon 
changes in price or availability.

**Features**: 
* Per-user tracking of changes in price and availability status of selected items.
* Tracking of multiple variants (sizes, colors) of an item.
* Notification by telegram messages. 
* Currently supported (12/24): Zara & Uniqlo. 

#### Overview of the code

##### Core routines
| file | description | 
| -----------------------------  | ----------------------------- | 
| `notifier_bot.py` | Main functions of the bot (bot-user interaction, querying, adding & removing products, tracking, updating). 
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
| `src/product.py`         | Abstract base class for products from various retailers
| `src/zara_product.py`    | Class that encapsulates data about a product tracked from Zara
| `src/uniqlo_product.py`  | Class that encapsulates data about a product tracked from Uniqlo
| `src/zalando_product.py` | Class that encapsulates data about a product tracked from Zalando 
| `src/hm_product.py`      | Class that encapsulates data about a product tracked from H&M
| `src/cos_product.py`     | Class that encapsulates data about a product tracked from COS




