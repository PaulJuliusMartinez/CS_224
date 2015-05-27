from scholar import *

querier = ScholarQuerier()
settings = ScholarSettings()
settings.set_citation_format(ScholarSettings.CITFORM_BIBTEX)
querier.apply_settings(settings)
query = SearchScholarQuery()
query.set_words('support vector machines filetype:pdf')
query.set_include_patents(False)
querier.send_query(query)

print len(querier.articles)
for art in querier.articles:
    print art.attrs['title'][0]
    print art.attrs['url_pdf'][0]
    print art.attrs['num_citations'][0]
    print '***'

querier.save_cookies()

