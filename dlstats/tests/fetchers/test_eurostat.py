# -*- coding: utf-8 -*-

import tempfile
import datetime
import os
from pprint import pprint
from urllib.parse import urlparse
from urllib.request import url2pathname, pathname2url

from dlstats.fetchers._commons import Datasets
from dlstats.fetchers import eurostat
from dlstats import constants

import unittest
from unittest import mock

from dlstats.tests.base import RESOURCES_DIR
from dlstats.tests.fetchers.base import BaseFetcherTestCase, BaseDBFetcherTestCase

# Nombre de série dans les exemples
SERIES_COUNT = 1

PROVIDER_NAME = 'Eurostat'

DATASETS = {'nama_10_gdp': {}}

#---Dataset nama_10_gdp
DATASETS['nama_10_gdp']["dimensions_count"] = 4 
DATASETS['nama_10_gdp']["name"] = "nama_10_gdp"
DATASETS['nama_10_gdp']["doc_href"] = None
DATASETS['nama_10_gdp']["last_update"] = datetime.datetime(2015,10,26)
DATASETS['nama_10_gdp']["filename"] = "nama_10_gdp"
DATASETS['nama_10_gdp']["sdmx"] = """
<?xml version="1.0" encoding="UTF-8"?>
<CompactData xmlns="http://www.SDMX.org/resources/SDMXML/schemas/v2_0/message" xmlns:common="http://www.SDMX.org/resources/SDMXML/schemas/v2_0/common" xmlns:compact="http://www.SDMX.org/resources/SDMXML/schemas/v2_0/compact" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:data="urn:sdmx:org.sdmx.infomodel.keyfamily.KeyFamily=EUROSTAT:nama_10_gdp_DSD:compact" xsi:schemaLocation="http://www.SDMX.org/resources/SDMXML/schemas/v2_0/message SDMXMessage.xsd urn:sdmx:org.sdmx.infomodel.keyfamily.KeyFamily=EUROSTAT:nama_10_gdp_DSD:compact EUROSTAT_nama_10_gdp_Compact.xsd http://www.SDMX.org/resources/SDMXML/schemas/v2_0/compact SDMXCompactData.xsd">
<Header>
<ID>nama_10_gdp</ID>
<Test>false</Test>
<Name xml:lang="en">nama_10_gdp</Name>
<Prepared>2015-10-26T21:08:39</Prepared>
<Sender id="EUROSTAT">
<Name xml:lang="en">EUROSTAT</Name>
</Sender>
<Receiver id="XML">
<Name xml:lang="en">SDMX-ML File</Name>
</Receiver>
<DataSetID>nama_10_gdp</DataSetID>
<Extracted>2015-10-26T21:08:39</Extracted>
</Header>
<data:DataSet>
<data:Series FREQ="A" unit="CLV05_MEUR" na_item="B1G" geo="AT" TIME_FORMAT="P1Y">
<data:Obs TIME_PERIOD="1995" OBS_VALUE="176840.7" />
</data:Series>
</data:DataSet>
</CompactData>
"""

DATASETS['nama_10_gdp']["dsd"] = """
<?xml version="1.0" encoding="UTF-8"?>
<Structure xmlns="http://www.SDMX.org/resources/SDMXML/schemas/v2_0/message" xmlns:common="http://www.SDMX.org/resources/SDMXML/schemas/v2_0/common" xmlns:compact="http://www.SDMX.org/resources/SDMXML/schemas/v2_0/compact" xmlns:cross="http://www.SDMX.org/resources/SDMXML/schemas/v2_0/cross" xmlns:generic="http://www.SDMX.org/resources/SDMXML/schemas/v2_0/generic" xmlns:query="http://www.SDMX.org/resources/SDMXML/schemas/v2_0/query" xmlns:structure="http://www.SDMX.org/resources/SDMXML/schemas/v2_0/structure" xmlns:utility="http://www.SDMX.org/resources/SDMXML/schemas/v2_0/utility" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.SDMX.org/resources/SDMXML/schemas/v2_0/message SDMXMessage.xsd">
<Header>
<ID>nama_10_gdp_DSD</ID>
<Test>false</Test>
<Truncated>false</Truncated>
<Name xml:lang="en">nama_10_gdp_DSD</Name>
<Prepared>2015-10-26T21:08:39</Prepared>
<Sender id="EUROSTAT">
<Name xml:lang="en">EUROSTAT</Name>
</Sender>
<Receiver id="XML">
<Name xml:lang="en">XML File</Name>
</Receiver>
</Header>

<CodeLists>
<structure:CodeList id="CL_UNIT" agencyID="EUROSTAT" isFinal="true">
<structure:Name xml:lang="en">Unit of measure</structure:Name>
<structure:Name xml:lang="de">Maßeinheit</structure:Name>
<structure:Name xml:lang="fr">Unité de mesure</structure:Name>
<structure:Code value="CLV05_MEUR">
<structure:Description xml:lang="en">Chain linked volumes (2005), million euro</structure:Description>
<structure:Description xml:lang="de">Verkettete Volumen (2005), Millionen Euro</structure:Description>
<structure:Description xml:lang="fr">Volumes chaînés (2005), millions d'euros</structure:Description>
</structure:Code>
</structure:CodeList>
<structure:CodeList id="CL_NA_ITEM" agencyID="EUROSTAT" isFinal="true">
<structure:Name xml:lang="en">National accounts indicator (ESA10)</structure:Name>
<structure:Name xml:lang="de">Volkswirtschaftliche Gesamtrechnungen Indikator (ESVG10)</structure:Name>
<structure:Name xml:lang="fr">Indicateur des comptes nationaux (SEC10)</structure:Name>
<structure:Code value="B1G">
<structure:Description xml:lang="en">Value added, gross</structure:Description>
<structure:Description xml:lang="de">Bruttowertschöpfung</structure:Description>
<structure:Description xml:lang="fr">Valeur ajoutée, brute</structure:Description>
</structure:Code>
</structure:CodeList>
<structure:CodeList id="CL_GEO" agencyID="EUROSTAT" isFinal="true">
<structure:Name xml:lang="en">Geopolitical entity (reporting)</structure:Name>
<structure:Name xml:lang="de">Geopolitische Meldeeinheit</structure:Name>
<structure:Name xml:lang="fr">Entité géopolitique (déclarante)</structure:Name>
<structure:Code value="AT">
<structure:Description xml:lang="en">Austria</structure:Description>
<structure:Description xml:lang="de">Österreich</structure:Description>
<structure:Description xml:lang="fr">Autriche</structure:Description>
</structure:Code>
</structure:CodeList>
<structure:CodeList id="CL_TIME_FORMAT" agencyID="SDMX" isFinal="true">
<structure:Name xml:lang="en">Time Format</structure:Name>
<structure:Code value="P1Y">
<structure:Description xml:lang="en">Annual</structure:Description>
</structure:Code>
</structure:CodeList>
<structure:CodeList id="CL_FREQ" agencyID="SDMX" isFinal="true">
<structure:Name xml:lang="en">Frequency code list</structure:Name>
<structure:Code value="A">
<structure:Description xml:lang="en">Annual</structure:Description>
</structure:Code>
</structure:CodeList>
<structure:CodeList id="CL_OBS_STATUS" agencyID="EUROSTAT" isFinal="true">
<structure:Name xml:lang="en">Observation status code list</structure:Name>
<structure:Code value="p">
<structure:Description xml:lang="en">provisional</structure:Description>
<structure:Description xml:lang="de">vorläufig</structure:Description>
<structure:Description xml:lang="fr">provisoire</structure:Description>
</structure:Code>
</structure:CodeList>
</CodeLists>

<Concepts>
<structure:ConceptScheme agencyID="EUROSTAT" id="CONCEPTS" isFinal="true">
<structure:Name xml:lang="en">Concepts</structure:Name>
<structure:Concept id="FREQ"><structure:Name xml:lang="en">Frequency</structure:Name>
</structure:Concept>
<structure:Concept id="unit"><structure:Name xml:lang="en">Unit of measure</structure:Name>
<structure:Name xml:lang="de">Maßeinheit</structure:Name>
<structure:Name xml:lang="fr">Unité de mesure</structure:Name>
</structure:Concept>
<structure:Concept id="na_item"><structure:Name xml:lang="en">National accounts indicator (ESA10)</structure:Name>
<structure:Name xml:lang="de">Volkswirtschaftliche Gesamtrechnungen Indikator (ESVG10)</structure:Name>
<structure:Name xml:lang="fr">Indicateur des comptes nationaux (SEC10)</structure:Name>
</structure:Concept>
<structure:Concept id="geo"><structure:Name xml:lang="en">Geopolitical entity (reporting)</structure:Name>
<structure:Name xml:lang="de">Geopolitische Meldeeinheit</structure:Name>
<structure:Name xml:lang="fr">Entité géopolitique (déclarante)</structure:Name>
</structure:Concept>
<structure:Concept id="TIME_PERIOD"><structure:Name xml:lang="en">Time period or range</structure:Name>
</structure:Concept>
<structure:Concept id="OBS_VALUE"><structure:Name xml:lang="en">Observation Value</structure:Name>
</structure:Concept>
<structure:Concept id="OBS_STATUS"><structure:Name xml:lang="en">Observation Status</structure:Name>
</structure:Concept>
<structure:Concept id="TIME_FORMAT"><structure:Name xml:lang="en">Time Format</structure:Name>
</structure:Concept>
</structure:ConceptScheme>
</Concepts>

<KeyFamilies>
<structure:KeyFamily id="nama_10_gdp_DSD" agencyID="EUROSTAT" isFinal="true" isExternalReference="false"><structure:Name xml:lang="en">nama_10_gdp_DSD</structure:Name>

<structure:Components>
<structure:Dimension conceptSchemeRef="CONCEPTS" conceptSchemeAgency="EUROSTAT" conceptRef="FREQ" codelistAgency="SDMX" codelist="CL_FREQ" isFrequencyDimension="true"/>
<structure:Dimension conceptSchemeRef="CONCEPTS" conceptSchemeAgency="EUROSTAT" conceptRef="unit" codelistAgency="ESTAT" codelist="CL_UNIT" crossSectionalAttachDataSet="false" crossSectionalAttachGroup="false" crossSectionalAttachSection="true" crossSectionalAttachObservation="false"></structure:Dimension>
<structure:Dimension conceptSchemeRef="CONCEPTS" conceptSchemeAgency="EUROSTAT" conceptRef="na_item" codelistAgency="ESTAT" codelist="CL_NA_ITEM" crossSectionalAttachDataSet="false" crossSectionalAttachGroup="false" crossSectionalAttachSection="true" crossSectionalAttachObservation="false"></structure:Dimension>
<structure:Dimension conceptSchemeRef="CONCEPTS" conceptSchemeAgency="EUROSTAT" conceptRef="geo" codelistAgency="ESTAT" codelist="CL_GEO" crossSectionalAttachDataSet="false" crossSectionalAttachGroup="false" crossSectionalAttachSection="true" crossSectionalAttachObservation="false"></structure:Dimension>
<structure:TimeDimension conceptSchemeRef="CONCEPTS" conceptSchemeAgency="EUROSTAT" conceptRef="TIME_PERIOD"><structure:TextFormat textType="String"></structure:TextFormat>
</structure:TimeDimension>
<structure:PrimaryMeasure conceptSchemeRef="CONCEPTS" conceptSchemeAgency="EUROSTAT" conceptRef="OBS_VALUE">
<structure:TextFormat textType="Double"></structure:TextFormat>
</structure:PrimaryMeasure>

<structure:Attribute conceptRef="TIME_FORMAT" conceptSchemeRef="CONCEPTS" conceptSchemeAgency="EUROSTAT" codelistAgency="SDMX" codelist="CL_TIME_FORMAT" attachmentLevel="Series" assignmentStatus="Mandatory"></structure:Attribute>
<structure:Attribute conceptSchemeRef="CONCEPTS" conceptSchemeAgency="EUROSTAT" conceptRef="OBS_STATUS" codelistAgency="EUROSTAT" codelist="CL_OBS_STATUS" attachmentLevel="Observation" assignmentStatus="Conditional" crossSectionalAttachDataSet="false" crossSectionalAttachGroup="false" crossSectionalAttachSection="false" crossSectionalAttachObservation="true"><structure:TextFormat textType="String"></structure:TextFormat>
</structure:Attribute>
</structure:Components>
</structure:KeyFamily>
</KeyFamilies>

</Structure>
"""

TABLE_OF_CONTENT = """<?xml version="1.0" encoding="UTF-8"?>
<nt:tree xmlns:nt="urn:eu.europa.ec.eurostat.navtree" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:eu.europa.ec.eurostat.navtree http://ec.europa.eu/eurostat/estat-navtree-portlet-prod/xsd/TableOfContent.xsd" creationDate="20151027T1102">
  <nt:branch>
    <nt:title language="en">Database by themes</nt:title>
    <nt:title language="fr">Base de données par thèmes</nt:title>
    <nt:title language="de">Datenbank nach Themen</nt:title>
    <nt:code>data</nt:code>
    <nt:children>
      <nt:branch>
        <nt:title language="en">Economy and finance</nt:title>
        <nt:title language="fr">Économie et finances</nt:title>
        <nt:title language="de">Wirtschaft und Finanzen</nt:title>
        <nt:code>economy</nt:code>
        <nt:children>
          <nt:branch>
            <nt:title language="en">National accounts (ESA 2010)</nt:title>
            <nt:title language="fr">Comptes nationaux (SEC 2010)</nt:title>
            <nt:title language="de">Volkswirtschaftliche Gesamtrechnungen (ESVG 2010)</nt:title>
            <nt:code>na10</nt:code>
            <nt:children>
              <nt:branch>
                <nt:title language="en">Annual national accounts</nt:title>
                <nt:title language="fr">Comptes nationaux annuels</nt:title>
                <nt:title language="de">Jährliche Volkswirtschaftliche Gesamtrechnungen</nt:title>
                <nt:code>nama_10</nt:code>
                <nt:children>
                  <nt:branch>
                    <nt:title language="en">Main GDP aggregates</nt:title>
                    <nt:title language="fr">Principaux agrégats du PIB</nt:title>
                    <nt:title language="de">Hauptaggregate des BIP</nt:title>
                    <nt:code>nama_10_ma</nt:code>
                    <nt:children>
                      <nt:leaf type="dataset">
                        <nt:title language="en">GDP and main components (output, expenditure and income)</nt:title>
                        <nt:title language="fr">PIB et principaux composants (production, dépenses et revenu)</nt:title>
                        <nt:title language="de">BIP und Hauptkomponenten (Produktionswert, Ausgaben und Einkommen)</nt:title>
                        <nt:code>nama_10_gdp</nt:code>
                        <nt:lastUpdate>26.10.2015</nt:lastUpdate>
                        <nt:lastModified>11.08.2015</nt:lastModified>
                        <nt:dataStart>1975</nt:dataStart>
                        <nt:dataEnd>2014</nt:dataEnd>
                        <nt:values>417804</nt:values>
                        <nt:unit language="en" />
                        <nt:unit language="fr" />
                        <nt:unit language="de" />
                        <nt:shortDescription language="en" />
                        <nt:shortDescription language="fr" />
                        <nt:shortDescription language="de" />
                        <nt:metadata format="html">http://ec.europa.eu/eurostat/cache/metadata/en/nama_10_esms.htm</nt:metadata>
                        <nt:metadata format="sdmx">http://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?file=metadata/nama_10_esms.sdmx.zip</nt:metadata>
                        <nt:downloadLink format="tsv">http://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?file=data/nama_10_gdp.tsv.gz</nt:downloadLink>
                        <nt:downloadLink format="sdmx">http://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?file=data/nama_10_gdp.sdmx.zip</nt:downloadLink>
                      </nt:leaf>
                      <nt:leaf type="dataset">
                        <nt:title language="en">Final consumption aggregates by durability</nt:title>
                        <nt:title language="fr">Principaux agrégats de la consommation finale par durabilité</nt:title>
                        <nt:title language="de">Hauptaggregate des letzten Verbrauch nach Dauerhaftigkeit</nt:title>
                        <nt:code>nama_10_fcs</nt:code>
                        <nt:lastUpdate>26.10.2015</nt:lastUpdate>
                        <nt:lastModified>12.10.2015</nt:lastModified>
                        <nt:dataStart>1975</nt:dataStart>
                        <nt:dataEnd>2014</nt:dataEnd>
                        <nt:values>69954</nt:values>
                        <nt:unit language="en" />
                        <nt:unit language="fr" />
                        <nt:unit language="de" />
                        <nt:shortDescription language="en" />
                        <nt:shortDescription language="fr" />
                        <nt:shortDescription language="de" />
                        <nt:metadata format="html">http://ec.europa.eu/eurostat/cache/metadata/en/nama_10_esms.htm</nt:metadata>
                        <nt:metadata format="sdmx">http://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?file=metadata/nama_10_esms.sdmx.zip</nt:metadata>
                        <nt:downloadLink format="tsv">http://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?file=data/nama_10_fcs.tsv.gz</nt:downloadLink>
                        <nt:downloadLink format="sdmx">http://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?file=data/nama_10_fcs.sdmx.zip</nt:downloadLink>
                      </nt:leaf>
                    </nt:children>
                  </nt:branch>
                </nt:children>
              </nt:branch>
            </nt:children>
          </nt:branch>
        </nt:children>
      </nt:branch>
    </nt:children>
  </nt:branch>
</nt:tree>
""".encode(encoding='UTF_8')




def make_url(self):
    import tempfile
    filepath = os.path.abspath(os.path.join(tempfile.gettempdir(), 
                                            self.provider_name, 
                                            self.dataset_code,
                                            "tests",
                                            self.dataset_code+'.sdmx.zip'))
    return "file:%s" % pathname2url(filepath)

def local_get(url, *args, **kwargs):
    "Fetch a stream from local files."
    from requests import Response

    p_url = urlparse(url)
    if p_url.scheme != 'file':
        raise ValueError("Expected file scheme")

    filename = url2pathname(p_url.path)
    response = Response()
    response.status_code = 200
    response.raw = open(filename, 'rb')
    return response

def write_zip_file(zip_filepath, filename, dsd, sdmx):
    """Create file in zipfile
    """
    import zipfile

    with zipfile.ZipFile(zip_filepath, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(filename+'.dsd.xml', dsd)
        zf.writestr(filename+'.sdmx.xml', sdmx)
        
def get_filepath(dataset_code):
    """Create SDMX file in zipfile
    
    Return local filepath of zipfile
    """
    dataset = DATASETS[dataset_code]
    zip_filename = dataset_code+'.sdmx.zip'
    filename = dataset_code
    dirpath = os.path.join(tempfile.gettempdir(), PROVIDER_NAME, dataset_code, "tests")
    filepath = os.path.abspath(os.path.join(dirpath, zip_filename))
    
    if os.path.exists(filepath):
        os.remove(filepath)
        
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    
    write_zip_file(filepath, filename, DATASETS[dataset_code]['dsd'], DATASETS[dataset_code]['sdmx'])
    
    return filepath


        

def load_fake_datas(select_dataset_code=None):
    """Load datas from DATASETS dict
    
    key: DATASETS[dataset_code]['datas']
    """
    
    fetcher = eurostat.Eurostat()
    
    results = {}
    
    for dataset_code, dataset in DATASETS.items():
        
        if select_dataset_code and select_dataset_code != dataset_code:
            continue
        
        _dataset = Datasets(provider_name=fetcher.provider_name, 
                    dataset_code=dataset_code, 
                    name=dataset['name'], 
                    doc_href=dataset['doc_href'], 
                    fetcher=fetcher, 
                    is_load_previous_version=False)
        
        dataset_datas = eurostat.EurostatData(_dataset, is_autoload=False)
        dataset_datas._load_datas(dataset['datas'])
        
        results[dataset_code] = {'series': []}

        for d in dataset_datas.rows:
            results[dataset_code]['series'].append(dataset_datas.build_serie(d))
            
    #pprint(results)
    return results

def get_table_of_content(self):
    return TABLE_OF_CONTENT

class EurostatDatasetsTestCase(BaseFetcherTestCase):
    """Fetchers Tests - No DB access
    """
    
    # nosetests -s -v dlstats.tests.fetchers.test_eurostat:EurostatDatasetsTestCase
    
    @unittest.skipIf(True, "TODO")    
    def test_nama_10_gdp(self):
        
        # nosetests -s -v dlstats.tests.fetchers.test_eurostat:EurostatDatasetsTestCase.test_nama_10_gdp        
        datas = load_fake_datas('nama_10_gdp')
        print("")
        pprint(datas)

        attempt = {'nama_10_gdp': {'series': [{'attributes': {},
                                            'datasetCode': 'nama_10_gdp',
                                            'dimensions': {'FREQ': "A",
                                                           'unit': "CLV05_MEUR",
                                                           'na_item': "B1G",
                                                           'geo': "AT",
                                                           'TIME_FORMAT': "P1Y"},
                                            'endDate': 45,
                                            'frequency': 'A',
                                            'key': 'A.CLV05_MEUR.B1G.AT',
                                            'name': '',
                                  'provider': 'Eurostat',
                                  'startDate': 25,
                                  'values': ["176840.7", "180307.4", "184320.1"]}]}}        
        self.assertDictEqual(datas, attempt)

        
class EurostatDatasetsDBTestCase(BaseDBFetcherTestCase):
    """Fetchers Tests - with DB
    
    sources from DATASETS[dataset_code]['datas'] written in zip file
    """
    
    # nosetests -s -v dlstats.tests.fetchers.test_eurostat:EurostatDatasetsDBTestCase
    
    def setUp(self):
        BaseDBFetcherTestCase.setUp(self)
        self.fetcher = eurostat.Eurostat(db=self.db, es_client=self.es)
        self.dataset_code = None
        self.dataset = None        
        self.filepath = None

    @mock.patch('requests.get', local_get)
    @mock.patch('dlstats.fetchers.eurostat.EurostatData.make_url', make_url)    
    def _common_tests(self):

        self._collections_is_empty()
        
        self.filepath = get_filepath(self.dataset_code)
        self.assertTrue(os.path.exists(self.filepath))
        
        # provider.update_database
        self.fetcher.provider.update_database()
        provider = self.db[constants.COL_PROVIDERS].find_one({"name": self.fetcher.provider_name})
        self.assertIsNotNone(provider)
        
        # upsert_categories
#        self.fetcher.upsert_categories()
#        category = self.db[constants.COL_CATEGORIES].find_one({"provider": self.fetcher.provider_name, 
#                                                               "categoryCode": self.dataset_code})
#        self.assertIsNotNone(category)
        
        dataset = Datasets(provider_name=self.fetcher.provider_name, 
                           dataset_code=self.dataset_code, 
                           name=DATASETS[self.dataset_code]['name'],
                           last_update=DATASETS[self.dataset_code]['last_update'],
                           doc_href=DATASETS[self.dataset_code]['doc_href'], 
                           fetcher=self.fetcher)

        # manual Data for iterator
        fetcher_data = eurostat.EurostatData(dataset) 
        dataset.series.data_iterator = fetcher_data
        dataset.update_database()

        self.dataset = self.db[constants.COL_DATASETS].find_one({"provider": self.fetcher.provider_name, 
                                                            "datasetCode": self.dataset_code})
        
        self.assertIsNotNone(self.dataset)
        
        self.assertEqual(len(self.dataset["dimensionList"]), DATASETS[self.dataset_code]["dimensions_count"])
        
        series = self.db[constants.COL_SERIES].find({"provider": self.fetcher.provider_name, 
                                                     "datasetCode": self.dataset_code})
        self.assertEqual(series.count(), SERIES_COUNT)
        
        
    def test_nama_10_gdp(self):
        
        # nosetests -s -v dlstats.tests.fetchers.test_eurostat:EurostatDatasetsDBTestCase.test_nama_10_gdp
                
        self.dataset_code = 'nama_10_gdp'
        
        self._common_tests()        

        serie = self.db[constants.COL_SERIES].find_one({"provider": self.fetcher.provider_name, 
                                                        "datasetCode": self.dataset_code,
                                                        "key": "A.CLV05_MEUR.B1G.AT"})
        self.assertIsNotNone(serie)
        
        d = serie['dimensions']
        self.assertEqual(d["freq"], 'A')
        self.assertEqual(d["unit"], 'CLV05_MEUR')
        self.assertEqual(d["geo"], 'AT')
        
        #TODO: meta_datas tests  

        #TODO: clean filepath


class LightEurostatDatasetsDBTestCase(BaseDBFetcherTestCase):
    """Fetchers Tests - with DB and lights sources
    
    1. Créer un fichier zip à partir des données du dict DATASETS
    
    2. Execute le fetcher normalement et en totalité
    """
    
    # nosetests -s -v dlstats.tests.fetchers.test_eurostat:LightEurostatDatasetsDBTestCase
    
    def setUp(self):
        BaseDBFetcherTestCase.setUp(self)
        self.fetcher = eurostat.Eurostat(db=self.db, es_client=self.es)
        self.dataset_code = None
        self.dataset = None        
        self.filepath = None
        
    @mock.patch('requests.get', local_get)
    @mock.patch('dlstats.fetchers.eurostat.EurostatData.make_url', make_url)    
    @mock.patch('dlstats.fetchers.eurostat.Eurostat.get_table_of_content', get_table_of_content)    
    def _common_tests(self):

        self._collections_is_empty()

        # Write czv/zip file in local directory
        filepath = get_filepath(self.dataset_code)
        self.assertTrue(os.path.exists(filepath))
        # Replace dataset url by local filepath
        DATASETS[self.dataset_code]['url'] = "file:%s" % pathname2url(filepath)

        self.fetcher.provider.update_database()
        provider = self.db[constants.COL_PROVIDERS].find_one({"name": self.fetcher.provider_name})
        self.assertIsNotNone(provider)
        
        self.fetcher.upsert_categories()
        category = self.db[constants.COL_CATEGORIES].find_one({"provider": self.fetcher.provider_name, 
                                                               "categoryCode": self.dataset_code})
        self.assertIsNotNone(category)

        self.fetcher.upsert_dataset(self.dataset_code)
        
        self.dataset = self.db[constants.COL_DATASETS].find_one({"provider": self.fetcher.provider_name, 
                                                            "datasetCode": self.dataset_code})
        self.assertIsNotNone(self.dataset)

        series = self.db[constants.COL_SERIES].find({"provider": self.fetcher.provider_name, 
                                                     "datasetCode": self.dataset_code})

        self.assertEqual(series.count(), SERIES_COUNT)

    def test_nama_10_gdp(self):
        
        # nosetests -s -v dlstats.tests.fetchers.test_eurostat:LightEurostatDatasetsDBTestCase.test_nama_10_gdp

        self.dataset_code = 'nama_10_gdp'        

        self._common_tests()

        #TODO: meta_datas tests  

@unittest.skipUnless('FULL_REMOTE_TEST' in os.environ, "Skip - not full remote test")
class FullEurostatDatasetsDBTestCase(BaseDBFetcherTestCase):
    """Fetchers Tests - with DB and real download sources
    
    1. Télécharge ou utilise des fichiers existants
    
    2. Execute le fetcher normalement et en totalité
    """
    
    # FULL_REMOTE_TEST=1 nosetests -s -v dlstats.tests.fetchers.test_eurostat:FullEurostatDatasetsDBTestCase
    
    def setUp(self):
        BaseDBFetcherTestCase.setUp(self)
        self.fetcher = eurostat.Eurostat(db=self.db, es_client=self.es)
        self.dataset_code = None
        self.dataset = None        
        self.filepath = None
        
    #@mock.patch('requests.get', local_get)
    def _common_tests(self):

        self._collections_is_empty()

        self.fetcher.provider.update_database()
        provider = self.db[constants.COL_PROVIDERS].find_one({"name": self.fetcher.provider_name})
        self.assertIsNotNone(provider)
        
        self.fetcher.upsert_categories()
        category = self.db[constants.COL_CATEGORIES].find_one({"provider": self.fetcher.provider_name, 
                                                               "categoryCode": self.dataset_code})
        self.assertIsNotNone(category)
        
        self.fetcher.upsert_dataset(self.dataset_code)
        
        self.dataset = self.db[constants.COL_DATASETS].find_one({"provider": self.fetcher.provider_name, 
                                                            "datasetCode": self.dataset_code})
        self.assertIsNotNone(self.dataset)

        series = self.db[constants.COL_SERIES].find({"provider": self.fetcher.provider_name, 
                                                     "datasetCode": self.dataset_code})

        series_count = series.count()
        self.assertTrue(series_count > 1)
        print(self.dataset_code, series_count)

    def test_nama_10_gdp(self):
        
        # nosetests -s -v dlstats.tests.fetchers.test_bis:FullEurostatDatasetsDBTestCase.test_nama_10_gdp

        self.dataset_code = 'nama_10_gdp'        

        self._common_tests()
        
        #self.fail("test")

        #TODO: meta_datas tests  

