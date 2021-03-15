import unittest

from application.domain import Column


class ColumnTest(unittest.TestCase):
    def test_validate_bigint(self):
        self.assertTrue(Column.validate('bigint', 100))
        self.assertTrue(not Column.validate('bigint', 10.1))
        self.assertTrue(not Column.validate('bigint', 'Texto'))

    def test_validate_numeric(self):
        self.assertTrue(Column.validate('numeric', 10.1))
        self.assertTrue(Column.validate('numeric', 100))
        self.assertTrue(not Column.validate('numeric', 'Texto'))

    def test_validate_varchar(self):
        self.assertTrue(Column.validate('varchar', 'Texto'))
        self.assertTrue(not Column.validate('varchar', 100))
        self.assertTrue(not Column.validate('varchar', 10.1))


if __name__ == "__main__":
    unittest.main()

import unittest

HTML = '''\
<html>
    <head>
        <title>unittest output</title>
    </head>
    <body>
        <table>
            {}
        </table>
    </body>    
<html>
'''

OK_TD = '<tr><td style="color: green;">{}</td></tr>'
ERR_TD = '<tr><td style="color: red;">{}</td></tr>'


class HTMLTestResult(unittest.TestResult):
    def __init__(self, runner):
        unittest.TestResult.__init__(self)
        self.runner = runner
        self.infos = []
        self.current = {}

    def newTest(self):
        self.infos.append(self.current)
        self.current = {}

    def startTest(self, test):
        self.current['id'] = test.id()

    def addSuccess(self, test):
        self.current['result'] = 'ok'
        self.newTest()

    def addError(self, test, err):
        self.current['result'] = 'error'
        self.newTest()

    def addFailure(self, test, err):
        self.current['result'] = 'fail'
        self.newTest()

    def addSkip(self, test, err):
        self.current['result'] = 'skipped'
        self.current['reason'] = err
        self.newTest()


class HTMLTestRunner:
    def run(self, test):
        result = HTMLTestResult(self)
        test.run(result)
        table = ''
        for item in result.infos:
            if item['result'] == 'ok':
                table += OK_TD.format(item['id'])
            else:
                table += ERR_TD.format(item['id'])

        print(HTML.format(table))
        return result


if __name__ == "__main__":
    suite = unittest.TestLoader().discover('.')
    HTMLTestRunner().run(suite)
