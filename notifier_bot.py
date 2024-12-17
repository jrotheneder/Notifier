from uuid import uuid4
import json
import os, sys, tempfile
import urllib.request, urllib.parse
from datetime import datetime

# Add the 'src' folder to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from exceptions import * 
from zara_product import *
from zalando_product import *
from uniqlo_product import *
from cos_product import *
from hm_product import *


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, PicklePersistence
from telegram import InputMediaPhoto, ParseMode
from telegram.utils.helpers import escape_markdown

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO, filename = "notifier.log", filemode = 'w')

def add(update, context):

    product = construct_product(update, context)
    if(product == None): # nothing found, user has been informed, return
        return
        
    # add to list of tracked items 
    if('fashion_items' not in context.user_data):
        context.user_data['fashion_items'] = {}
        
    user_items = context.user_data['fashion_items']

    sku = product.dict['sku']
    
    if(sku not in user_items):
        user_items[sku] = product

        msg = "Item added succesfully\n\n" + str(product) + "\n"

        context.bot.send_message(chat_id=update.effective_chat.id, 
        text=msg)
        
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, 
        text= "Item already tracked")

def construct_product(update, context): 

    url = context.args[0] # second arg should be size or sku
    product = None

    try: # determine site, construct Product

        # TODO these checks are problematic if we add zara home; see also
        # restore function
        if('zalando' in url):
            item_identifier = context.args[1]
            product = ZalandoProduct.fromUrlSize(url, item_identifier) 

        elif('zara' in url):
            item_identifier = context.args[1]
            if(len(item_identifier) < 5): # size
                product = ZaraProduct.fromUrlSize(url, item_identifier)
            else:
                product = ZaraProduct.fromUrlSku(url, item_identifier)

        elif('uniqlo' in url):
            item_identifier = context.args[1]
            product = UniqloProduct.fromUrlSize(url, item_identifier) 

        elif('cosstores' in url): 
            product = CosProduct.fromUrl(url) 

        elif('hm' in url): 
            product = HmProduct.fromUrl(url) 

        else:
            raise UnknownCommandError("neither zalando, zara nor uniqlo url \
            found in add()") 

    except (SkuNotFoundException, UnknownCommandError) as ex:
        context.bot.send_message(chat_id=update.effective_chat.id, 
            text=str(ex))

    except Exception as ex:
        context.bot.send_message(chat_id=update.effective_chat.id, 
            text=str(ex))
        raise

    return product

def remove(update, context):

    skus = context.args
    
    for sku in skus: 
        try:
            del context.user_data['fashion_items'][sku]
            msg = "Item " + sku + " removed succesfully"
        except KeyError:
            msg = "Item " + sku + " was not tracked or sku not found"
        
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                 text=msg)
    
def empty(update, context):
    
    try:
        del context.user_data['fashion_items']
        msg = "Deleted all items succesfully"
    except KeyError:
        msg = "Nothing to delete"
        
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text=msg)
   
            
def list_tracked_items(update, context):
    
    user_items = context.user_data.get('fashion_items')
    messages = []

    if(user_items != None and len(user_items) > 0):

        groups = {}
        for key, item in user_items.items(): 

            ptype = item.productType()

            if ptype not in groups:
                groups[ptype] = [item]
            else:
                groups[ptype].append(item)

        messages.append("Currently tracking " + str(len(user_items))\
            + " items:")

        for groupname, group in groups.items(): 
            
            messages.append("\n\n*" + groupname.capitalize() + ":* " + str(len(group))\
                    + " item\(s\)\n\n" + "\n\n".join([escape_markdown(str(item), 2) for \
                    item in group]) + "\n\n") 
    else:
        messages.append("Currently, no items are tracked")
        
    
    for msg in messages: 
        splits = split_messages(msg)
        for m in splits: 
            context.bot.send_message(chat_id=update.effective_chat.id, 
                                 text=m, parse_mode=ParseMode.MARKDOWN_V2)
    
def command_item_info(update, context): # called via info command
        
    url = ZaraScraper.cleanUrl(context.args[0])

    if('zara' in url): 
        zara_item_info_helper(update, context, url)
        return

    else: # assume we got a size to the url
        try: 
            product = construct_product(update, context)

            if(product != None): 
                context.bot.send_message(chat_id=update.effective_chat.id, 
                    text=str(product))
                return

        except Exception as ex: 

            logging.info("Error in /info command:\n" + str(ex)  + "\n\n")
            context.bot.send_message(chat_id=update.effective_chat.id, \
                    text= "Error " + str(ex) + "\n Send a zara url or other url \
                     + size to get item information")

def default_item_info(update, context): # called as default without command

    url = ZaraScraper.cleanUrl(update.message.text)

    if('zara' in url):
        zara_item_info_helper(update, context, url)

    else:
        context.bot.send_message(chat_id=update.effective_chat.id, \
                text= "send a zara url to get item information")
        raise UnknownCommandError("Unknown command")
        
def zara_item_info_helper(update, context, url): 
    """
    Helper function for info command. Given a zara url, it extracts
    summary information about the available variants of the item
    and sends this information to the user.
    """
    try:
        [name, skus, skus_sans_sizes, size_dict, image_url_dict, color_dict] \
            = ZaraScraper.skuSummary(ZaraScraper.getProductList(url))
    
        msg = "Product: " + name + "\nUrl: " + url + "\nfound "\
                + str(len(skus_sans_sizes)) + " colors and "\
                + str(len(set(size_dict.values()))) + " sizes\n\n" \
                + "Listing SKUs along with some pictures: \n\n"

        context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

        # send images so user can associate skus with colors
        for sku_sans_size in skus_sans_sizes: 

            img_url = image_url_dict[sku_sans_size]  
            color = color_dict[sku_sans_size]
            img_msg = "Color: " + color + ", " +\
                    "Image: [[[" + "1" + "]]](" + img_url + ")"

            context.bot.send_message(chat_id=update.effective_chat.id,
                    text=img_msg, parse_mode=ParseMode.MARKDOWN_V2)

            for sku in skus: 
                if sku_sans_size in sku: 

                    # NOTE: as of late, sizes are explicitly given in the json
                    # so we can just extract the size from the sku
#                     sizeCode = str(sku.split('-')[-1])
#                     if sizeCode in ZaraScraper.numToSize: 
#                         sizeCode = " (" + ZaraScraper.numToSize[sizeCode] + ")"
#                     else: 
#                         sizeCode = ""

                    sizeCode = " (" + size_dict[sku] + ")"
                    msg = sku + sizeCode
                    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


    except SkuNotFoundException as ex:
        context.bot.send_message(chat_id=update.effective_chat.id, 
            text=str(ex))
            
def msg(update, context):
    
    msg = " ".join(context.args) 
    
    if(msg):
        context.bot.send_message(chat_id="215433687", text=msg)
                      
def help(update, context):
    
    cmds = ["/help", "/info <url>", "/add <url> <size>", "/add <url> <sku>", 
            "/list", "/remove <sku1> [<sku2> ...]", "/update",
            "/monitor [<period in seconds>]", "/stop_monitor", "/backup", 
            "/restore <url>", "/msg <message>"]
    
    helpstrings = ["display usage information",
"get overview of available variants of item corresponding\
to given zara url, including sku (stock keeping unit) numbers",
"add product with given url and specified size \
(XS-XXL or numeric depending on product) to the list of tracked items. On Zara, this \
only works, if the product only comes in a single variant (e.g. \
one color only).",
"Add product with given url and sku to the list of \
tracked items. Only needed for Zara products with multiple variants . \
Skus are of the form 54614904-250-2 or 54614904-250-38 \
where the last number determines size and the number in the middle \
determines product variant. They can be queried with /info",
"list currently tracked products",
"Remove product with given sku from tracking",
"Check for changes in tracked products (experimental!)",
"Start automatic monitoring at intervals of period  (experimental!, period 1800s recommended)",
"Stop automatic monitoring (experimental!)",
"Generate a .json file containing information about currently tracked items",
"Restore from a backup in the form of a .json file, which must be downloadable \
at the supplied url (use e.g. pastebin.com and raw urls for this)",
"Send a message to the developer (e.g. if you need access)\
 - include your telegram handle if you want a reply ;)"
]
    
    msg = "Below are listed the available commands, their arguments (which are written in \
between < and >) and optional arguments (in brackets). E.g. the command /info <url> would be executed as /info www.zara.com/someproductpage.html\n\n" + "\n\n".join([cmd + "  :  " + helpstr for cmd, helpstr in zip(cmds, helpstrings)])
    
    context.bot.send_message(chat_id=update.effective_chat.id, 
        text=msg)
    

def split_messages(msg, size=4096):
    return [msg[i : i+4096] for i in range(0, len(msg), 4096)]

def quiet_update(user_data):
    
    changeFlag = 0
    user_items = user_data.get('fashion_items')
    
    if(user_items != None):
        
        msg = ""
        sku_changed_items = {} # we use skus as keys in user_item_dict, so if
                               # those change we have to do housekeeping
        
        for key, item in user_items.items():
            
            n_changes = 0
            try:
                old_sku = item.dict['sku'] # zara tends to change skus, check for that
                [n_changes, old_values] = item.update()

                if(old_sku != item.dict['sku']): 
                    sku_changed_items[key] = item
                
            except SkuNotFoundException as ex:
                msg += escape_markdown(str(ex) + "\n", 2)
                
            if(n_changes > 0):
                msg1 = escape_markdown(",".join(old_values.keys()),2)
                msg2 = escape_markdown("changed in\n" + \
                        item.update_string(old_values)  + "\n",2)

                msg += "*" + msg1 + "* " + msg2

        # update items with changed skus
        for key, item in sku_changed_items.items():

            del user_items[key]
            user_items[item.dict['sku']] = item

                
        if(msg == ""):
            msg = "No changes detected"
        else:
            changeFlag = 1
            
    else:
        msg = "No items tracked, nothing to update."
        
    return [changeFlag, msg]
    
def manual_update(update, context):
    
    [changeFlag, msg] = quiet_update(context.user_data)

    logging.info("manual update called at " + str(datetime.now()))
    logging.info(msg + "\n\n")
        
    if(len(msg) > 4096): 
        messages = split_messages(msg, 4096)
        for m in messages:
            context.bot.send_message(chat_id=update.effective_chat.id, 
                text=m, parse_mode=ParseMode.MARKDOWN_V2)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, 
            text=msg, parse_mode=ParseMode.MARKDOWN_V2)

    # TODO remove 
    global user_context
    user_context = context
    
        
def start_regular_update(update, context):

    context_dict = {'id' : update.message.chat_id, 'user_data' : 
                   context.user_data}
    
    if(context.args and context.args[0].isnumeric()):
        interval = float(context.args[0])
    else:
        interval = 5*60 # seconds
    
    job_name = "monitor_" + str(context_dict['id'])
    
    if job_name not in [j.name for j in context.job_queue.jobs()]:

        context.job_queue.run_repeating(regular_update_callback,
            interval=interval, first=0, context=context_dict,
            name=job_name)
        
        msg = "Started monitoring with interval " + str(interval) + "s"
    
    else: 
        msg = "Already monitoring."

    context.bot.send_message(chat_id=update.effective_chat.id, 
        text=msg)

    
def stop_regular_update(update, context):

    job_name = "monitor_" + str(update.message.chat_id)
    job_list = context.job_queue.get_jobs_by_name(job_name)
    
    for job in job_list:
        job.schedule_removal()
    
    context.bot.send_message(chat_id=update.effective_chat.id, 
        text="Stopped monitoring")

        
def regular_update_callback(context):
                
    [changeFlag, msg] = quiet_update(
        context.job.context['user_data'])
    
    logging.info("update callback called at " + str(datetime.now()))
    logging.info(msg + "\n\n")
    
    if(changeFlag == 1):
        context.bot.send_message(chat_id=context.job.context['id'],
        text=msg, parse_mode=ParseMode.MARKDOWN_V2)
    
def backup_to_json(update, context):
        
    item_dict = context.user_data.get('fashion_items')
    json_dict = {sku : item.dict for sku, item in item_dict.items()}
    
    jsonStr = json.dumps(json_dict, indent=4, sort_keys = True)
    
    fd, path = tempfile.mkstemp()
    try:
        with os.fdopen(fd, 'w') as tmp:
            tmp.write(jsonStr)
            
        context.bot.send_document(chat_id=update.effective_chat.id,
            document=open(path,'rb'), filename="backup.json")

    finally:
        os.remove(path)

def send_logs(update, context):
    
    path = "/home/ubuntu/Notifier/notifier.log"
    context.bot.send_document(chat_id=update.effective_chat.id,
        document=open(path,'rb'), filename="notifier.log")
        
def restore_from_online_json(update, context):
    
    # TODO this won't work yet for large lists of tracked 
    # items due to telegrams msg size limits

    url = context.args[0]
    res = urllib.request.urlopen(url)
    data = res.read()
    jsonStr = data.decode('utf-8')
        
    json_dict = json.loads(jsonStr)
    item_dict = {}

    for sku, prod_dict in json_dict.items(): 
        url = prod_dict['url']  

        # TODO careful with order once adding zara home
        if('zalando' in url): 
            item_dict[sku] = ZalandoProduct(prod_dict) 
        elif('zara' in url): 
            item_dict[sku] = ZaraProduct(prod_dict) 
        elif('uniqlo' in url):
            item_dict[sku] = UniqloProduct(prod_dict) 
        elif('cosstores' in url):
            item_dict[sku]  = CosProduct(prod_dict) 
        elif('hm' in url):
            item_dict[sku]  = HmProduct(prod_dict) 
        
    context.user_data['fashion_items'] = item_dict
    
    context.bot.send_message(chat_id=update.effective_chat.id,
        text="Restored. I advise you check I did everything right.")

