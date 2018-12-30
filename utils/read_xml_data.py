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
        self.genes = {}
        self.gene = {
            'id': '',
            'name': '',
            'protein_name': '',
            'categories': [],
            'link_to_uniprot': '',
            'go_term': '',
            'associate_compound_number': 0,
            'compounds': [],
        }

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
        self.current_data = ''
        if tag == 'links':
            self.outer_scope = ''
        if tag == 'transporters':
            self.drugs.append(self.drug)
            self.reset_drug()
        if tag == 'target':
            self.targets.append(copy.deepcopy(self.target))
            self.gene['compounds'].append(self.drug)
            if self.genes.get(self.gene['id'], None) is not None:
                compounds = self.genes.get(self.gene['id'])['compounds']
                self.gene['compounds'].extend(compounds)
            self.gene['associate_compound_number'] = len(self.gene['compounds'])
            self.gene['link_to_uniprot'] = (
                'https://www.uniprot.org/uniprot/?query=gene%3A' +
                self.gene['name'] + '&sort=score'
            )
            self.genes.update({self.gene['id']: copy.deepcopy(self.gene)})
            self.reset_gene()
        if tag == 'targets':
            self.drug['targets'] = self.targets
            self.targets = []
        if tag == 'links':
            self.drug['links_to_drugbank'] = self.links_to_drugbank
        if tag == 'link':
            self.links_to_drugbank.append(self.splited_link)
            self.splited_link = ''

    # 内容事件处理
    def characters(self, content):
        if self.current_data == 'drugbank_id':
            self.drug['drugbank_id'] = content
        elif self.current_data == 'name':
            if self.outer_scope == 'target':
                self.target['target_name'] = content
                self.gene['protein_name'] = content
            elif self.outer_scope == 'drug':
                self.drug['drug_name'] = content
        elif self.current_data == 'gene-name':
            self.gene['name'] = content
        elif self.current_data == 'id':
            self.target['target_id'] = content
            self.gene['id'] = content
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

    def reset_drug(self):
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
        self.current_data = ""

    def reset_gene(self):
        self.gene = {
            'id': '',
            'name': '',
            'protein_name': '',
            'compounds': [],
            'associate_compound_number': 0,
            'categories': [],
            'link_to_uniprot': '',
            'go_term': '',
        }

    def endDocument(self):
        with open('extracted_drugs_from_xml.json', 'w') as f:
            f.write(json.dumps(self.drugs))
            print('done extract drug')
        with open('extracted_genes_from_xml.json', 'w') as f:
            genes = []
            for k, v in self.genes.items():
                genes.append(v)
            f.write(json.dumps(genes))
            print('done extract gene')

    def testprint(self, content):
        print(content)
        sleep(0.5)


class XmlReader:
    def __init__(self):
        self._drugs = []  # list of dict
        self._genes = {}

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
        with open('extracted_drugs_from_xml.json', 'r') as f:
            self._drugs = json.load(f)
        with open('extracted_genes_from_xml.json', 'r') as f:
            self._genes = json.load(f)

    def get_drugs(self):
        """return a list of dict"""
        return self._drugs

    def get_genes(self):
        """return a dict"""
        return self._genes


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
