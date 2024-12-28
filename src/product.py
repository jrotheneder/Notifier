import copy

class Product: 

    stock_msg_threshold = 10 # changes in stock below this value are signalled
    
    def __init__(self, productDict):

        self.dict = productDict.copy()

        # we print name before other attributes, so need to ensure it exists
        assert "name" in self.dict, "Product must have a name"
        
        
    def __str__(self):

        head_string = "name: " +  self.dict["name"] + "\n"
        tail_string = "\n".join([key + ": " + str(val) 
            for key, val in sorted(self.dict.items()) if key != "name"])
        
        return head_string + tail_string

    def update_string(self, old_dict):
        
        def distinguish(key):
            
            if(key in old_dict):
                return str(self.dict[key]) +\
                    " (previously " + str(old_dict[key]) + ")"
                
            else: 
                return str(self.dict[key])
            
        
        return "\n".join(sorted([key + ": " + distinguish(key) 
            for key in self.dict.keys()])) + "\n"       

    def productType(self):
        return "abstractProduct"

