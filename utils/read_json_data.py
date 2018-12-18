import json

PATH = '/home/naroah/Documents/part-time job/score_distribution.json'
class JsonReader():
    def __init__(self, path=PATH):
        self.path = path

    def read(self) -> json:
        with open(self.path, 'r') as json_file:
            self.data = json.load(json_file)

    def get_all_score(self):
        scores = []
        for i in self.data:
            scores.append(i['predict_score'])
        return scores

    def get_score_sorted_data(self, quantity=20):
        rows = []
        data = sorted(self.data, key=lambda x:x['predict_score'], reverse=True)
        data = data[:quantity]
        for i in data:
            row = {}
            row.update({'gene_id': i['target_id']})
            row.update({'gene_name': i['supporting_entry'][0]['target']})
            row.update({'compound_id': i['drug_id']})
            row.update({'compound_name': i['supporting_entry'][0]['drug']})
            row.update({'score': i['predict_score']})
            row.update({'supporting_entries_number': len(i['supporting_entry'])})
            rows.append(row)
        # print(rows)
        return rows

    def get_total_number(self) -> dict:
        data = self.data
        targetid= set()
        drugid = set()
        pmid = set()
        total_numbers = {}

        for i in data:
            targetid.add(i['target_id'])
            drugid.add(i['drug_id'])
            for j in i['supporting_entry']:
                pmid.add(j['pmid'])

        print('total gene number is: {}'.format(len(targetid)))
        print('total compound number is: {}'.format(len(drugid)))
        print('total related publication number is: {}'.format(len(pmid)))
        total_numbers.update({'total_gene_number': len(targetid)})
        total_numbers.update({'total_compound_number': len(drugid)})
        total_numbers.update({'total_related_publication': len(pmid)})
        return total_numbers


if __name__ == '__main__':
    reader = JsonReader()
    reader.read()
    reader.get_total_number()
