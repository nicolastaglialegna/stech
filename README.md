# stech

Aplicación que dada una determinada dirección IP de un cablemodem, se obtenga vía SNMP la información de fabricante, modelo y versión de software. Los cuales se deben almacenar en el destino dado.
## Parametros de ingreso 

* [Ip] Dirección IP del cablemodem.
* [Destination:]Donde se almacenará la información, esta puede ser:

db: Se debe almacenar el fabricante, modelo y la versión de software en la base de datos
file: Se debe almacenar el fabricante, modelo y versión de software en el file.
both: Se debe almacenar fabricante, modelo y versión de software en la base de datos y archivo.

### Condiciones solicitadas

La aplicación se ejecutará por CLI, por lo que se solicita que la IP y destino se puedan pasar como argumentos de la aplicación (Ver ejemplos más adelante). En caso de que un fabricante, modelo y versión de software ya esté almacenado en uno de los medios se tiene que mostrar por pantalla el error.

### Validaciones a considerar

* Se tiene que validar que la ip no este repetida y respete el formato IPv4
* Que el fabricante, modelo y versión de software no estén repetido en el mismo medio. En caso de utilizar destination en “both” se debería validar en ambos medios.
* El CM puede no existir en la ip dada.
* Como comunidad SNMP se asume "private" para todos los CM.


### Requerimientos no funcionales

* Se debe utilizar Python 3.4 o superior como lenguaje para desarrollar la aplicación.
* Se asume que todos los cablemodem soportan SNMP v2c
* Se debe utilizar mysql o mariadb como motor relacional.
* Se pueden utilizar todas las librerías que considere necesarias sin restricciones.

### Ejemplos de input y output

**Input**
```
python app.py 10.0.0.10 db
```

**Out**
```
Se debe almacenar la información de vendor, modelo y versión de software en la base de datos.
```

**Input**
```
python app.py 10.0.0.10 file
```

**Out**
```
Se debe almacenar la información de vendor, modelo y versión de software en un file.
```

**Input**
```
python app.py 10.0.0.10 both
```

**Out**
```
Se debe almacenar la información de vendor, modelo y versión de software en un file y base de datos.
```

### Datos adicionales

La OID SNMP sugerida para consultar los datos del cablemodem es:
* Name: sysDescr
* OID: 1.3.6.1.2.1.1.1

## Despliegue 

Crear entorno virtual, en terminal ejecutar:
```
virtualenv env -p python3
```

Instalar paquetes python:

```
sudo apt-get install python3-dev libmysqlclient-dev
```

Ingresar al entorno virtual

```
source env/bin/activate
```

Instalamos requerimientos:

```
pip install -r requirements.txt
```


Creamos imagen y levantamos el contenedor que contiene la base de datos.

```
docker build -t mysql_stech:1.0 .              

docker-compose up
```

Podemos verificar si se creo la base de datos entrando al contenedor y ejecutando:

mysql -uroot -p
_pass: stech_

show databases;


