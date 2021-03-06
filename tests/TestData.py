from tde.exceptions import CantExtractData
from tests.src.Base import Base
from tests.src.data import WikipediaLetterCountTextFileData, WikipediaWordCountTextFileData, \
    WikipediaCategoryCountTextFilesData, WikipediaLetterCountHTMLFileData, WikipediaWordCountHTMLFileData, \
    WikipediaCategoryCountHTMLFilesData


class TestInspector(Base):

    def _get_content_of_file(self, file_path):
        with open(file_path) as file_content:
            return file_content.read()

    def test_wikipedia_text_data(self):
        letter_count = WikipediaLetterCountTextFileData()
        letter_count.swallow(self._get_content_of_file('tests/src/source_files/evolution.txt'))
        self.assertEquals({'Évolution (biologie)': 55251}, letter_count.get_data())

        word_count = WikipediaWordCountTextFileData()
        word_count.swallow(self._get_content_of_file('tests/src/source_files/evolution.txt'))
        self.assertEquals({'Évolution (biologie)': 3378}, word_count.get_data())

        category_count = WikipediaCategoryCountTextFilesData()
        category_count.swallow(self._get_content_of_file('tests/src/source_files/evolution.txt'))
        self.assertEquals({'Science': 1}, category_count.get_data())
        category_count.swallow(self._get_content_of_file('tests/src/source_files/relativite.txt'))
        self.assertEquals({'Science': 2}, category_count.get_data())

    def test_wikipedia_html_data(self):
        letter_count = WikipediaLetterCountHTMLFileData()
        letter_count.swallow(self._get_content_of_file('tests/src/source_files/evolution.html'))
        self.assertEquals({'Évolution (biologie)': 59883}, letter_count.get_data())

        word_count = WikipediaWordCountHTMLFileData()
        word_count.swallow(self._get_content_of_file('tests/src/source_files/evolution.html'))
        self.assertEquals({'Évolution (biologie)': 3460}, word_count.get_data())

        category_count = WikipediaCategoryCountHTMLFilesData()
        category_count.swallow(self._get_content_of_file('tests/src/source_files/evolution.html'))
        self.assertEquals({'Science': 1}, category_count.get_data())
        category_count.swallow(self._get_content_of_file('tests/src/source_files/relativite.html'))
        self.assertEquals({'Science': 2}, category_count.get_data())

    def test_cant_extract(self):
        letter_count = WikipediaLetterCountHTMLFileData()
        courgettes_farcies_text = self._get_content_of_file('tests/src/source_files/aubergines_farcies.txt')
        self.assertRaises(CantExtractData, letter_count.swallow, courgettes_farcies_text)
