import time
from selenium import webdriver
import sys
from bs4 import BeautifulSoup
import re
from selenium.webdriver.chrome.service import Service

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


def cargar_medico(usuario, password):      #LOGUEAR USUARIO Y PW
    
    #s = Service('geckodriver')
    driver = webdriver.Chrome(executable_path= "C:/Users/Alejo/Documents/Pami/auto_pami/chromedriver.exe")
    driver.get('https://efectoresweb.pami.org.ar/EfectoresWeb/login.isp') #NAVEGADOR
    driver.maximize_window()

    driver.find_element_by_xpath('//*[@id="zk_comp_16"]').send_keys(usuario) 
    driver.find_element_by_xpath('//*[@id="zk_comp_20"]').send_keys(password)
    driver.find_element_by_xpath('//*[@id="zk_comp_37"]').click() #BOTON LOGIN
    time.sleep(1)
    driver.get('https://efectoresweb.pami.org.ar/EfectoresWeb/ambulatorio.isp') #PAGINA DE ALTA
    time.sleep(0.5)

    def completar_form(afiliado, cod_diag, fecha):   

        time.sleep(1)
        driver.get('https://efectoresweb.pami.org.ar/EfectoresWeb/ambulatorio.isp') #PAGINA DE ALTA
        time.sleep(0.5)
        driver.find_element_by_xpath('//*[@id="zk_comp_96"]').click() #BOTON ALTA
        time.sleep(0.5)


                            ################### CAMBIAR SEGUN MES, SI ES ACTUAL O SIGUIENTE ####################
        def modif_calendario():
            
            driver.find_element_by_xpath('//*[@id="zk_comp_128-real"]').click() #CALENDARIO
            time.sleep(0.2)
            #driver.find_element_by_xpath('//*[@id="_z_6-left"]').click() 
            #time.sleep(0.2)

            if fecha[0] == "0":
                dia_fecha = fecha[1]
            else:
                dia_fecha = fecha[:2]

            for xpath in calendario:
                if driver.find_element_by_xpath(xpath).text == dia_fecha:
                    driver.find_element_by_xpath(xpath).click()
                    break

        
        def cargar_afiliado():

            try: #MODIFICAR NUMERO DE AFILIADO
                if (len(afiliado) == 14) and afiliado[12::] == "00":
                    afiliado_final, subcodigo_afiliado = afiliado[:12], "00 "
                elif (len(afiliado) == 14) and afiliado[12::] != "00":
                    afiliado_final, subcodigo_afiliado = afiliado[:12], afiliado[12::]+" "
                elif (len(afiliado) == 13) and afiliado[11::] == "00":
                    afiliado_final, subcodigo_afiliado = afiliado[:11], "00 "
                elif (len(afiliado) == 13) and afiliado[11::] != "00":
                    afiliado_final, subcodigo_afiliado = afiliado[:11], afiliado[11::]+" "
            except ValorAfiliado:
                print("Hay algun problema con el numero de afiliado")

            time.sleep(0.2)  
            driver.find_element_by_xpath('//*[@id="zk_comp_130-real"]').click() #ABRE FORM DE AFILIADO
            time.sleep(0.2)
            driver.find_element_by_xpath('//*[@id="zk_comp_153"]').send_keys(afiliado_final) #NUMERO DE AFILIADO
            time.sleep(0.2)
            driver.find_element_by_xpath('//*[@id="zk_comp_130-real"]').click() #ABRE FORM DE AFILIADO
            time.sleep(0.2)
            driver.find_element_by_xpath('//*[@id="zk_comp_153"]').click()
            driver.find_element_by_xpath('//*[@id="zk_comp_159"]').click() #BUSCAR     
            time.sleep(1)

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            htmlAfiliados = soup.find_all("div", {"class": "z-listcell-content"})
            for elmtAfiliado in htmlAfiliados:
                if subcodigo_afiliado in str(elmtAfiliado):
                    varAfiliado = str(elmtAfiliado)
            afil = re.findall(r"zk_comp_\d\d\d-cave", varAfiliado)

            time.sleep(0.5)
            driver.find_element_by_xpath('//*[@id="'+afil[0]+'"]').click() #CLICKEA NOMBRE Y APELLIDO


        def profesional_actuante():

            time.sleep(0.2)
            driver.find_element_by_xpath('//*[@id="zk_comp_383-real"]').click() #PROFESIONAL ACTUANTE
            time.sleep(0.2)
            driver.find_element_by_xpath('//*[@id="zk_comp_385"]').click() #SELECCIONA PROFESIONAL
            time.sleep(0.2)


        def diagnostico():
            
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

            driver.find_element_by_xpath('//*[@id="zk_comp_223-real"]').click() #LUPA DE DIAGNOSTICO
            time.sleep(0.2)
            driver.find_element_by_xpath('//*[@id="zk_comp_236"]').send_keys(cod_final) #RELLENA CODIGO DE DIAGNOSTICO
            time.sleep(0.2)
            driver.find_element_by_xpath('//*[@id="zk_comp_223-real"]').click() #LUPA DE DIAGNOSTICO
            time.sleep(0.2)
            driver.find_element_by_xpath('//*[@id="zk_comp_236"]').click()
            time.sleep(0.5)
            driver.find_element_by_xpath('//*[@id="zk_comp_242"]').click() #CLICKEA BUSCAR CODIGO
            time.sleep(1)

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            htmlDiagnosticos = soup.find_all("div", {"class": "z-listcell-content"})
            for elmtDiagnostico in htmlDiagnosticos:
                if cod_final in str(elmtDiagnostico):
                    varDiagnostico = str(elmtDiagnostico)
                    break
            diag = re.findall(r"zk_comp_\d\d\d-cave", varDiagnostico)
        
            time.sleep(0.5)
            driver.find_element_by_xpath('//*[@id="'+diag[0]+'"]').click() #CLICKEA EL ELEMENTO DE LA LISTA
            time.sleep(0.2)
            driver.find_element_by_xpath('//*[@id="zk_comp_262"]').click() #CLICKEA AGREGAR DIAGNOSTICO
       
        
        def practicas():
  
            driver.find_element_by_xpath('//*[@id="zk_comp_280-real"]').click() #LUPA DE PRACTICAS
            time.sleep(0.2)
            driver.find_element_by_xpath('//*[@id="zk_comp_285"]').send_keys("427101") #RELLENA CODIGO DE PRACTICA
            driver.find_element_by_xpath('//*[@id="zk_comp_286"]').click() #CLICKEA LUPITA PARA BUSCAR PRACTICA
            time.sleep(0.2)
            driver.find_element_by_xpath('//*[@id="zk_comp_280-real"]').click() #LUPA DE PRACTICAS
            time.sleep(0.2)

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            htmlPracticas = soup.find_all("div", {"class": "z-listcell-content"})
            for elmtPracticas in htmlPracticas:
                if "CONSULTA MEDICO DE CABECERA" in elmtPracticas:
                    varPracticas = str(elmtPracticas)
            pract = re.findall(r"zk_comp_\d\d\d-cave", varPracticas)

            driver.find_element_by_xpath('//*[@id="'+pract[0]+'"]').click() #CLICKEA PRIMER ELEMENTO DE LA LISTA DE PRACTICAS
            driver.find_element_by_xpath('//*[@id="zk_comp_306"]').send_keys("1") #COMPLETA EL 1
            driver.find_element_by_xpath('//*[@id="zk_comp_308-real"]').send_keys("AFILIADO PROPIO") #SELECCIONA AFILIADO PROPIO
            driver.find_element_by_xpath('//*[@id="zk_comp_313"]').click() #AGREGA PRACTICA
            time.sleep(0.2) 

        modif_calendario()
        cargar_afiliado()
        profesional_actuante()
        diagnostico()
        practicas()
        time.sleep(0.2)
        driver.find_element_by_xpath('//*[@id="zk_comp_317"]').click() #ENVIA FORMULARIO COMPLETO
        time.sleep(0.3)

    with open("C:/Users/Alejo/Documents/Pami/auto_pami/pacientes_csvs/pacientes" + credenciales[0] + ".csv", "r+") as pacientes:
            for paciente in pacientes:
                data = paciente.split(",") 
                with open("C:/Users/Alejo/Documents/Pami/auto_pami/carga" + credenciales[0] + ".csv", "r+") as log:
                    if data[0] not in log.read():
                        try:
                            completar_form(data[0], data[1], data[2])
                            print(f"{data[0]} cargado")
                            log.write(f"{data[0]}\n")

                        except UnboundLocalError:
                            print(f"UnboundLocalError con {data[0]}")
                            log.write(f"{data[0]} ERROR \n")
                    else:
                        print(f"{data[0]} cargado previamente")
                    time.sleep(1.5)
            #driver.close()


if __name__ == "__main__":
    with open("C:/Users/Alejo/Documents/Pami/auto_pami/medicos.csv", "+r") as file:
        for medico in file:
            credenciales = medico.split(",")
            print(f"Comienza carga de {credenciales[0]}")
            cargar_medico(credenciales[0], credenciales[1])
