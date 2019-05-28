import pymongo


client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['dtitool']
coll = db['protein_vocabulary']


class DB:
    def __init__(self):
        self._client = pymongo.MongoClient('mongodb://localhost:27017/')
        self._db = self._client['dtitool']
        self._protein_vocabulary = self._db['protein_vocabulary']
        self._drug_vocabulary = self._db['drug_vocabulary']
        self._dtinet_score = self._db['DTInet_score']
        self._neodti_score = self._db['NeoDTI_score']

    """
    argument which should be "DTInet" or "NeoDTI"
    """
    def get_score_entries(self, drug_name, which):
        query = {'drug_name': drug_name}
        try:
            drug = self._drug_vocabulary.find(query)[0]
        except IndexError as e:
            return None
        line = drug['line']
        return self._get_score_entries_by_line(line, which)
        
    
    def _get_score_entries_by_line(self, line, which):
        pipeline = [
            {"$match": {"line": str(line)}}, # TODO
            {"$unwind": "$score_entries"},
            {"$sort": {"score_entries.score": -1}},
            {"$limit": 10}
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
        
    def _get_protein_name(self, protein_id):
        query = {"protein_id": protein_id}
        docs = self._protein_vocabulary.find(query)
        return docs[0]['protein_name']

    def _get_protein_smiles(self, protein_id):
        query = {"protein_id": protein_id}
        docs = self._protein_vocabulary.find(query)
        return docs[0]['smiles']

if __name__ == "__main__":
    db = DB()
    s = db.get_score_entries('GSK-256066', 'DTInet')
    print(s)
