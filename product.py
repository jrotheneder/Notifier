import copy

class Product: 

    stock_msg_threshold = 10 # changes in stock below this value are signalled
    
    def __init__(self, productDict):

        self.dict = productDict.copy()
        
        
    def __str__(self):
        
        return "\n".join([key + ": " + str(val) 
            for key, val in sorted(self.dict.items())])        

    def update_string(self, old_dict):
        """
        
        """
        
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
