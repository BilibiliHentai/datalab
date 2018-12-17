from random import random, randint


class TestData(object):
    kw = ['holy', 'shit', 'ok', 'jesus', 'rivaroxaban', 'prothrombinase']

    def __init__(self):
        self.data = []

    def get_test_data(self, query_keyword=None, data_sum=20):

        for _ in range(data_sum):
            self.data.append(
                {
                    'name': query_keyword if query_keyword is not None and query_keyword in TestData.kw else self._get_random_string(),
                    'score': random(),
                    'cite_num': randint(1,20),
                    'paris': [self._get_random_string() for x in range(10)],
                    'supporting_entries': [self._get_random_string() for x in range(10)],
                }
            )
        return self.data

    def _get_random_string(self):
        characters = 'abcdefghicklmnopgrstuvwxyz'
        return ''.join([characters[randint(0,25)] for i in range(randint(1,10))])


if __name__ == '__main__':
    test_data = TestData()
    data = test_data.get_test_data('holy')
    for i in data:
        print(i)
