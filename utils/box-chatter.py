##
# class that embed chromadb

import chromadb 


class BoxChroma():
    def _init(self):
        self.client = chromadb.HttpClient(host='localhost', port=8000)