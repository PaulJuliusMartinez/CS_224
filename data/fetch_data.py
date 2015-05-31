from scholar import *
from subprocess import call, check_output
from sets import Set
import pycurl
import os

STORAGE_DIR = './texts/'
MIN_WORDS = 1000
DEVNULL = open(os.devnull, 'wb')
curl = pycurl.Curl()

def fetchResultsForCategory(category):
    querier = ScholarQuerier()
    settings = ScholarSettings()
    settings.set_citation_format(ScholarSettings.CITFORM_BIBTEX)
    querier.apply_settings(settings)
    query = SearchScholarQuery()
    query.set_words(category + ' filetype:pdf')
    query.set_include_patents(False)
    querier.send_query(query)
    querier.save_cookies()

    results = []
    for art in querier.articles:
	results.append((
	    art.attrs['title'][0],
	    art.attrs['cluster_id'][0],
	    art.attrs['url_pdf'][0],
	    art.attrs['num_citations'][0]
	))

    return results
    #return [('bad article', '1234', 'http://www.aaai.org/Papers/Symposia/Fall/1994/FS-94-02/FS94-02-034.pdf', 34)]

def fetchPdf(url, cid):
    try:
	curl.setopt(curl.URL, url)
	with open(STORAGE_DIR + cid + '.pdf', 'w') as f:
	    curl.setopt(curl.WRITEFUNCTION, f.write)
	    curl.perform()
	return True
    except:
	return False

def wc(filename):
    return int(check_output(["wc", "-l", filename]).split()[0])

def processPdf(citations, cid):
    pdffilename = STORAGE_DIR + cid + '.pdf'
    txtfilename = STORAGE_DIR + str(citations) + '_' + cid + '.txt'
    err = call(['python', 'pdfminer/tools/pdf2txt.py', '-o', txtfilename, pdffilename], stderr=DEVNULL)
    os.remove(pdffilename)
    if err != 0:
	print 'Error with pdfminer'
	os.remove(txtfilename)
	return False
    if wc(txtfilename) < MIN_WORDS:
	print 'Not enough words, removing ' + txtfilename
	os.remove(txtfilename)
	return False
    return True


if __name__ == "__main__":
    categories = [
	'raster images',
	'computer typography',
	'vector images',
	'computer animation',
	'3D computer models',
	'2D computer models',
	'computer generated imagery',
	'low bandwith computer generated images',
	'real time rendering',
	'keyframe animation',
	'pixel grids',
	'rendering pipeline',
	'shader pipeline',
	'computer caustics lighting',
	'ray tracing',
	'scanline rendering',
	'shading pipeline',
	'catmull spline',
	'procedural textures',
	'bitmap textures',
	'bump mapping',
	'texture mapping',
	'anti-aliasing',
	'volume rendering',
	'charles csuri',
	'donal greenberg',
	'aaron marcus',
	'michael noll',
	'utah teapot',
	'radiosity global illumination',
	'monte carlo rendering',
	'blinn-phong shading',
	'phong shading',
	'gouraud shading',
	'flat shading',
	'displacement mapping',
	'reflection illumination model',
	'specular reflection',
	'diffuse reflection',
	'translucency rendering',
	'motion blur rendering',
	'motion capture animation',
	'crowd simulation',
	'quadtree',
	'octree'
    ]

    used_cids = Set()
    for category in categories:
	results = fetchResultsForCategory(category)
	for title, cid, url, num_citations in results:
	    if cid in used_cids: continue
	    if url is None: continue
	    success = fetchPdf(url, cid)
	    if success:
		success = processPdf(num_citations, cid)
	    if success:
		used_cids.add(cid)
		print 'Successfully fetched ' + title + ' which had ' + str(num_citations) + ' citations'
	    else:
		print 'Failed to fetch ' + title + ' at url: ' + url

	print 'Done processing category ' + category

