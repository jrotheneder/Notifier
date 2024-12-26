## Notifier - Price & Availability Tracking Bot 

####   Description 
A bot used for scraping data from the websites of selected
fashion retailers, tracking items and notifying by telegram messages upon 
changes in price or availability. The main **features** are: 
* Per-user tracking of multiple variants (sizes, colors) of an item; adding,
  listing and removing items. 
* Notification upon changes in price and availability status of tracked items.
  The bot can be queried to check for changes manually or instructed to do so at
  specified time intervals.
* Export of tracked items to a .json file, restoring the list of tracked items
  from such a file.
* Currently supported retailers (Dec. 24'): **Zara** & **Uniqlo**. 

**Demo**: 

https://github.com/user-attachments/assets/0532228f-b43e-4a1c-9a12-c48b7767f8a7

#### Instructions  
* Notifier can be run (ideally on a server[^1]) by calling `python3
notifier_main.py`. 
* In order to run, there needs to be a `config` folder in the project
root directory with two files,`bot_token.txt` (see the telegram bot tutorial 
["From BotFather to 'Hello World'
"](https://core.telegram.org/bots/tutorial#obtain-your-bot-token)), and
`allowed_users.txt`, containing linewise the telegram handles of allowed users.
* The first user listed in `allowed_users.txt` can issue the command `/shutdown`
  to the bot which terminates the bot graciously and ensures that tracked items
  are stored persistently. 
* For usage instructions, call `/help` from the bot.

[^1]:Some sites (e.g. Uniqlo) require the Selenium framework, for which the
  server should not be too weak. We found a two-core VM.Standard.A1.Flex
  (Ampere/ARM) server from Oracle to be sufficient, while an VM.Standard.E5.Flex
  (AMD) instance proved too slow. To get Selenium running on an arm64 based
  architecture, see [this
  answer](https://stackoverflow.com/a/78946315/5775322) on stackoverflow.

#### Overview of the code

##### Core routines
| file | description | 
| -----------------------------  | ----------------------------- | 
| `notifier_main.py` | Main routine, to be executed on server side.
| `notifier_bot.py` | Core functions of the bot (bot-user interaction, querying, adding & removing products, tracking, updating). 


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




