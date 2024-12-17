import os,sys,json
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from src.zara_scraper import *
import requests


def zara_item_info_helper(url): 
    """
    Test for the helper function for info command. Given a zara url, it extracts
    summary information about the available variants of the item
    and sends this information to the user.
    """
    
    message = "" 

    try:
        [name, skus, skus_sans_sizes, size_dict, image_url_dict, color_dict] \
            = ZaraScraper.skuSummary(ZaraScraper.getProductList(url))
    
        msg = "Product: " + name + "\nUrl: " + url + "\nfound "\
                + str(len(skus_sans_sizes)) + " colors and "\
                + str(len(set(size_dict.values()))) + " sizes\n\n" \
                + "Listing SKUs along with some pictures: \n\n"

#         context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
        message += msg

        # send images so user can associate skus with colors
        for sku_sans_size in skus_sans_sizes: 

            img_url = image_url_dict[sku_sans_size]  
            color = color_dict[sku_sans_size]
            img_msg = "Color: " + color + ", " +\
                    "Image: [[[" + "1" + "]]](" + img_url + ")"
#           img_msg = "Color is " + color + "\nImage (may get color wrong): "\
#               +"[[[" + "1" + "]]](" + img_url + ")"

#             context.bot.send_message(chat_id=update.effective_chat.id,
#                     text=img_msg, parse_mode=ParseMode.MARKDOWN_V2)
            message += img_msg

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
#                     context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
                    message += "\n" + msg


    except SkuNotFoundException as ex:
        context.bot.send_message(chat_id=update.effective_chat.id, 
            text=str(ex))

    return message



