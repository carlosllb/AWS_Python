import os
import boto3
import json
from prettytable import PrettyTable

pregunta = "\n####################################################\n"
pregunta += "Selecciona alguna de las siguientes opciones:\n"
pregunta += "\t1. Listar configuraciones de conexion a AWS\n"
pregunta += "\t2. Configurar conexion a AWS\n"
pregunta += "\t3. Listar VPC\n"
pregunta += "\t4. Listar SG\n\n"
pregunta += "\t0. Para salir del programa\n"
pregunta += "####################################################\n"
pregunta += "> "

pregunta_perfil = "\nEscribe el nombre del perfil a utilizar?\n"
pregunta_perfil += "> "

pregunta_region = "En que region quieres que se listen la(s) VPC(s)?\n"
pregunta_region += "> "

pregunta_vpc = "De que VPC quieres ver los SG?\n"
pregunta_vpc += "> "

# FUNCION PARA LISTADO DE PERFILES AWS EN EL ORDENADOR
def listAwsProfiles():
    listAwsProfiles = os.system('aws configure list-profiles')
    #output = listAwsProfiles.read()
    return listAwsProfiles

def listAwsVpc(perfil,region):
    boto3.setup_default_session(profile_name=perfil)
    ec2 = boto3.resource('ec2', region_name=region)
    client = boto3.client('ec2')
    filters = [{'Name':'tag:Name'}]
    vpcs = list(ec2.vpcs.all())
    for vpc in vpcs:
        print(f"{vpc.id}")
    
def listAwsSg(perfil,region):
    # FOR TESTING
    perfil="carlos"
    region="eu-west-1"

    listAwsVpc(perfil,region)
    boto3.setup_default_session(profile_name=perfil)
    ec2 = boto3.resource('ec2', region_name=region)
    client = boto3.client('ec2')
    vpc = input(pregunta_vpc)

    # FOR TESTING
    vpc="vpc-25a2e243"

    groups = client.describe_security_groups(Filters=[{'Name': 'vpc-id', 'Values': [vpc]}])
    #describe_sg = json.dumps(groups, indent=1, default=str)
    describe_sg = json.loads(json.dumps(groups, indent=1, default=str))
    # print(describe_sg)
    
    # print(describe_sg["SecurityGroups"])
    #print(describe_sg["SecurityGroups"][0]["Description"])
    #print(describe_sg["SecurityGroups"][0]["IpPermissions"])

    for i in describe_sg["SecurityGroups"]:
        sg_texto = i['GroupName']
        for permisos in i['IpPermissions']:
            #print(permisos['FromPort'])
            sg_texto_from = permisos
            print(f"{sg_texto} {sg_texto_from}")
    # for valor,sg in groups.items():
    #     if valor == 'SecurityGroups':
    #         for valor in sg:
    #             # print(f"{valor['GroupName']} - {valor['IpPermissions']}")
    #             texto_sg = valor['GroupName']
    #             # print(valor['IpPermissions'])
    #             for permissions in list(valor['IpPermissions']):
    #                 for permission1,permission2 in permissions.items():
    #                     print(f"{permission1} - {permission2}")


# x = PrettyTable()
# x.field_names = ["City name", "Area", "Population", "Annual Rainfall"]
# x.add_row(["Adelaide", 1295, 1158259, 600.5])
# print(x)

# IMPRESION DE MENU Y PREGUNTAS A USUARIO
while True:
    respuesta = input(pregunta)
    if respuesta == '':
        print("Debe elegir alguno de los valores indicados")
    else:
        respuesta = int(respuesta)
    if respuesta == 0:
        break
    else:
        if respuesta == 1:
            # SE EJECUTA LA FUNCION PARA LISTAR LAS CONEXIONES CONFIGURADAS A AWS
            print("Listado de conexiones a AWS:")
            listAwsProfiles()
            print("\n")
        elif respuesta == 2:
            # SE INDICA COMO REALIZAR LA CONFIGURACION DE CONEXION A AWS
            print("Ejecuta en una linea de comando:\n")
            print("aws configure --profile nombre_profile\n")
            print("Sigue las instruciones que aparecen en pantalla\n")
        elif respuesta == 3:
            print("Perfiles disponibles:")
            listAwsProfiles()
            perfil = input(pregunta_perfil)
            region = input(pregunta_region)
            listAwsVpc(perfil,region)
        elif respuesta == 4:
            print("Perfiles disponibles:")
            listAwsProfiles()
            perfil = input(pregunta_perfil)
            region = input(pregunta_region)
            listAwsSg(perfil,region)




# USUARIOS AWS
# K:    AKIAQ5OOVDA6EGUPZ6TJ
# SK:   ojQ8TbbaRAqDs6I7wsirChAqEZ7XtjJKYvYFDEve
#
# K:    AKIAQ5OOVDA6BXA4Q3VJ  
# SK:   AWzf/x4DAvXmScN6MEJem8pWd04u1gfP/M6Yy3oj

