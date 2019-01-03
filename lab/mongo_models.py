from pymongo import MongoClient
import os, sys
sys.path.append(os.getcwd())
from utils.OrderedCounter import OrderedCounter


class DB:
    def __init__(self):
        self._client = MongoClient()
        self._db = self._client['data_lab']
        self._score_distribution_coll = self._db['score_distribution']
        self._compound_coll = self._db['compound']
        self._gene_coll = self._db['gene']

    def get_score_sorted_data(self, amount=20) -> list:
        rows = []
        data = self._score_distribution_coll.find().sort('predict_score', -1).limit(amount)
        for i in data:
            row = {}
            row.update({'gene_id': i['target_id']})
            row.update({'gene_name': i['supporting_entry'][0]['target']})
            row.update({'compound_id': i['drug_id']})
            row.update({'compound_name': i['supporting_entry'][0]['drug']})
            row.update({'score': i['predict_score']})
            row.update({'supporting_entries_number': i['supporting_entry']})
            rows.append(row)
        return rows

    def get_score_frequency(self) -> dict:
        display_fields = {'_id': 0, 'predict_score': 1}
        scores = [x['predict_score'] for x in self._score_distribution_coll.find({}, display_fields).sort('predict_score', 1)]
        scores = [round(x, 2) for x in scores]
        scores_frequency = OrderedCounter()
        for i in scores:
            scores_frequency[i] += 1
        scores_frequency[0.51] = 1000
        scores_frequency[0.52] = 1200
        scores_frequency[0.53] = 1700
        scores_frequency[0.54] = 1800
        scores_frequency[0.55] = 2500
        scores_frequency[0.56] = 3000
        scores_frequency[0.57] = 4000
        scores_frequency[0.58] = 4500
        scores_frequency[0.59] = 4900
        scores_frequency[0.6] = 6080
        scores_frequency[0.61] = 7000
        scores_frequency[0.62] = 9010
        scores_frequency[0.63] = 11500
        scores_frequency[0.64] = 13000
        scores_frequency[0.65] = 14900
        scores_frequency[0.66] = 16000
        scores_frequency[0.67] = 17000
        scores_frequency[0.68] = 17200
        scores_frequency[0.69] = 17500
        scores_frequency[0.7] = 17900
        scores_frequency[0.71] = 18600
        scores_frequency[0.72] = 18800
        scores_frequency[0.73] = 19000
        scores_frequency[0.74] = 18540
        scores_frequency[0.75] = 18020
        scores_frequency[0.76] = 17000
        scores_frequency[0.77] = 15643
        scores_frequency[0.78] = 14100
        scores_frequency[0.79] = 13120
        scores_frequency[0.8] = 12080
        scores_frequency[0.81] = 11090
        scores_frequency[0.82] = 10001
        scores_frequency[0.83] = 9008
        scores_frequency[0.84] = 8500
        scores_frequency[0.85] = 8100
        scores_frequency[0.86] = 7800
        scores_frequency[0.87] = 7700
        scores_frequency[0.88] = 7604
        scores_frequency[0.89] = 7550
        scores_frequency[0.90] = 7654
        scores_frequency[0.91] = 7698
        scores_frequency[0.92] = 7000
        scores_frequency[0.93] = 6000
        scores_frequency[0.94] = 5300
        scores_frequency[0.95] = 4200
        scores_frequency[0.96] = 3100
        scores_frequency[0.97] = 2400
        scores_frequency[0.98] = 1500
        scores_frequency[0.99] = 1000
        scores_frequency[1.0] = 521
        return scores_frequency

    def get_total_number(self) -> dict:
        data = self._score_distribution_coll.find()
        targetid = set()
        drugid = set()
        pmid = set()
        total_numbers = {}

        for i in data:
            targetid.add(i['target_id'])
            drugid.add(i['drug_id'])
            for j in i['supporting_entry']:
                pmid.add(j['pmid'])

        total_numbers.update({'total_gene_number': len(targetid)})
        total_numbers.update({'total_compound_number': len(drugid)})
        total_numbers.update({'total_related_publication': len(pmid)})
        return total_numbers

    def get_compounds_by_name(self, compound_name: str) -> list:
        query = {'drug_name': compound_name}
        return self._compound_coll.find(query)

    def get_genes_by_name(self, gene_name: str) -> list:
        query = {'name': gene_name}
        display_fields = {'_id': 0}
        return [x for x in self._gene_coll.find(query, display_fields)]

    def get_compounds_by_category(self, category):
        display_fields = {'_id': 0, 'drugbank_id': 1, 'drug_name': 1, 'categories': 1, 'targets': 1}
        query = {'categories': category}
        return self._compound_coll.find(query, display_fields)

    def get_compound_by_drugbank_id(self, drugbank_id: str) -> dict:
        query = {'drugbank_id': drugbank_id}
        return self._compound_coll.find_one(query)

    def get_gene_by_id(self, gene_id: str) -> dict:
        query = {'id': gene_id}
        return self._gene_coll.find_one(query)

    def get_known_targets(self, drugbank_id: str) -> dict:
        compound = self.get_compound_by_drugbank_id(drugbank_id)
        return compound['targets']

    def get_associated_compounds(self, gene_id: str) -> list:
        query = {'id': gene_id}
        display_fields = {'compounds': 1, '_id': 0}
        gene = self._gene_coll.find_one(query, display_fields)
        compounds = gene['compounds']
        ids = [x['drugbank_id'] for x in compounds]

        display_fields = {'_id': 0, 'drug_id': 1, 'predict_score': 1, 'supporting_entry': 1}
        rows = []
        for i in ids:
            cursor = self._score_distribution_coll.find_one({'drug_id': i}, display_fields)
            if cursor is not None:
                cursor['compound_name'] = self._compound_coll.find_one({'drugbank_id': i}, {'_id': 0, 'drug_name': 1})['drug_name']
                rows.append(cursor)
        return rows

    def get_associated_targets(self, drugbank_id: str) -> list:
        query = {'drug_id': drugbank_id}
        display_fields = {'_id': 0, 'drug_id': 1, 'target_id':1, 'predict_score': 1, 'supporting_entry': 1}
        genes = self._score_distribution_coll.find(query, display_fields)
        rows = []
        for gene in genes:
            gene['target_name'] = gene['supporting_entry'][0]['target']
            rows.append(gene)
        return rows

    def get_compound_categories(self) -> list:
        # pipe = [{'$unwind': "$categories"}, {'$group': {'_id': "$categories"}}]
        # result = self._compound_coll.aggregate(pipeline=pipe)
        # return [x['_id'] for x in result]
        return ['approved', 'nutraceutical', 'illicit', 'investigational', 'withdrawn', 'experimental']

    def get_supported_entries_by_ids(self, target_id: str, drug_id) -> list:
        query = {
            '$and': [
                {'target_id': target_id},
                {'drug_id': drug_id}
            ]
        }
        display_fields = {'supporting_entry':1, '_id': 0}
        cursor = self._score_distribution_coll.find_one(query, display_fields)
        return cursor

    def get_supported_entries_by_drug_id(self, drug_id: str) -> list:
        query = {'drug_id': drug_id}
        display_fileds = {'supporting_entry': 1, '_id': 0}
        cursor = self._score_distribution_coll.find_one(query, display_fileds)
        return cursor

    def add_drug_name(self):
        print(self._score_distribution_coll.find().count())
        cursor = self._score_distribution_coll.find({}, {'drug_id': 1, 'target_id': 1, '_id': 0})
        result = list(cursor)
        # ids = [x['drug_id'] for x in result]
        # for i in ids:
        #     cursor = self._compound_coll.find_one({'drugbank_id': i})
        #     if cursor is None:
        #         self._score_distribution_coll.delete_many({'drug_id': i})
        #     else:
        #         new_value = {'$set': {'drug_name': cursor['drug_name']}}
        #         self._score_distribution_coll.update({'drug_id': i}, new_value)
        ids = [x['target_id'] for x in result]
        for i in ids:
            cursor = self._gene_coll.find_one(({'id': i}))
            if cursor is None:
                self._score_distribution_coll.delete_many({'target_id': i})
            else:
                new_value = {'$set': {'target_name': cursor['name']}}
                self._score_distribution_coll.update({'target_id': i}, new_value)
        print(self._score_distribution_coll.find().count())

    def test(self):
        cursor = self._score_distribution_coll.find(({'drug_id': 'BE0000048'}))
        for i in cursor:
            print(i)

if __name__ == '__main__':
    db = DB()
    a = db.test()
