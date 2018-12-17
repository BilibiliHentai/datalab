# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
from typing import Callable, List
from pymongo import MongoClient


class Database(object):
    def __init__(self, db_name, username=None, password=None, host="166.111.141.147", port=27017):
        self.client = self.connect(host, port)
        self.db = self.client.get_database(db_name)
        self.authentic(username, password)


    def connect(self, host, port):
        try:
            client = MongoClient(host=host, port=port, connect=False)
            print('----Connect: success')
            return client
        except:
            print('----Connect: error')
            return None


    def authentic(self, username, password):
        try:
            self.db.authenticate(username, password)
            print('----Authentic: success')
        except:
            print('----Authentic: error')


    def close(self):
        self.client.close()


    def __str__(self):
        s = ''
        s += 'DataBase: {0}\n'.format(self.db.name)
        for table_name in self.db.list_collection_names():
            table = self.db.get_collection(table_name)
            s += '{0}: {1} records\n'.format(table.name, table.count())
        return s

    # condition list
    # ����
    # { < key >: < value >}    db.col.find({"id": "DB00001"})

    # С��
    # { < key >:{$lt: < value >}}    db.col.find({"likes": {$lt:50}})

    # С�ڻ����
    # { < key >:{$lte: < value >}}    db.col.find({"likes": {$lte:50}})

    # ����
    # { < key >:{$gt: < value >}}    db.col.find({"likes": {$gt:50}})

    # ���ڻ����
    # { < key >:{$gte: < value >}}    db.col.find({"likes": {$gte:50}})

    # ������
    # { < key >:{$ne: < value >}}    db.col.find({"likes": {$ne:50}})

    def _find_one(self, table_name, condition=None):
        table = self.db.get_collection(table_name)
        return table.find_one(condition)

    def _find(self, table_name, condition=None):
        table = self.db.get_collection(table_name)
        return table.find(condition)

    def query_gene(self, gene_name):
        gene_name = gene_name.lower()
        compound_dict = {}

        gene_item = self._find_one('GeneMap', {'name': gene_name})
        try:
            gene_id = gene_item['id']
        except:
            print("No record")
            return []

        pairs = self._find('CompoundGene', {'gene': gene_id})

        for pair in pairs:
            compound_id = pair['compound']
            sent = ' '.join(pair['sent'])
            pmid = pair['pmid']
            score = pair['score']

            if compound_id in compound_dict:
                compound_dict[compound_id]['ref'].append((pmid, sent))
                compound_dict[compound_id]['cite_num'] += 1
                compound_dict[compound_id]['avg_score'] += float(score)
            else:
                compound_dict[compound_id] = {'name': '', 'avg_score': float(score), 'cite_num': 1, 'ref': [(pmid, sent)]}

        for compound_id in compound_dict.keys():
            compound_item = self._find_one('dictionary', {'id': compound_id})
            compound_name = compound_item['name'][0]

            compound_dict[compound_id]['name'] = compound_name
            compound_dict[compound_id]['avg_score'] /= compound_dict[compound_id]['cite_num']
        compound_dict_values = compound_dict.values()
        data = list(compound_dict_values)
        return data

    def query_compound(self, compound_name):
        compound_name = compound_name.lower()
        gene_dict = {}

        compound_item = self._find_one('CompoundMap', {'name': compound_name})
        try:
            compound_id = compound_item['id']
        except:
            print("No record")
            return []

        pairs = self._find('CompoundGene', {'compound': compound_id})

        for pair in pairs:
            gene_id = pair['gene']
            sent = ' '.join(pair['sent'])
            pmid = pair['pmid']
            score = pair['score']

            if gene_id in gene_dict:
                gene_dict[gene_id]['ref'].append((pmid, sent))
                gene_dict[gene_id]['cite_num'] += 1
                gene_dict[gene_id]['avg_score'] += float(score)
            else:
                gene_dict[gene_id] = {'name': '', 'avg_score': float(score), 'cite_num': 1, 'ref': [(pmid, sent)]}

        for gene_id in gene_dict.keys():
            gene_item = self._find_one('dictionary', {'id': gene_id})
            gene_name = gene_item['name'][0]

            gene_dict[gene_id]['name'] = gene_name
            gene_dict[gene_id]['avg_score'] /= gene_dict[gene_id]['cite_num']
        gene_dict_values = gene_dict.values()
        data = list(gene_dict_values)
        return data

    def get_gene(self, sum:int, sort:Callable[[List], str]) -> list:
        data = []
        gene_collection = self.db['GeneMap']
        compound_dict = {}
        for gene_item in gene_collection.find():

            try:
                gene_id = gene_item['id']
            except:
                print("No record")
                return []

            pairs = self._find('CompoundGene', {'gene': gene_id})

            for pair in pairs:
                compound_id = pair['compound']
                sent = ' '.join(pair['sent'])
                pmid = pair['pmid']
                score = pair['score']

                if compound_id in compound_dict:
                    compound_dict[compound_id]['ref'].append((pmid, sent))
                    compound_dict[compound_id]['cite_num'] += 1
                    compound_dict[compound_id]['avg_score'] += float(score)
                else:
                    compound_dict[compound_id] = {'name': '', 'avg_score': float(score), 'cite_num': 1, 'ref': [(pmid, sent)]}

            for compound_id in compound_dict.keys():
                compound_item = self._find_one('dictionary', {'id': compound_id})
                compound_name = compound_item['name'][0]

                compound_dict[compound_id]['name'] = compound_name
                compound_dict[compound_id]['avg_score'] /= compound_dict[compound_id]['cite_num']
            compound_dict_values = compound_dict.values()
            # TODO
            data.append(list(compound_dict_values))
        return data

    def get_compound(self):
        return self.db['CompoundMap']

    def get_gene_sum(self):
        return len(self.db['GeneMap'])

    def get_compound_sum(self):
        return len(self.db['CompoundMap'])


database = Database('PMC', username='PMC', password='PMC123', host="166.111.141.147", port=27017)


if __name__ == '__main__':
    print('\n---------Interacted Genes for compound *rivaroxaban*---------\n')
    database = Database('PMC', username='PMC', password='PMC123', host="166.111.141.147", port=27017)
    genes = database.query_compound('rivaroxaban')
    genes = sorted(genes, key=lambda x: x['cite_num'], reverse=True)
    # gene['name']: ��������
    # gene['avg_score]: ƽ������
    # gene['cite_num]: �ο���Ŀ
    # gene['ref]: [(pmid,sent),(pmid,sent)...]
    for gene in genes:
        print(gene['name'], gene['avg_score'], gene['cite_num'])

    print('\n---------Interacted Compounds for gene *prothrombinase*---------\n')
    compounds = database.query_gene('prothrombinase')
    compounds = sorted(compounds, key=lambda x: x['cite_num'], reverse=True)
    # compound['name']: С��������
    # compound['avg_score]: ƽ������
    # compound['cite_num]: �ο���Ŀ
    # compound['ref]: [(pmid,sent),(pmid,sent)...]
    for compound in compounds:
        print(compound['name'], compound['avg_score'], compound['cite_num'])

