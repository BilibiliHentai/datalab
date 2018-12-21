#!/usr/bin/python
# -*- coding: UTF-8 -*-
from xml.dom.minidom import parse
import xml.dom.minidom
import xml.sax
# import xmltodict
import json
import copy
from time import sleep


class XmlDataHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.all_target = {}
        self.drugs = []
        self.drug = {
            'drugbank_id': '',
            'drug_name': '',
            'targets': [],
            'links_to_drugbank': '',  # url in link
            'link_to_CTD': '',  # cas-number
            'uniprot_ids': [],  # uniprot-id
            'indication': '',
            'categories': [],  # group
        }
        self.links_to_drugbank = []
        self.splited_link = ''
        self.targets = []
        self.target = {
            'target_id': '',
            'target_name': '',
        }
        self.outer_scope = ""
        self.has_drug_bank_id = False
        self.current_data = ""

    # 元素开始事件处理

    def startElement(self, tag, attributes):
        self.current_data = tag
        if tag == 'drug':
            self.outer_scope = tag
        elif tag == 'drugbank-id' and attributes.get('primary', False):
            self.current_data = 'drugbank_id'
        elif tag == 'link':
            self.outer_scope = tag
        elif tag == 'target':
            self.outer_scope = 'target'

    # 元素结束事件处理
    def endElement(self, tag):
        if tag == 'name':
            self.has_drug_bank_id = False
        self.current_data = ''
        if tag == 'links':
            self.outer_scope = ''
        if tag == 'transporters':
            self.drugs.append(self.drug)
            self.reset()
        if tag == 'target':
            self.targets.append(copy.deepcopy(self.target))
            self.all_target.update({self.target['target_id']: self.target['target_name']})
        if tag == 'targets':
            self.drug['targets'] = self.targets
            self.targets = []
        if tag == 'links':
            self.drug['links_to_drugbank'] = self.links_to_drugbank
        if tag == 'link':
            self.links_to_drugbank.append(self.splited_link)
            self.splited_link = ''
            self.outer_scope == ''

    # 内容事件处理
    def characters(self, content):
        if self.current_data == 'drugbank_id':
            self.drug['drugbank_id'] = content
        elif self.current_data == 'name':
            if self.outer_scope == 'target':
                self.target['target_name'] = content
            elif self.outer_scope == 'drug':
                self.drug['drug_name'] = content
        elif self.current_data == 'id':
            self.target['target_id'] = content
        elif self.current_data == 'cas-number':
            self.drug['link_to_CTD'] = content
        elif self.current_data == 'url':
            if self.outer_scope == 'link':
                self.splited_link += content
        elif self.current_data == 'indication':
            self.drug['indication'] = content
        elif self.current_data == 'uniprot-id':
            self.drug['uniprot_ids'].append(content)
        elif self.current_data == 'group':
            self.drug['categories'].append(content)

    def reset(self):
        self.drug = {
            'drugbank_id': '',
            'drug_name': '',
            'targets': [],
            'links_to_drugbank': '',  # url in link
            'link_to_CTD': '',  # cas-number
            'uniprot_ids': [],  # uniprot-id
            'indication': '',
            'categories': [],  # group
        }
        self.links_to_drugbank = []
        self.splited_link = ''
        self.targets = []
        self.target = {
            'target_id': '',
            'target_name': '',
        }
        self.outer_scope = ""
        self.has_drug_bank_id = False
        self.current_data = ""

    def endDocument(self):
        with open('extracted_data_from_xml.json', 'w')as f:
            f.write(json.dumps(self.drugs))
    def testprint(self, content):
        print(content)
        sleep(0.5)


class XmlReader:
    def __init__(self):
        self.data = ''  # list of dict

    @staticmethod
    def extract_data_from_xml(path):
        """
        parse data and dump it to a json file in the cwd.
        """
        # 创建一个 XMLReader
        parser = xml.sax.make_parser()
        # turn off namepsaces
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)

        # 重写 ContextHandler
        handler = XmlDataHandler()
        parser.setContentHandler(handler)

        parser.parse(path)

    def read(self):
        # print(os.path.dirname(os.path.abspath(__file__)))
        with open('extracted_data_from_xml.json', 'r') as f:
            self.data = json.load(f)

    def get_data(self):
        return self.data


if __name__ == "__main__":
    print('Enter xml file path:')
    input_ = input()
    if input_ != '':
        path = input_
    else:
        path = '/home/naroah/Documents/part-time job/full database.xml'
    print('Extracting...')
    XmlReader.extract_data_from_xml(path)
    print('Done')
