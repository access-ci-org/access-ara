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
from logic.rp_modules import get_modules_and_versions
import glob #for reading the text files
import os
import confluenceAPI

db.connect()

#Creating the variables from the api call in confluenceAPI

# api_table = confluenceAPI.table

# with db.atomic() as transaction:
#     try:
#         #Put validate data file here when Aiden makes it
#     except Exception as e: #e will be a place holder until Aiden completes the validation function
#         print(e)
#         transaction.rollback() 
tables = db.get_tables()
print(f"the tables: {tables}")

# delete all data and create blank tables
db.drop_tables([RPS,JobClass,RpJobClass,ResearchFields,RpResearchField,Software,RpSoftware,GUI,RpGUI,RpMemory])
db.create_tables([RPS,JobClass,RpJobClass,ResearchFields,RpResearchField,Software,RpSoftware,GUI,RpGUI,RpMemory])

# rps = []

# for rp_names in api_table:
#     rp_name = rp_names[]
#     scratch_tb = rp_names['scratch_tb']
#     longterm_tb = rp_names['longterm_tb']
#     graphical = rp_names['graphical']
#     parallel = rp_names['parallel']
#     virtual_machine = rp_names['virtual_machine']
#     rps.append({"name":rp_name, "scratch_tb":scratch_tb, "longterm_tb":longterm_tb, "graphical":graphical})
    
rps = [
   {"name":"ACES", "scratch_tb":1, "longterm_tb":100, "graphical":2},
   {"name":"Anvil", "scratch_tb":100, "longterm_tb":50},
    {"name":"Bridges-2", "scratch_tb":0, "longterm_tb":0, "parallel": 1, "graphical":2},
    {"name":"DARWIN", "scratch_tb":2, "longterm_tb":10, "parallel": 1, "graphical":2},
    {"name":"Delta", "scratch_tb":1.5, "longterm_tb":0.5, "parallel": 1, "graphical":2},
   {"name":"Expanse", "scratch_tb":7000, "longterm_tb":12000, "parallel": 1, "graphical":2},
   {"name":"FASTER", "scratch_tb":1, "longterm_tb":50, "graphical":2},
   {"name":"Jetstream2", "scratch_tb":0, "longterm_tb":0, "virtual_machine":2, "always_running":2},
   {"name":"OOKAMI", "scratch_tb":30, "longterm_tb":80},
   {"name":"KyRIC", "scratch_tb":10, "longterm_tb":0.5, "graphical":2},
    {"name":"Rockfish", "scratch_tb":10, "longterm_tb":100},
    {"name":"Stampede-2", "scratch_tb":0, "longterm_tb":1, "parallel": 1, "graphical":2},
   {"name":"RANCH", "scratch_tb":0, "longterm_tb":20},
    {"name":"Open Science Grid", "scratch_tb":0, "longterm_tb":0.5},
   {"name":"Open Storage Network", "scratch_tb":0, "longterm_tb":0},
   ]



print("Adding RPS data")
RPS.insert_many(rps).on_conflict_replace().execute()

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
print("Adding JobClass data")
JobClass.insert_many(jobClass).on_conflict_replace().execute()

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

rpJobClass = []
for jobClass in list(jobClassAndRps.keys()):
    for rp in jobClassAndRps[jobClass]:
        rpJobClass.append({"rp": RPS.get(RPS.name == rp),
        "job_class": JobClass.get(JobClass.class_name == jobClass),
        "suitability":1,
        })
print("Adding RPJobClass data")
RpJobClass.insert_many(rpJobClass).on_conflict_replace().execute()

Gui = [
    {"gui_name":"OpenOnDemand"},
    {"gui_name":"RStudio"},
    {"gui_name":"JupyterLab"},
    {"gui_name":"Exosphere"},
    {"gui_name":"Horizon"},
    {"gui_name":"CACAO"},
    ]

print("Adding GUI data")
GUI.insert_many(Gui).on_conflict_replace().execute()

#Types of GUI's

rpGUI_together = {
    "OpenOnDemand":['bridges-2', 'expanse', 'anvil', 'aces', 'faster'],
    "RStudio":['aces'],
    "JupyterLab":['aces'],
    "Exosphere":['jetstream2'],
    "Horizon":['jetstream2'],
    "CACAO":['jetstream2']}

rpGui = []
for gui in list(rpGUI_together.keys()):
    for rp in rpGUI_together[gui]:
        rpGui.append({"rp": RPS.get(RPS.name == rp),
        "gui": GUI.get(GUI.gui_name == gui)})

print("Adding the GUI to the RP list")
RpGUI.insert_many(rpGui).on_conflict_replace().execute()

#Accessing all of the module text files and putting them into their respective arrays

os.chdir('softwares')

modules = glob.glob('*.txt')
rpSftw = {}
modulesAndVersions = {}
for name in modules:
    rpName = name.split("_")[0]
    modulesAndVersions,mods = get_modules_and_versions(name,modulesAndVersions)
    rpSftw[rpName] = mods

print("Adding data to Software")
Software.insert_many(modulesAndVersions.items(), fields=[Software.software_name,Software.version]).on_conflict_replace().execute()

#associate modules with specific RP
rpSoftware = []
for item in rpSftw.items():
    rp = RPS.get(RPS.name == item[0])
    rpSoftware.extend([(rp,Software.get(Software.software_name==software),1) for software in item[1]])


print("Adding data to RpSoftware")
RpSoftware.insert_many(rpSoftware,fields=[RpSoftware.rp,RpSoftware.software,RpSoftware.suitability]).on_conflict_replace().execute()

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
print('Adding data to RpMemory')
RpMemory.insert_many(per_node_memory_gb).on_conflict_replace().execute()

db.close()