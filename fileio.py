import json
class FileIO:
    def write(self, fileName : str, mod : str, data : list) -> None:
        with open(f"{fileName}.{mod}", 'w') as file:
            json.dump(data, file)
    
    def read(self, fileName : str, mod : str) -> list:
        with open(f"{fileName}.{mod}", 'r') as file:
            return json.load(file)