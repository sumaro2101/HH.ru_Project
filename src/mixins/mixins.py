from pydantic import BaseModel, ConfigDict
from typing import Union, Dict, List

from src.api_exchange.exchange import ApiChange
from src.utils.enum_town import EnumTown


class MixinConvert(BaseModel, extra='allow'):
    """Миксин для внедрения Exchange в основную программу
    """   
     
    convert_to_RUB: bool = False
    
    def _make_list_for_convert(self, list_: List[Dict]):
        """Метод который проходится по списку объектов и выводит иностранные валюты

        Args:
            list_ (List[Dict]): Список с объектами
        """  
              
        currencies = []
        
        [currencies.append(item['salary']['currency']) 
         for item in list_
         if item['salary']['currency'] != 'RUR' and item['salary']['currency'] not in currencies]
        
        return currencies
    
    def get_rate_currency(self, list_: List[str]) -> Dict:
        """API которое получает список валют которые войдут в запрос

        Args:
            list_ (List[str]): Список валют

        Returns:
            Dict: Возращает результат запроса с индексами указанных валют
        """ 
               
        rates = ApiChange(symbols=list_)
        
        if rates.ex_change.get('rates'):
            return rates.ex_change['rates']

    def _convert_valute(self, class_, list_: List[Dict]) -> List[Dict]:
        """Метод который проходится по списку с объетами и меняет 
        значение денежного эквивалетна у тех у котого иностранная валюта

        Args:
            list_ (List[Dict]): Список до конвертации

        Returns:
            List[Dict]: Список после конвертации
        """    
            
        converted = list_
        rate_dict = self.get_rate_currency(self._make_list_for_convert(list_))
        if rate_dict:
            for item in converted:
                if item['salary']['currency'] != 'RUR':
                    valute_item = item['salary']['from']
                    valute_rate = rate_dict[item['salary']['currency']]
                    
                    item['salary']['from'] = int(valute_item / valute_rate)
                    if item['salary']['to']:
                        valute_item = item['salary']['to']
                        item['salary']['to'] = int(valute_item / valute_rate)
                    
        class_._response = converted


class MixinSort(BaseModel, extra='allow'):
    """Миксин сортировки объектов по определенному значению
    """    
    
    def __init_subclass__(cls, **kwargs: ConfigDict):
        return super().__init_subclass__(**kwargs)
        
    def _sort_json_response(self, class_, dict_: List[Dict]) -> List[Dict]:
        """Сортировка JSON файла по зарплате

        Returns:
            Dict: Возращает отсортированный словарь
        """  
              
        sorted_json = sorted(dict_, key=lambda x: x['salary']['from'], reverse=True)
        
        class_._response = sorted_json
    

class MixinTown(BaseModel, extra='allow'):
    """Миксин итеграции функциональности поиска по определенному городу
    """    
    
    def __init_subclass__(cls, **kwargs: ConfigDict):
        return super().__init_subclass__(**kwargs)
    town: Union[str, None] = None
    
    def make_id_of_town(self, town: str) -> int:
        """Метод получает имя города и возразает ID

        Args:
            town (str): имя города

        Returns:
            int: ID города
        """  
           
        if town is not None:
            return EnumTown[town].value