import time
from selenium import webdriver
import sys
from bs4 import BeautifulSoup
import re

subcodigos = {"00":"zk_comp_388","01":"zk_comp_389","02":"zk_comp_390","03":"zk_comp_391","04":"zk_comp_392","05":"zk_comp_393","06":"zk_comp_394",
            "07":"zk_comp_395","08":"zk_comp_396","09":"zk_comp_397","10":"zk_comp_398","11":"zk_comp_399","12":"zk_comp_400","13":"zk_comp_401",
            "14":"zk_comp_402","15":"zk_comp_403","16":"zk_comp_404","17":"zk_comp_405","18":"zk_comp_406","19":"zk_comp_407","20":"zk_comp_408",
            "21":"zk_comp_409","22":"zk_comp_410","38":"zk_comp_411","39":"zk_comp_412","40":"zk_comp_413","42":"zk_comp_414","44":"zk_comp_415",
            "45":"zk_comp_416","46":"zk_comp_417","47":"zk_comp_418","68":"zk_comp_419","69":"zk_comp_420","70":"zk_comp_421","74":"zk_comp_422",
            "75":"zk_comp_423","76":"zk_comp_424","77":"zk_comp_425","78":"zk_comp_426","82":"zk_comp_427","83":"zk_comp_428","85":"zk_comp_429",
            "87":"zk_comp_430","88":"zk_comp_431","89":"zk_comp_432","90":"zk_comp_433","91":"zk_comp_434","92":"zk_comp_435","93":"zk_comp_436",
            "94":"zk_comp_437","95":"zk_comp_438","96":"zk_comp_439","97":"zk_comp_440","98":"zk_comp_441","99":"zk_comp_442"}

calendario = ["/html/body/div[2]/div/table/tbody/tr[1]/td[1]","/html/body/div[2]/div/table/tbody/tr[1]/td[2]","/html/body/div[2]/div/table/tbody/tr[1]/td[3]",
              "/html/body/div[2]/div/table/tbody/tr[1]/td[4]","/html/body/div[2]/div/table/tbody/tr[1]/td[5]","/html/body/div[2]/div/table/tbody/tr[1]/td[6]",
              "/html/body/div[2]/div/table/tbody/tr[1]/td[7]","/html/body/div[2]/div/table/tbody/tr[2]/td[1]","/html/body/div[2]/div/table/tbody/tr[2]/td[2]",
              "/html/body/div[2]/div/table/tbody/tr[2]/td[3]","/html/body/div[2]/div/table/tbody/tr[2]/td[4]","/html/body/div[2]/div/table/tbody/tr[2]/td[5]",
              "/html/body/div[2]/div/table/tbody/tr[2]/td[6]","/html/body/div[2]/div/table/tbody/tr[2]/td[7]","/html/body/div[2]/div/table/tbody/tr[3]/td[1]",
              "/html/body/div[2]/div/table/tbody/tr[3]/td[2]","/html/body/div[2]/div/table/tbody/tr[3]/td[3]","/html/body/div[2]/div/table/tbody/tr[3]/td[4]",
              "/html/body/div[2]/div/table/tbody/tr[3]/td[5]","/html/body/div[2]/div/table/tbody/tr[3]/td[6]","/html/body/div[2]/div/table/tbody/tr[3]/td[7]",
              "/html/body/div[2]/div/table/tbody/tr[4]/td[1]","/html/body/div[2]/div/table/tbody/tr[4]/td[2]","/html/body/div[2]/div/table/tbody/tr[4]/td[3]",
              "/html/body/div[2]/div/table/tbody/tr[4]/td[4]","/html/body/div[2]/div/table/tbody/tr[4]/td[5]","/html/body/div[2]/div/table/tbody/tr[4]/td[6]",
              "/html/body/div[2]/div/table/tbody/tr[4]/td[7]","/html/body/div[2]/div/table/tbody/tr[5]/td[1]","/html/body/div[2]/div/table/tbody/tr[5]/td[2]",
              "/html/body/div[2]/div/table/tbody/tr[5]/td[3]","/html/body/div[2]/div/table/tbody/tr[5]/td[4]","/html/body/div[2]/div/table/tbody/tr[5]/td[5]",
              "/html/body/div[2]/div/table/tbody/tr[5]/td[6]","/html/body/div[2]/div/table/tbody/tr[5]/td[7]"]


def login_medico(usuario, password):      #LOGUEAR USUARIO Y PW
    
    driver = webdriver.Firefox(executable_path=r'/home/mmolinari/Repo/auto_pami/geckodriver')
    driver.get('https://efectoresweb.pami.org.ar/EfectoresWeb/login.isp') #NAVEGADOR
    driver.maximize_window()
    time.sleep(1)

    driver.find_element_by_xpath('//*[@id="zk_comp_16"]').send_keys(usuario) 
    driver.find_element_by_xpath('//*[@id="zk_comp_20"]').send_keys(password)
    driver.find_element_by_xpath('//*[@id="zk_comp_37"]').click() #BOTON LOGIN
    time.sleep(1)
    #driver.get('https://efectoresweb.pami.org.ar/EfectoresWeb/ambulatorio.isp') #PAGINA DE ALTA

    def completar_form(afiliado, cod_diag, fecha):

        try: #MODIFICAR CODIGO DE PRESTACION
            if len(cod_diag) == 3:
                cod_final = cod_diag+"."
            elif len(cod_diag) == 5:
                cod_final = cod_diag
            elif len(cod_diag) == 4:
                primer_parte, segunda_parte = cod_diag[0:3], cod_diag[3]
                cod_final = primer_parte + "." + segunda_parte  
        
        except ValorCodigo:
            print(cod_diag + "ES CODIGO INVALIDO")


        try: #MODIFICAR NUMERO DE AFILIADO
            if len(afiliado) == 12:
                afiliado_final = afiliado
                subcodigo_afiliado = False
            elif (len(afiliado) == 14) and afiliado[12::] == "00":
                afiliado_final = afiliado[:12]
                subcodigo_afiliado = False
            elif (len(afiliado) == 14) and afiliado[12::] != "00":
                afiliado_final, subcodigo_afiliado = afiliado[:12], afiliado[12::]

        except ValorAfiliado:
            print("Hay algun problema con el numero de afiliado")

        driver.get('https://efectoresweb.pami.org.ar/EfectoresWeb/ambulatorio.isp') #PAGINA DE ALTA
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="zk_comp_96"]').click() #BOTON ALTA
        time.sleep(0.5)


        def modif_calendario():
            
            driver.find_element_by_xpath('//*[@id="zk_comp_128-real"]').click() #CALENDARIO
            time.sleep(0.5)
            driver.find_element_by_xpath('//*[@id="_z_6-left"]').click()
            time.sleep(0.5)

            if fecha[0] == "0":
                dia_fecha = fecha[1]
            else:
                dia_fecha = fecha[:2]

            for xpath in calendario:
                if driver.find_element_by_xpath(xpath).text == dia_fecha:
                    driver.find_element_by_xpath(xpath).click()
                    break

        
        def cargar_afiliado():

            time.sleep(0.3)  
            driver.find_element_by_xpath('//*[@id="zk_comp_130-real"]').click() #ABRE FORM DE AFILIADO
            time.sleep(0.1)
            driver.find_element_by_xpath('//*[@id="zk_comp_153"]').send_keys(afiliado_final) #NUMERO DE AFILIADO
            time.sleep(0.1)
            driver.find_element_by_xpath('//*[@id="zk_comp_130-real"]').click() #ABRE FORM DE AFILIADO
            time.sleep(0.1)
            driver.find_element_by_xpath('//*[@id="zk_comp_153"]').click()
            driver.find_element_by_xpath('//*[@id="zk_comp_159"]').click() #BUSCAR
            time.sleep(0.1)       
            if subcodigo_afiliado: #EXCEPCION AFILIADOS CON SUBCODIGOS
                driver.find_element_by_xpath('//*[@id="zk_comp_386-real"]').click() #ABRE LUPITA DE PARENTEZCO
                time.sleep(0.1)
                driver.find_element_by_id(subcodigos[str(subcodigo_afiliado)]).click() #ELIJE PARENTEZCO
                time.sleep(0.1)
                driver.find_element_by_xpath('//*[@id="zk_comp_386-real"]').click() #ABRE LUPITA DE PARENTEZCO
                time.sleep(0.1)
                driver.find_element_by_xpath('//*[@id="zk_comp_130-real"]').click() #ABRE FORM DE AFILIADO DEVUELTA
                time.sleep(0.1)
                driver.find_element_by_xpath('//*[@id="zk_comp_496-cave"]').click() #CLICKEA NOMBRE Y APELLIDO
            else:
                driver.find_element_by_xpath('//*[@id="zk_comp_496-cave"]').click() #CLICKEA NOMBRE Y APELLIDO


        def profesional_actuante():

            time.sleep(0.1)
            driver.find_element_by_xpath('//*[@id="zk_comp_383-real"]').click() #PROFESIONAL ACTUANTE
            time.sleep(0.1)
            driver.find_element_by_xpath('//*[@id="zk_comp_385"]').click() #SELECCIONA PROFESIONAL
            time.sleep(0.1)


        def diagnostico(codigo):
            
            driver.find_element_by_xpath('//*[@id="zk_comp_223-real"]').click() #LUPA DE DIAGNOSTICO
            time.sleep(0.1)
            driver.find_element_by_xpath('//*[@id="zk_comp_236"]').send_keys(codigo) #RELLENA CODIGO DE DIAGNOSTICO
            time.sleep(0.1)
            driver.find_element_by_xpath('//*[@id="zk_comp_223-real"]').click() #LUPA DE DIAGNOSTICO
            time.sleep(0.1)
            driver.find_element_by_xpath('//*[@id="zk_comp_236"]').click()
            time.sleep(0.1)
            driver.find_element_by_xpath('//*[@id="zk_comp_242"]').click() #CLICKEA BUSCAR CODIGO
            time.sleep(0.1)

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            elementos = soup.find_all("div", {"class": "z-listcell-content"})
            for elemento in elementos:
                if codigo in elemento:
                    ex = str(elemento)
            m = re.findall(r"zk_comp_\d\d\d-cave", ex)
        
            time.sleep(0.1)
            driver.find_element_by_xpath('//*[@id="'+m[0]+'"]').click() #CLICKEA EL ELEMENTO DE LA LISTA
            time.sleep(0.1)
            driver.find_element_by_xpath('//*[@id="zk_comp_262"]').click() #CLICKEA AGREGAR DIAGNOSTICO
       
        
        def practicas():
  
            driver.find_element_by_xpath('//*[@id="zk_comp_280-real"]').click() #LUPA DE PRACTICAS
            time.sleep(0.1)
            driver.find_element_by_xpath('//*[@id="zk_comp_285"]').send_keys("427101") #RELLENA CODIGO DE PRACTICA
            driver.find_element_by_xpath('//*[@id="zk_comp_286"]').click() #CLICKEA LUPITA PARA BUSCAR PRACTICA
            time.sleep(0.1)
            driver.find_element_by_xpath('//*[@id="zk_comp_280-real"]').click() #LUPA DE PRACTICAS
            time.sleep(0.1)

            soup2 = BeautifulSoup(driver.page_source, 'html.parser')
            elementos2 = soup2.find_all("div", {"class": "z-listcell-content"})
            for elemento2 in elementos2:
                if "CONSULTA MEDICO DE CABECERA" in elemento2:
                    exx = str(elemento2)
            n = re.findall(r"zk_comp_\d\d\d-cave", exx)

            driver.find_element_by_xpath('//*[@id="'+n[0]+'"]').click() #CLICKEA PRIMER ELEMENTO DE LA LISTA DE PRACTICAS
            driver.find_element_by_xpath('//*[@id="zk_comp_306"]').send_keys("1") #COMPLETA EL 1
            driver.find_element_by_xpath('//*[@id="zk_comp_308-real"]').send_keys("AFILIADO PROPIO") #SELECCIONA AFILIADO PROPIO
            driver.find_element_by_xpath('//*[@id="zk_comp_313"]').click() #AGREGA PRACTICA
            time.sleep(0.1) 

        modif_calendario()
        cargar_afiliado()
        profesional_actuante()
        diagnostico(cod_final)
        practicas()

        ######## driver.find_element_by_xpath(zk_comp_317).click() #ENVIA FORMULARIO COMPLETO
        time.sleep(2) 
        # AUTOMATICAMENTE REDIRECCIONA PARA CREAR NUEVO FORMULARIO

    with open("/home/mmolinari/Repo/auto_pami/pacientes_csvs/pacientes" + credenciales[0] + ".csv", "r+") as file2:
            for data_paciente in file2:
                data = data_paciente.split(",")              
                completar_form(data[0], data[1], data[2])
            time.sleep(5)
            print(f"Finalizada la carga de {credenciales[0]}")
            #driver.close()


if __name__ == "__main__":

    with open("/home/mmolinari/Repo/auto_pami/medicos.csv", "+r") as file:
        for medico in file:
            credenciales = medico.split(",")
            print(f"Comienza carga de {credenciales[0]}")
            login_medico(credenciales[0], credenciales[1])
