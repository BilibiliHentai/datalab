import pymongo
import time


# client = pymongo.MongoClient('mongodb://localhost:27017/')
# dtitool_db = client['dtitool']
# coll = dtitool_db['protein_vocabulary']


class DB:
    def __init__(self):
        self._client = pymongo.MongoClient('mongodb://localhost:27017/')
        self._db = self._client['dtitool']
        self._protein_vocabulary = self._db['protein_vocabulary']
        self._drug_vocabulary = self._db['drug_vocabulary']
        self._dtinet_score = self._db['DTInet_score']
        self._neodti_score = self._db['NeoDTI_score']
        self._dtinet_score_entries = self._db['DTInet_score_entries']
        self._neodti_score_entries = self._db['NeoDTI_score_entries']

    def _get_protein_name(self, protein_id):
        query = {"protein_id": protein_id}
        docs = self._protein_vocabulary.find(query)
        return docs[0]['protein_name']

    def _get_protein_smiles(self, protein_id):
        query = {"protein_id": protein_id}
        docs = self._protein_vocabulary.find(query)
        return docs[0]['smiles']

    def _get_score_entries_by_line(self, line, which):
        pipeline = [
            {"$match": {"line": line}}, # TODO
            {"$unwind": "$score_entries"},
            {"$sort": {"score_entries.score": -1}},
            {"$limit": 20}
        ]
        if which == 'DTInet':
            docs = self._dtinet_score.aggregate(pipeline)
            score_name = 'DTInet_score'
            ranking_name = 'DTInet_ranking'
        elif which == 'NeoDTI':
            docs = self._neodti_score.aggregate(pipeline)
            score_name = 'NeoDTI_score'
            ranking_name = 'NeoDTI_ranking'

        score_entries = []
        ranking = 1
        for doc in docs:
            score = doc['score_entries'].pop("score", None)
            doc['score_entries'][score_name] = score

            protein_name = self._get_protein_name(doc['score_entries']['protein_id'])
            smiles = self._get_protein_smiles(doc['score_entries']['protein_id'])
            doc['score_entries'][ranking_name] = ranking
            doc['score_entries']['protein_name'] = protein_name
            doc['score_entries']['smiles'] = smiles
            score_entries.append(doc['score_entries'])
            ranking += 1

        return score_entries

    def _get_one_drug(self, attribute):
        query = {
            '$or': [
                {'drug_id': attribute},
                {'drug_name': attribute}
            ]
        }
        drug = self._drug_vocabulary.find_one(query)
        return drug
    
    def _get_one_protein(self, attribute):
        query = {
            '$or': [
                {'protein_id': attribute},
                {'protein_name': attribute},
            ]
        }
        protein = self._protein_vocabulary.find_one(query)
        return protein

    def get_scores_by_protein_id(self, protein_id, top_x=10):
        pipeline = [
            {'$match': {'protein_id': protein_id}},
            {"$sort": {"score_entries.score": -1}},
            {"$limit": top_x},
        ]
        query = {"protein_id": protein_id}
        dtinet_scores = self._dtinet_score_entries.find().sort('score', -1).limit(top_x)
        # dtinet_scores = self._neodti_score.aggregate(pipeline)
        print(dtinet_scores)
        for i in dtinet_scores:
            print(i)
        

    def get_score_entries(self, attribute, which):
        """
        argument which should be "DTInet" or "NeoDTI"
        """
        drug = self._get_one_drug(attribute)
        if drug is None:
            return 
        line = drug['line']
        return self._get_score_entries_by_line(line, which)
        
    def get_score_entries_by_drug_condition(self, which, attribute, upper_limit, lower_limit):
        drug = self._get_one_drug(attribute)
        line = drug['line']
        pipeline = [
            {"$unwind": "$score_entries"},
            {
                '$match': {
                    'line': line,
                    'score_entries.score': {'$lt': upper_limit, '$gt': lower_limit}
                }
            },
            {"$sort": {"score_entries.score": -1}}
        ]
        if which == 'DTInet':
            docs = self._dtinet_score.aggregate(pipeline)
            score_name = 'DTInet_score'
        elif which == 'NeoDTI':
            docs = self._dtinet_score.aggregate(pipeline)
            score_name = 'NeoDTI_score'
            
        score_entries = []
        ranking = 1
        for doc in docs:
            score = doc['score_entries'].pop("score", None)
            doc['score_entries'][score_name] = score

            protein_name = self._get_protein_name(doc['score_entries']['protein_id'])
            doc['score_entries']['protein_name'] = protein_name
            score_entries.append(doc['score_entries'])
            ranking += 1

        return score_entries


    def get_score_entries_by_drug_ranking(self, which, attribute, upper_ranking, lower_ranking):
        drug = self._get_one_drug(attribute)
        line = drug['line']
        pipeline = [
            {"$unwind": "$score_entries"},
            {
                '$match': {
                    'line': line,
                }
            },
            {"$sort": {"score_entries.score": -1}}
        ]

        if which == 'DTInet':
            docs = self._dtinet_score.aggregate(pipeline)
            ranking_name = 'DTInet_ranking'
        elif which == 'NeoDTI':
            docs = self._neodti_score.aggregate(pipeline)
            ranking_name = 'NeoDTI_ranking'
            
        score_entries = []
        ranking = 1
        for doc in docs:
            if lower_ranking <= ranking <= upper_ranking:
                doc['score_entries'][ranking_name] = ranking
                protein_name = self._get_protein_name(doc['score_entries']['protein_id'])
                doc['score_entries']['protein_name'] = protein_name
                score_entries.append(doc['score_entries'])
            ranking += 1

        return score_entries       

    def get_score_entries_by_protein_condition(self, which, attribute, upper_limit, lower_limit):
        protein = self._get_one_protein(attribute)
        result =[]
        # drug = {
        #     'drug_id': '',
        #     'drug_name': '',
        #     'DTInet_score': 0,
        #     'DTInet_ranking': 0,
        #     'NeoDTI_score': 0,
        #     'NeoDTI_ranking': 0,
        #     'label': 0,
        #     'sequence': ''
        # }

        pipeline = [
            {"$unwind": "$score_entries"},
            {"$sort": {"score_entries.score": -1}},
            {"$match": {
                    "score_entries.protein_id": protein['protein_id'],
                    "score_entries.score":  {'$lt': upper_limit, '$gt': lower_limit}
                }
            },
        ]

        if which == 'DTInet':
            docs = self._dtinet_score.aggregate(pipeline)
            score_name = "DTInet_score"
            ranking_name = "DTInet_ranking"
        elif which == 'NeoDTI':
            docs = self._dtinet_score.aggregate(pipeline)
            score_name = "NeoDTI_score"
            ranking_name = "NeoDTI_ranking"
        
        ranking = 1
        for doc in docs:
            drug = self._drug_vocabulary.find_one({"line": doc["line"]})
            try:
                drug_name = drug["drug_name"]
            except KeyError as e:
                drug_name = ""
            
            result.append({
                'drug_id': drug["drug_id"],
                "drug_name": drug_name,
                score_name: doc["score_entries"]['score'],
                ranking_name: ranking,
                "label": doc["score_entries"]["label"],
                "sequence": drug["unknown"]
            })
            ranking += 1
        return result

    def get_score_entries_by_protein_ranking(self, which, attribute, upper_ranking, lower_ranking):
        protein = self._get_one_protein(attribute)
        print(protein)
        result = []
        pipeline = [
            {"$unwind": "$score_entries"},
            {
                '$match': {
                    'score_entries.protein_id': protein["protein_id"],
                }
            },
            {"$sort": {"score_entries.score": -1}}
        ]

        if which == 'DTInet':
            docs = self._dtinet_score.aggregate(pipeline)
            score_name = "DTInet_score"
            ranking_name = 'DTInet_ranking'
        elif which == 'NeoDTI':
            score_name = "NeoDTI_score"
            docs = self._neodti_score.aggregate(pipeline)
            ranking_name = 'NeoDTI_ranking'

        ranking = 1
        for doc in docs:
            print(doc)
            if lower_ranking <=  ranking <= upper_ranking:
                drug = self._drug_vocabulary.find_one({"line": doc["line"]})
                try:
                    drug_name = drug["drug_name"]
                except KeyError as e:
                    drug_name = ""
                
                result.append({
                    'drug_id': drug["drug_id"],
                    "drug_name": drug_name,
                    score_name: doc["score_entries"]['score'],
                    ranking_name: ranking,
                    "label": doc["score_entries"]["label"],
                    "sequence": drug["unknown"]
                })
            ranking += 1
        return result
        

    def _get_score_entries_by_line(self, line, which):
        pipeline = [
            {"$match": {"line": line}}, # TODO
            {"$unwind": "$score_entries"},
            {"$sort": {"score_entries.score": -1}},
            {"$limit": 20}
        ]
        if which == 'DTInet':
            docs = self._dtinet_score.aggregate(pipeline)
            score_name = 'DTInet_score'
            ranking_name = 'DTInet_ranking'
        elif which == 'NeoDTI':
            docs = self._neodti_score.aggregate(pipeline)
            score_name = 'NeoDTI_score'
            ranking_name = 'NeoDTI_ranking'

        score_entries = []
        ranking = 1
        for doc in docs:
            score = doc['score_entries'].pop("score", None)
            doc['score_entries'][score_name] = score

            protein_name = self._get_protein_name(doc['score_entries']['protein_id'])
            smiles = self._get_protein_smiles(doc['score_entries']['protein_id'])
            doc['score_entries'][ranking_name] = ranking
            doc['score_entries']['protein_name'] = protein_name
            doc['score_entries']['smiles'] = smiles
            score_entries.append(doc['score_entries'])
            ranking += 1

        return score_entries
    
    def get_drug_entries(self, attribute):
        result =[]
        drug = {
            'drug_id': '',
            'drug_name': '',
            'DTInet_score': 0,
            'DTInet_ranking': 0,
            'NeoDTI_score': 0,
            'NeoDTI_ranking': 0,
            'label': 0,
            'Smiles': ''
        }
        protein = self._get_one_protein(attribute)
        query = {
            "score_entries": {
                "$elemMatch": {"protein_id": protein['protein_id']}
            }
        }

        pipeline = [
            {"$unwind": "$score_entries"},
            {"$sort": {"score_entries.score": -1}},
            {"$match": {"score_entries.protein_id": protein['protein_id']}},
            # {"$limit": 20}
        ]

        dtinet_docs = self._dtinet_score.aggregate(pipeline)
        ranking = 1
        local_dtinet_docs = []
        for doc in dtinet_docs:
            doc['score_entries']['ranking'] = ranking
            local_dtinet_docs.append(doc)
            ranking += 1

        neodti_docs = self._neodti_score.aggregate(pipeline)
        ranking = 1
        local_neodti_docs = []
        for doc in neodti_docs:
            doc['score_entries']['ranking'] = ranking
            local_neodti_docs.append(doc)
            ranking += 1
        
        for doc in local_dtinet_docs:
            drug = self._drug_vocabulary.find_one({'line': doc['line']})
            try:
                drug_name = drug['drug_name']
            except KeyError as e:
                drug_name = ''
            for i in local_neodti_docs:
                if i['line'] == doc['line']:
                    score_ = i['score_entries']['score']
                    ranking_ = i['score_entries']['ranking']
            result.append({
                'drug_id': drug['drug_id'],
                'drug_name': drug_name,
                'DTInet_score': doc['score_entries']['score'],
                'DTInet_ranking': doc['score_entries']['ranking'],
                'NeoDTI_score': score_,
                'NeoDTI_ranking': ranking_,
                'label': doc['score_entries']['label'],
                # 'smiles': protein['smiles'],
                'sequence': drug['unknown']
            })
        
        return result

db = DB()


if __name__ == "__main__":
    start = time.time()
    db = DB()
    d = db.get_score_entries_by_protein_ranking('DTInet', 'BRD4', 10, 1)
    print(d)
    end = time.time()
    print(end - start)