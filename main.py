import requests as rq
from tkinter import messagebox as msg
import warnings

########### VARIÁVEIS ###########
sitename = "Manaus"
customer = "SAMSUNG"
URL_BASE = "https://man-prd.jemsms.corp.jabil.org/"
USUARIO = R"Jabil\3808777"
SENHA = "Ivdscorp@#$2025"
SITE = "Manaus"
SESSION = None
###########
def avisos():
    var_pass = """
    +++++++++++++++++++++++++++++++++++++++++++
                      PASS
    +++++++++++++++++++++++++++++++++++++++++++
                  """
    var_fail = """
    +++++++++++++++++++++++++++++++++++++++++++
                      FAIL
    +++++++++++++++++++++++++++++++++++++++++++
                  """
    return var_pass, var_fail
def getToken():
    try:
        token = None
        warnings.filterwarnings("ignore", message="Unverified HTTPS request")
        url = f"{URL_BASE}api-external-api/api/user/adsignin"
        url_parameters = {"name":USUARIO, "password": SENHA}
        r = rq.post(url, data=url_parameters, verify=False)
        if r.status_code >= 200 and r.status_code < 300:
            token = r.text.strip()
            return token
        else:
            print(F"NOK - {r.status_code}")
    except Exception as e:
        print(F"ERRO DE CONEXÃO: {e}")
###################################################
TOKEN = getToken()
###################################################
def criar_sessao():
    if not TOKEN:
        return "Token não capturado"
    try:
        if "=" in TOKEN:
            nome, valor = TOKEN.split("=", 1)
            sessao = rq.Session()
            sessao.verify = False
            sessao.cookies.set(nome, valor)
            sessao.headers.update()
            sessao.headers.update({"Cache-Control": "no-cache"})
            return sessao
    except Exception as e:
        return f"ERROR - {e}"
def criar_sessao_station(stationContext):
    if not TOKEN:
        return "Token não capturado"
    try:
        if "=" in TOKEN:
            nome, valor = TOKEN.split("=", 1)
            sessao = rq.Session()
            sessao.verify = False
            sessao.cookies.set(nome, valor)
            sessao.headers.update()
            sessao.headers.update({"Cache-Control": "no-cache"})
            sessao.headers.update({"stationcontext": stationContext})
            sessao.headers.update({"Content-Type": "application/json"})
            return sessao
    except Exception as e:
        return f"ERROR - {e}"

SESSION = criar_sessao()
def wipID(serial):
        url = f"{URL_BASE}api-external-api/api/Wips/GetWipInformationBySerialNumber"
        params = {"SerialNumber": serial, "SiteName": SITE}
        try:
            r = SESSION.get(url, params=params)
            data = r.json()
            wipid = None
            if r.status_code < 300:
                if not isinstance(data, dict):
                    for item in data:
                        wipid = item.get("WipId")
                        materialname = item.get("MaterialName")
                return wipid, materialname
            else:
                print(f"\n**** WIP INVÁLIDO! **** {r.status_code}: {r.text.split()}")
                return None, None
        except Exception as e:
            print(f"Erro durante processamento de WIP! {e}")
            return None, None
def getBomId(wipid_):
    try:
        url = f"{URL_BASE}api-external-api/api/Wips/{wipid_}/Bom"
        r = SESSION.get(url, params={"wipId":wipid_})
        data = r.json()
        bomId = None
        if isinstance(data, dict):
            for c,v in data.items():
                for c1,v1 in enumerate(v):
                    bomId = v1.get("Bom", {}).get("BomId")
            return bomId
    except Exception as e:
        print(f"ERRO DURANTE PROCESSAMENTO DE GETBOMID! {e}")
####################################################################
# ENVIAR RESULTADOS
####################################################################
def getInfoforPackout():
    try:
        url = f"{URL_BASE}/packout/api/wipPackout/container/create"
        parameters = {"containerTypeId": 4,"packingRequestId": "","wipSerialNumber": ""}
        resourcer_oprtions = f"""
{'+'*40}
[1] - SAM SMART 01 - Packout
[2] - SAM SMART 02 - Packout
[3] - SAM SMART 03 - Packout
[4] - SAM SMART 04 - Packout
{'+'*40}
        """
        def content(stationcontext):
            content = stationcontext
            sessao_content = criar_sessao_station(stationContext=content)
            request = sessao_content.post(url=url, json=parameters, verify=False)
            data = request.json()
            smgbox = None
            container = None
            if isinstance (data, dict):
                smgbox = data.get("Name")
                container = data.get("ContainerTypeName")               
                status = data.get("ContainerStatus")
            print(f'\n{"*"*15} BOX CRIADA {"*"*15}\n')
            print(f"BOX: {smgbox}")
            print(f"TIPO: {container}")
            print(f"STATUS: {status}")
            print(f"\n{"*"*40}\n")
        print(resourcer_oprtions)
        Resourcer = int(input("SELECIONE O RESOURCER PARA REALIZAR O PACKOUT >>> "))
        if Resourcer == 4:
            station_context_content = '{"routeId":25,"routeStepId":714,"resourceId":803,"resourceName":"SAM SMART 04 - Packout","routeName":"SAMSUNG SMARTPHONE A075","routeProcessTypeId":2,"routeStepName":"Packout","isPullStep":false,"isStartingStep":false,"routeStepNameId":9,"stationType":7,"routeTypeId":1,"routeType":"Production","manufacturingAreaId":48,"manufacturingAreaName":"SAMSUNG SMARTPHONE 04"}'
            content(station_context_content)
        elif Resourcer == 3:
            station_context_content = '{"routeId":25,"routeStepId":714,"resourceId":802,"resourceName":"SAM SMART 03 - Packout","routeName":"SAMSUNG SMARTPHONE A075","routeProcessTypeId":2,"routeStepName":"Packout","isPullStep":false,"isStartingStep":false,"routeStepNameId":9,"stationType":7,"routeTypeId":1,"routeType":"Production","manufacturingAreaId":47,"manufacturingAreaName":"SAMSUNG SMARTPHONE 03"}'
            content(station_context_content)
        elif Resourcer == 2:
            station_context_content = '{"routeId":25,"routeStepId":714,"resourceId":721,"resourceName":"SAM SMART 02 - Packout","routeName":"SAMSUNG SMARTPHONE A075","routeProcessTypeId":2,"routeStepName":"Packout","isPullStep":false,"isStartingStep":false,"routeStepNameId":9,"stationType":7,"routeTypeId":1,"routeType":"Production","manufacturingAreaId":42,"manufacturingAreaName":"SAMSUNG SMARTPHONE 02"}'
            content(station_context_content)
        elif Resourcer == 1:
            station_context_content = '{"routeId":25,"routeStepId":714,"resourceId":522,"resourceName":"SAM SMART 01 - Packout","routeName":"SAMSUNG SMARTPHONE A075","routeProcessTypeId":2,"routeStepName":"Packout","isPullStep":false,"isStartingStep":false,"routeStepNameId":9,"stationType":7,"routeTypeId":1,"routeType":"Production","manufacturingAreaId":29,"manufacturingAreaName":"SAMSUNG SMARTPHONE 01"}'
            content(station_context_content)
    except Exception as e:
        print(f"\nErro de processamento de informação! - {e}")
    
####################################################################
def bomStructure_128(bom_id):
    url = f"{URL_BASE}api-external-api/api/boms/{bom_id}/bomStructure"
    r = SESSION.get(url, json={"bomId":bom_id}, verify=False)
    data = r.json()
    halb_top = memory = description = None
    if isinstance(data, dict):
        halb_top = next(
            (
                item.get("ParentBomName")
                for item in data["BomHierarchy"]
                if item.get("MaterialName") == "SMS1108-000760"
            ),
            None
        )
        memory = next(
            (
                item.get("MaterialName")
                for item in data["BomHierarchy"]
                if item.get("ParentBomName") == f"{halb_top}"
            ),
            None
        )
        description = next(
            (
                item.get("MaterialDescription")
                for item in data["BomHierarchy"]
                if item.get("MaterialName") == f"{memory}"
            ),
            None
        )
        if halb_top == None:
            var_fail = avisos()[1]
            print(var_fail)
        else:
            var_pass = avisos()[0]
            print(var_pass)
            print(f"""HALB: {halb_top}
MEMORY: {memory}
DESCRIPTION: {description}\n""")                    
def bomStructure_256(bom_id):
    url = f"{URL_BASE}api-external-api/api/boms/{bom_id}/bomStructure"
    r = SESSION.get(url, params={"bomId":bom_id}, verify=False)
    data = r.json()
    aviso = "BOM DIVERGENTE"
    halb_top = None
    if isinstance(data, dict):
        halb_top = next(
            (
                item.get("ParentBomName")
                for item in data["BomHierarchy"]
                if item.get("MaterialName") == "SMS1108-000750"
            ),
            aviso
        )
    if isinstance(data, dict):
        memory = next(
            (
                item.get("MaterialName")
                for item in data["BomHierarchy"]
                if item.get("ParentBomName") == f"{halb_top}"
            ),
            aviso
        )
    if isinstance(data, dict):
        description = next(
            (
                item.get("MaterialDescription")
                for item in data["BomHierarchy"]
                if item.get("MaterialName") == f"{memory}"
            ),
            aviso
        )
    var_pass = avisos()
    print(var_pass[0])
    print(f"""HALB: {halb_top}
MEMORY: {memory}
DESCRIPTION: {description}\n""")

def choice():
    MEMORIA = int(input("""\n
+++++++++++++++++++++++++++++++++++++++++++
DEFINA A MEMORIA
                
[0] - 128Gb
[1] - 256Gb
                
+++++++++++++++++++++++++++++++++++++++++++

>>>  """))
    try:
        if MEMORIA == 0:
            serial = input("\nS/N >>> ")
            wipId_var = wipID(serial)[0]
            bomId = getBomId(wipId_var)
            getInfoforPackout()
            if bomStructure_128(bomId) == None:
                msg.showerror("ATENÇÃO", "BOM DIVERGENTE, INFORME SEU LÍDER")
        if MEMORIA == 1:
            serial = input("\nS/N >>> ")
            wipId_var = wipID(serial)[0]
            bomId = getBomId(wipId_var)
            getInfoforPackout()
            if bomStructure_256(bomId) == None:
                msg.showerror("ATENÇÃO", "BOM DIVERGENTE, INFORME SEU LÍDER")
    except Exception as e:
        print(f"ERRO DURANTE CROSS-CHECKING! {e}")
choice()