from random import random, randint


class TestData(object):
    kw = ['holy', 'shit', 'ok', 'jesus', 'rivaroxaban', 'prothrombinase']


    def get_test_data(self, query_keyword):
        self.data = []
        if query_keyword in TestData.kw:
            for _ in range(100):
                self.data.append(
                    {
                        'name': self._get_random_string(),
                        'avg_score': random(),
                        'cite_num': randint(1,20),
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