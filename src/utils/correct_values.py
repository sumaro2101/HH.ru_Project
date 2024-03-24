

class CorrectValues:
    
    @classmethod
    def correct_list(cls, items):
        correct_tuple = []
        
        for item in items.values():

            if type(item) != dict and type(item) != list:
                correct_tuple.append(item)
            elif type(item) == list:
                if len(item) != 0:
                    correct_tuple.extend(cls.correct_list(item[0]))
            else:
                correct_tuple.extend(cls.correct_list(item))
        
        return correct_tuple
    
    @classmethod
    def correct_name_companies(cls, list_companies):
        result = list_companies.split(',')
        result = [item.strip() for item in result]
        return result
    
    