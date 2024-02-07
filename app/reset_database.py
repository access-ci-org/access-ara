from models import db
from models.rps import RPS
from models.jobClass import JobClass
from models.rpJobClass import RpJobClass
from models.researchField import ResearchFields
from models.rpResearchField import RpResearchField
from models.software import Software
from models.rpSoftware import RpSoftware
from models.gui import GUI
from models.rpGUI import RpGUI
from models.rpMemory import RpMemory
from models.rpInfo import RpInfo
from logic.rp_modules import get_modules_and_versions
from pushToDb import update_db_from_conf
import glob #for reading the text files
import sys
import re

def recreate_tables():

    """
    delete and recreate all of the tables in the database
    """
    db.connect(reuse_if_open=True)
    
    with db.atomic() as transaction:
        try:
            tables = db.get_tables()
            print(f"Dropping tables: {tables}")
            db.drop_tables([RPS,JobClass,RpJobClass,ResearchFields,RpResearchField,Software,RpSoftware,GUI,RpGUI,RpMemory,RpInfo])

            db.create_tables([RPS,JobClass,RpJobClass,ResearchFields,RpResearchField,Software,RpSoftware,GUI,RpGUI,RpMemory,RpInfo])
            tables = db.get_tables()
            print(f"Recreated tables: {tables}")
        except Exception as e:
            transaction.rollback()
            print(e)

    db.close()

def reset_with_test_data():

    """
    Add test data to the database. This data is used for testing our application 
    and is not meant to be used for the actual application.
    """
    db.connect(reuse_if_open=True)
    rps = [
    {"name":"ACES", "scratch_tb":1, "longterm_tb":100, "gpu":2, "graphical":2},
    {"name":"Anvil", "scratch_tb":100, "longterm_tb":50, "gpu":2},
    {"name":"Bridges-2", "scratch_tb":0, "longterm_tb":0, "gpu": 2, "graphical":2},
    {"name":"DARWIN", "scratch_tb":2, "longterm_tb":10, "gpu": 2, "graphical":2},
    {"name":"Delta", "scratch_tb":1.5, "longterm_tb":0.5, "gpu": 2, "graphical":2},
    {"name":"Expanse", "scratch_tb":7000, "longterm_tb":12000, "gpu": 2, "graphical":2},
    {"name":"FASTER", "scratch_tb":1, "longterm_tb":50, "gpu":2, "graphical":2},
    {"name":"Jetstream2", "scratch_tb":0, "longterm_tb":0, "gpu":2, "virtual_machine":2, "always_running":2},
    {"name":"OOKAMI", "scratch_tb":30, "longterm_tb":80, "gpu":2},
    {"name":"KyRIC", "scratch_tb":10, "longterm_tb":0.5, "graphical":2},
    {"name":"Rockfish", "scratch_tb":10, "longterm_tb":100, "gpu":2},
    {"name":"Stampede-2", "scratch_tb":0, "longterm_tb":1, "graphical":2},
    {"name":"RANCH", "scratch_tb":0, "longterm_tb":20},
    {"name":"Open Science Grid", "scratch_tb":0, "longterm_tb":0.5, "gpu":2},
    {"name":"Open Storage Network", "scratch_tb":0, "longterm_tb":0},
    ]
    fields = [
        {"field_name":"Biology"},
        {"field_name":"Chemistry"},
        {"field_name":"Physics"},
        {"field_name":"Computer Science"},
        {"field_name":"Civil Engineering"},
        {"field_name":"Economics"},
        {"field_name":"Linguistics"},
        {"field_name":"History"},
        {"field_name":"Agriculture"},
        {"field_name":"Medicine"},
    ]

    jobClass = [
        {"class_name":"Data Analytics"},
        {"class_name":"Data Mining"},
        {"class_name":"NLP"},
        {"class_name":"Textual Analysis"},
        {"class_name":"Modeling and Simulation"},
        {"class_name":"Bioinformatics"},
        {"class_name":"Biophysics"},
        {"class_name":"BioChemistry"},
        {"class_name":"Fluid Dynamics"},
        {"class_name":"Image Processing"},
        {"class_name":"Machine Learning"},
        {"class_name": "Materials Science"},
        {"class_name":"Astronomic Science"},
        {"class_name":"Digital Humanities"},
        {"class_name":"Computational Chemistry"},
        {"class_name":"Genomics"},
        {"class_name":"Deep Learning"},
        {"class_name":"High Energy Physics"},
        {"class_name":"Virtual Machine"},
        {"class_name":"General"},
        {"class_name":"Parallel"},
    ]
    #Class of jobs
    jobClassAndRps = {"Data Analytics":['delta', 'bridges-2', 'darwin'],
                    "Data Mining":['darwin'],
                    "NLP":['kyric'],
                    "Textual Analysis":['delta'],
                    "Modeling and Simulation":['delta'],
                    "Bioinformatics":['kyric','expanse'],
                    "Biophysics":['kyric','expanse'],
                    "Biochemistry":['kyric','expanse'],
                    "Fluid Dynamics":['delta'],
                    "Materials Science":['expanse'], 
                    "Image Processing":['darwin'], 
                    "Machine Learning":['delta','bridges-2','darwin'],
                    "Astronomic Science":['expanse'], 
                    "Digital Humanities":[], 
                    "Computational Chemistry":['expanse'], 
                    "Genomics":[], 
                    "Deep Learning":['delta'], 
                    "High Energy Physics":['expanse'],
                    "Virtual Machine":['jetstream2'], 
                    "General":['stampede-2','darwin'], 
                    "Parallel":['stampede-2']}
    
    #Types of GUI's
    Gui = [
    {"gui_name":"Open OnDemand"},
    {"gui_name":"RStudio"},
    {"gui_name":"JupyterLab"},
    {"gui_name":"Exosphere"},
    {"gui_name":"Horizon"},
    {"gui_name":"CACAO"},
    ]
    
    # which GUIs belong to which RPs
    rpGUI_together = {
        "Open OnDemand":['bridges-2', 'expanse', 'anvil', 'aces', 'faster'],
        "RStudio":['aces'],
        "JupyterLab":['aces'],
        "Exosphere":['jetstream2'],
        "Horizon":['jetstream2'],
        "CACAO":['jetstream2']}
    

    with db.atomic() as transaction:
        #try adding the data to the database. If there is an error, rollback the transaction
        try:
            print("Adding RPS data")
            RPS.insert_many(rps).on_conflict_replace().execute()

            #per node memory
            per_node_memory_gb = [{'rp':RPS.get(RPS.name == 'aces'),
                                'node_type':'Standard','per_node_memory_gb':512},
                            {'rp':RPS.get(RPS.name == 'anvil'),
                                'node_type':'Standard','per_node_memory_gb':256},
                            {'rp':RPS.get(RPS.name == 'anvil'), 
                                'node_type':'Large Memory', 'per_node_memory_gb':1000},
                            {'rp':RPS.get(RPS.name == 'bridges-2'),
                                'node_type':'Standard','per_node_memory_gb':256},
                            {'rp':RPS.get(RPS.name == 'bridges-2'),
                                'node_type':'Large Memory','per_node_memory_gb':512},
                            {'rp':RPS.get(RPS.name == 'darwin'),
                                'node_type':'Standard','per_node_memory_gb':512},
                            {'rp':RPS.get(RPS.name == 'darwin'),
                                'node_type':'Large Memory','per_node_memory_gb':1024},
                            {'rp':RPS.get(RPS.name == 'darwin'),
                                'node_type':'Extra-Large Memory','per_node_memory_gb':2048},
                            {'rp':RPS.get(RPS.name == 'delta'),
                                'node_type':'Standard','per_node_memory_gb':256},
                            {'rp':RPS.get(RPS.name == 'delta'),
                                'node_type':'Large Memory','per_node_memory_gb':2000},
                            {'rp':RPS.get(RPS.name == 'expanse'),
                                'node_type':'Standard','per_node_memory_gb':256},
                            {'rp':RPS.get(RPS.name == 'expanse'),
                                'node_type':'Large Memory','per_node_memory_gb':2000},
                            {'rp':RPS.get(RPS.name == 'faster'),
                                'node_type':'Standard','per_node_memory_gb':256},
                            {'rp':RPS.get(RPS.name == 'jetstream2'),
                                'node_type':'Standard','per_node_memory_gb':512},
                            {'rp':RPS.get(RPS.name == 'jetstream2'),
                                'node_type':'Large Memory','per_node_memory_gb':1024},
                            {'rp':RPS.get(RPS.name == 'ookami'),
                                'node_type':'Standard','per_node_memory_gb':32},
                            {'rp':RPS.get(RPS.name == 'kyric'),
                                'node_type':'Large Memory','per_node_memory_gb':3000},
                            {'rp':RPS.get(RPS.name == 'rockfish'),
                                'node_type':'Standard','per_node_memory_gb':192},
                            {'rp':RPS.get(RPS.name == 'rockfish'),
                                'node_type':'Large Memory','per_node_memory_gb':1500},
                            {'rp':RPS.get(RPS.name == 'stampede-2'),
                                'node_type':'Standard','per_node_memory_gb':96}]

            print("Adding ResearchFields data")
            ResearchFields.insert_many(fields).on_conflict_replace().execute()

            rpResearch = [
                {"rp": RPS.get(RPS.name == "Bridges-2"),
                "research_field": ResearchFields.get(ResearchFields.field_name == "Biology"),
                "suitability":1,
                },
                {"rp": RPS.get(RPS.name == "stampede-2"),
                "research_field": ResearchFields.get(ResearchFields.field_name == "Biology"),
                "suitability":1,
                },
                {"rp": RPS.get(RPS.name == "expanse"),
                "research_field": ResearchFields.get(ResearchFields.field_name == "Biology"),
                "suitability":1,
                },
                {"rp": RPS.get(RPS.name == "bridges-2"),
                "research_field": ResearchFields.get(ResearchFields.field_name == "Chemistry"),
                "suitability":1,
                },
                {"rp": RPS.get(RPS.name == "stampede-2"),
                "research_field": ResearchFields.get(ResearchFields.field_name == "Chemistry"),
                "suitability":1,
                },
                {"rp": RPS.get(RPS.name == "bridges-2"),
                "research_field": ResearchFields.get(ResearchFields.field_name == "Physics"),
                "suitability":1,
                },
                {"rp": RPS.get(RPS.name == "stampede-2"),
                "research_field": ResearchFields.get(ResearchFields.field_name == "Physics"),
                "suitability":1,
                },
                {"rp": RPS.get(RPS.name == "expanse"),
                "research_field": ResearchFields.get(ResearchFields.field_name == "Physics"),
                "suitability":1,
                },
                {"rp": RPS.get(RPS.name == "bridges-2"),
                "research_field": ResearchFields.get(ResearchFields.field_name == "Computer Science"),
                "suitability":1,
                },
                {"rp": RPS.get(RPS.name == "stampede-2"),
                "research_field": ResearchFields.get(ResearchFields.field_name == "Computer Science"),
                "suitability":1,
                },
                {"rp": RPS.get(RPS.name == "expanse"),
                "research_field": ResearchFields.get(ResearchFields.field_name == "Computer Science"),
                "suitability":1,
                },
                {"rp": RPS.get(RPS.name == "jetstream2"),
                "research_field": ResearchFields.get(ResearchFields.field_name == "Civil Engineering"),
                "suitability":1,
                },
                {"rp": RPS.get(RPS.name == "bridges-2"),
                "research_field": ResearchFields.get(ResearchFields.field_name == "Civil Engineering"),
                "suitability":1,
                },
                {"rp": RPS.get(RPS.name == "jetstream2"),
                "research_field": ResearchFields.get(ResearchFields.field_name == "Economics"),
                "suitability":1,
                },
                {"rp": RPS.get(RPS.name == "expanse"),
                "research_field": ResearchFields.get(ResearchFields.field_name == "Economics"),
                "suitability":1,
                },
                {"rp": RPS.get(RPS.name == "open science grid"),
                "research_field": ResearchFields.get(ResearchFields.field_name == "Linguistics"),
                "suitability":1,
                },
                {"rp": RPS.get(RPS.name == "open science grid"),
                "research_field": ResearchFields.get(ResearchFields.field_name == "History"),
                "suitability":1,
                },
                {"rp": RPS.get(RPS.name == "kyric"),
                "research_field": ResearchFields.get(ResearchFields.field_name == "Agriculture"),
                "suitability":1,
                },
                {"rp": RPS.get(RPS.name == "anvil"),
                "research_field": ResearchFields.get(ResearchFields.field_name == "Agriculture"),
                "suitability":1,
                },
                {"rp": RPS.get(RPS.name == "ookami"),
                "research_field": ResearchFields.get(ResearchFields.field_name == "Medicine"),
                "suitability":1,
                },
                {"rp": RPS.get(RPS.name == "rockfish"),
                "research_field": ResearchFields.get(ResearchFields.field_name == "Medicine"),
                "suitability":1,
                },
                {"rp": RPS.get(RPS.name == "bridges-2"),
                "research_field": ResearchFields.get(ResearchFields.field_name == "Medicine"),
                "suitability":1,
                },
            ]
            
            print("Adding RpResearchField data")
            RpResearchField.insert_many(rpResearch).on_conflict_replace().execute()

            print("Adding JobClass data")
            JobClass.insert_many(jobClass).on_conflict_replace().execute()

            rpJobClass = []
            for jobClass in list(jobClassAndRps.keys()):
                for rp in jobClassAndRps[jobClass]:
                    rpJobClass.append({"rp": RPS.get(RPS.name == rp),
                    "job_class": JobClass.get(JobClass.class_name == jobClass),
                    "suitability":1,
                    })
            print("Adding RPJobClass data")
            RpJobClass.insert_many(rpJobClass).on_conflict_replace().execute()

            print("Adding GUI data")
            GUI.insert_many(Gui).on_conflict_replace().execute()

            rpGui = []
            for gui in list(rpGUI_together.keys()):
                for rp in rpGUI_together[gui]:
                    rpGui.append({"rp": RPS.get(RPS.name == rp),
                    "gui": GUI.get(GUI.gui_name == gui),
                    "suitability":1})

            print("Adding the GUI to the RP list")
            RpGUI.insert_many(rpGui).on_conflict_replace().execute()

            print('Adding data to RpMemory')
            RpMemory.insert_many(per_node_memory_gb).on_conflict_replace().execute()

        except Exception as e:
            transaction.rollback()
            print(e)
    db.close()

def add_softwares():
    db.connect(reuse_if_open=True)
    #Accessing all of the module text files and putting them into their respective arrays
    with db.atomic() as transaction:
        try:
            modules = glob.glob('./app/softwares/*.txt')
            rpSftw = {}
            modulesAndVersions = {}
            for name in modules:
                rpName = re.search(r'([^(\\|/)]+)_(.+)', name).group(1) #get just the rp name from file path
                modulesAndVersions,mods = get_modules_and_versions(name,modulesAndVersions)
                rpSftw[rpName] = mods

            print("Adding data to Software")
            Software.insert_many(modulesAndVersions.items(), fields=[Software.software_name,Software.version]).on_conflict_replace().execute()

            #associate modules(softwares) with specific RP
            rpSoftware = []
            for item in rpSftw.items():
                rp = RPS.get(RPS.name == item[0])
                rpSoftware.extend([(rp,Software.get(Software.software_name==software)) for software in item[1]])
            print("Adding data to RpSoftware")
            RpSoftware.insert_many(rpSoftware,fields=[RpSoftware.rp,RpSoftware.software]).on_conflict_replace().execute()
        except Exception as e:
            transaction.rollback()
            print(e)
    db.close()
    
#Adds "info" to the database. This incudes a blurb about them, a link to the ACCESS resources website, and the individual documentation link
def add_info():
    db.connect(reuse_if_open=True)
    with db.atomic() as transaction:
        try:
            #info about the RP's as well as links to their websites
            rpInfo = [{'rp':RPS.get(RPS.name == 'aces'), 
                       'blurb': r"ACES (Accelerating Computing for Emerging Sciences) is funded by NSF ACSS program (Award #2112356) and provides an innovative advanced computational prototype system. ACES is especially recommended for users who need workflows that can utilize novel accelerators and/or multiple GPUs.", 
                       'link': r"https://operations.access-ci.org/node/597", 
                       'documentation': r"https://access-ci.atlassian.net/wiki/spaces/ACCESSdocumentation/pages/303923220/ACES+Texas+A+M"},
                    {'rp':RPS.get(RPS.name == 'anvil'), 
                     'blurb': r"Purdue Anvil's advanced computing capabilities are well suited to support a wide range of computational and data-intensive research spanning from traditional high-performance computing to modern artificial intelligence applications. It’s general purpose CPUs and 128 cores per node make it suitable for many types of CPU-based workloads.", 
                     'link': r"https://operations.access-ci.org/node/577", 
                     'documentation': r"https://access-ci.atlassian.net/wiki/spaces/ACCESSdocumentation/pages/283773878/Anvil+Purdue"},
                    {'rp':RPS.get(RPS.name == 'bridges-2'), 
                     'blurb': r"Bridges-2 Regular Memory (RM) nodes provide extremely powerful general-purpose computing, machine learning and data analytics, AI inferencing, and pre- and post-processing. Their x86 CPUs support an extremely broad range of applications, and jobs can request anywhere from 1 core to all 64,512 cores of the Bridges-2 RM resource.", 
                     'link': r"https://operations.access-ci.org/node/578", 
                     'documentation': r"https://access-ci.atlassian.net/wiki/spaces/ACCESSdocumentation/pages/283773971/Bridges-2+PSC"},
                    {'rp':RPS.get(RPS.name == 'darwin'), 
                     'blurb': r"The Delaware Advanced Research Workforce and Innovation Network’s (DARWIN’s) standard memory nodes provide powerful general-purpose computing, data analytics, and pre- and post-processing capabilities. The large and xlarge memory nodes enable memory-intensive applications and workflows that do not have distributed-memory implementations.", 
                     'link': r"https://operations.access-ci.org/node/595", 
                     'documentation': r"https://access-ci.atlassian.net/wiki/spaces/ACCESSdocumentation/pages/348225537/DARWIN+Delaware"},
                    {'rp':RPS.get(RPS.name == 'delta'), 
                     'blurb': r"The Delta CPU resource is designed for general purpose computation across a broad range of domains able to benefit from the scalar and multi-core performance provided by the CPUs such as appropriately scaled weather and climate, hydrodynamics, astrophysics, and engineering modeling and simulation, and other domains that have algorithms that have not yet moved to the GPU.", 
                     'link': r"https://operations.access-ci.org/node/575", 
                     'documentation': r"https://access-ci.atlassian.net/wiki/spaces/ACCESSdocumentation/pages/336822273/Delta+NCSA"},
                    {'rp':RPS.get(RPS.name == 'expanse'), 
                    'blurb': r"Expanse is designed to provide cyberfrastructure for the long tail of science, covering a diverse application base with complex workflows. The system is geared towards supporting capacity computing, optimized for quick turnaround on small/modest scale jobs. Expanse supports composable systems computing with dynamic capabilities enabled using tools such as Kubernetes and workflow software.", 
                    'link': r"https://operations.access-ci.org/node/566", 
                    'documentation': r"https://access-ci.atlassian.net/wiki/spaces/ACCESSdocumentation/pages/283774343/Expanse+SDSC"},
                    {'rp':RPS.get(RPS.name == 'faster'), 
                    'blurb': r"FASTER (Fostering Accelerated Scientific Transformations, Education and Research) is funded by the NSF MRI program (Award #2019129) and provides a composable high-performance data-analysis and computing instrument. The 180 compute nodes, including 260 NVIDIA GPUs, lend themselves to workflows that can utilize multiple GPUs.", 
                    'link': r"https://operations.access-ci.org/node/565", 
                    'documentation': r"https://access-ci.atlassian.net/wiki/spaces/ACCESSdocumentation/pages/283774421/FASTER+Texas+A+M"},
                    {'rp':RPS.get(RPS.name == 'jetstream2'), 
                    'blurb': r"Jetstream 2 is for researchers needing virtual machine services on demand as well as for software creators and researchers needing to create their own customized virtual machine environments. Additional use cases are for research-supporting infrastructure services that need to be 'always on' as well as science gateway services and for education support, providing virtual machines for students.", 
                    'link': r"https://operations.access-ci.org/node/564", 
                    'documentation': r"https://access-ci.atlassian.net/wiki/spaces/ACCESSdocumentation/pages/283774493/Jetstream2+IU"},
                    {'rp':RPS.get(RPS.name == 'ookami'), 
                    'blurb': r"Ookami provides researchers with access to the A64FX processor developed by Riken and Fujitsu for the Japanese path to exascale computing and is deployed in the, until June 2022, fastest computer in the world, Fugaku. It is the first such computer outside of Japan. Applications that are fitting within the memory requirements (27GB per node) and are well vectorized, or well auto-vectorized by the compiler. Note a node is allocated exclusively to one user. Node-sharing is not available.", 
                    'link': r"https://operations.access-ci.org/node/585", 
                    'documentation': r"https://access-ci.atlassian.net/wiki/spaces/ACCESSdocumentation/pages/283774570/OOKAMI+Stonybrook"},
                    {'rp':RPS.get(RPS.name == 'kyric'), 
                    'blurb': r"The Kentucky Research informatics Cloud (KyRIC) Large Memory nodes are increasingly needed by a wide range of ACCESS researchers, particularly researchers working with big data such as massive NLP data sets used in many research domains or the massive genomes required by computational biology and bioinformatics.", 
                    'link': r"https://operations.access-ci.org/node/568", 
                    'documentation': r"https://access-ci.atlassian.net/wiki/spaces/ACCESSdocumentation/pages/352387073/KyRIC+Kentucky"},
                    {'rp':RPS.get(RPS.name == 'rockfish'), 
                    'blurb': r"Johns Hopkins University’s flagship cluster, Rockfish, integrates high-performance and data-intensive computing while developing tools for generating, analyzing and disseminating data sets of ever-increasing size. The cluster contains compute nodes optimized for different research projects and complex, optimized workflows.", 
                    'link': r"https://operations.access-ci.org/node/569", 
                    'documentation': r"https://access-ci.atlassian.net/wiki/spaces/ACCESSdocumentation/pages/283774703/Rockfish+JHU"},
                    {'rp':RPS.get(RPS.name == 'stampede-2'), 
                    'blurb': r"Stampede2 is intended primarily for parallel applications scalable to tens of thousands of cores, as well as general purpose and throughput computing. Normal batch queues will enable users to run simulations up to 48 hours. Jobs requiring run times and more cores than allowed by the normal queues will be run in a special queue after approval of TACC staff. normal, serial and development queues are configured as well as special purpose queues.", 
                    'link': r"https://operations.access-ci.org/node/596", 
                    'documentation': r"https://access-ci.atlassian.net/wiki/spaces/ACCESSdocumentation/pages/283774765/Stampede-2+TACC"},
                    {'rp':RPS.get(RPS.name == 'ranch'), 
                    'blurb': r"TACC's High Performance Computing systems are used primarily for scientific computing with users having access to WORK, SCRATCH, and HOME file systems that are limited in size.The Ranch system serves the HPC and Vis community systems by providing a massive, high-performance file system for archival purposes.", 
                    'link': r"https://operations.access-ci.org/node/572", 
                    'documentation': r"https://access-ci.atlassian.net/wiki/spaces/ACCESSdocumentation/pages/283775021/RANCH+TACC"},
                    {'rp':RPS.get(RPS.name == 'open science grid'), 
                    'blurb': r"A virtual HTCondor pool made up of resources from the Open Science Grid (OSG). Recommended for high throughput jobs using a single core, or a small number of threads which can fit on a single compute node.", 
                    'link': r"https://operations.access-ci.org/node/583", 
                    'documentation': r"https://access-ci.atlassian.net/wiki/spaces/ACCESSdocumentation/pages/283775085/Open+Science+Grid+OSG"},
                    {'rp':RPS.get(RPS.name == 'open storage network'), 
                    'blurb': r"The Open Storage Network (OSN) is an NSF-funded cloud storage resource, geographically distributed among several pods. Cloud-style storage of project datasets for access using AWS S3-compatible tools. The minimum allocation is 10TB. Storage allocations up to 300TB may be requested via the ACCESS resource allocation process.", 
                    'link': r"https://operations.access-ci.org/node/582", 
                    'documentation': r"https://access-ci.atlassian.net/wiki/spaces/ACCESSdocumentation/pages/283775144/Open+Storage+Network+OSN"}]
            print('Adding data to RpInfo')
            RpInfo.insert_many(rpInfo,fields=[RpInfo.rp,RpInfo.blurb,RpInfo.link,RpInfo.documentation]).on_conflict_replace().execute()
            #close the database
        except:
            transaction.rollback()
            print(e)
    db.close()


if __name__ == "__main__":
    try:
        whichData = sys.argv[1]
        if whichData == 'test':
            recreate_tables()
            print("Resetting database from test data")
            reset_with_test_data()

        elif whichData == 'conf':
            tables = db.get_tables()
            if not db.get_tables():
                recreate_tables()
            print("Resetting database from conf")
            update_db_from_conf()

        else:
            print("Invalid argument for reset_database.\nPass in 'test' to use the test data or 'conf' to use the data from confluence")
        
        add_softwares()
        add_info()
        print("Database reset")

    except Exception as e:
        print(sys.exc_info()[2])
        print(e)