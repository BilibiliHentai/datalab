#!/usr/bin/python
# -*- coding: UTF-8 -*-
from xml.dom.minidom import parse
import xml.dom.minidom
import xml.sax
# import xmltodict
import json
from time import sleep


class dataHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.all_target = {}
        self.drugs = []
        self.drug = {
            'drugbank_id': '',
            'drug_name': '',
            'targets': '',
            'links_to_drugbank': '', # url in link
            'link_to_CTD': '', # cas-number
            'uniprot': '', # uniprot-id
            'indication': '',
            'categories': [], # group
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
            print(self.drug)
            self.reset()
        if tag == 'target':
            self.targets.append(self.target)
            self.all_target.update({self.target['target_id']: self.target['target_name']})
        if tag == 'targets':
            self.drug['targets'] = self.targets
            self.targets = []
        if tag == 'links':
            self.drug['links_to_drugbank'] = self.links_to_drugbank
        if tag == 'link':
            self.links_to_drugbank.append(self.splited_link)
            # self.testprint(self.splited_link)
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
            self.drug['uniprot'] = content
        elif self.current_data == 'group':
            self.drug['categories'].append(content)

    def reset(self):
        self.drug = {
            'drugbank_id': '',
            'drug_name': '',
            'targets': '',
            'links_to_drugbank': '', # url in link
            'link_to_CTD': '', # cas-number
            'uniprot': '', # uniprot-id
            'indication': '',
            'categories': [], # group
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

    # def endDocument(self):
    #     with open('targets.json', 'w')as f:
    #         f.write(json.dumps(self.all_target))

    def testprint(self, content):
        print(content)
        sleep(0.5)

if (__name__ == "__main__"):
    path = "/home/naroah/Documents/part-time job/full database.xml"
    # 创建一个 XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # 重写 ContextHandler
    Handler = dataHandler()
    parser.setContentHandler(Handler)

    parser.parse(path)


