# Práctica de Sistemas Distribuidos 2024/2025 :computer:	:nerd_face:

Este proyecto implementa una solución distribuida usando Ice en Python. En un primer momento, se crearon ejemplos de RDict, RList y RSet, así como un sistema de iteradores para probar los requisitos definidos en el Entregable 1. Ahora, en el Entregable 2, se ha integrado Apache Kafka como sistema de cola de mensajes para recibir operaciones a través de un topic configurable y responder en otro topic.

## Tabla de Contenidos
1. Requisitos del Sistema
2. Instalar Dependencias y compilar Archivos Ice
3. Ejecución del Proyecto
4. Descripción de Archivos
5. Notas adicionales
6. Autor

## 1. Requisitos del sistema

Necesitas tener instalado:

- Python 3.10 o superior
- Ice (ZeroC Ice) versión 3.7.10
- Pip (administrador de paquetes de Python)
- Docker y Docker Compose (Apache Kafka)
- kcat (Para probar kafka) *opcional

## 2. Instalar dependecias y compilar archivos ice

Para instalar las dependecias del proyecto: (Es posible que en este archivo tengas que cambiar la ruta de remotetypes)

>pip install -r requirements.txt

Para compilar los archivos ice:

>slice2py src/remotetypes.ice

Se recomienda que se haga desde un entorno virtual, ya que de esa forma he desarrollado toda la práctica:

>python -m venv venv
>source venv/bin/activate



## 3. Ejecución del proyecto

En cambio al anterior entregable el primer paso es levantar Kafka. Para ello lo primero es (Teniendo nuestro archivo docker-compose.yml) añadir un contenedor Docker:

>sudo docker-compose up -d

*Utilizar sudo, ya que nos evita quebraderos de cabeza innecesarios.

Esto iniciará Apache Kafka en **localhost:9092**

Para iniciar el servidor, debes situarte en la raíz del proyecto y ejecutar:
(Sustituyendo mi ruta por la de tu caso)

>python remotetypes/server.py --Ice.Config=/home/marcos/Escritorio/Universidad/Dist/venv/ssdd-remote-types/config/remotetypes.config

Normalmente con compilar el server.py debería ir, pero en mi caso, no me ha sido posible de otra forma que con este comando. Además si salta un error, es por el path que Python interpreta mal, para solucionarlo hay que poner el siguiente comando:
>export PYTHONPATH=$PYTHONPATH:$(pwd)

Para probar los requisitos iniciales **sin kafka** se hace con la siguiente instrucción: (Situándose en /remotetypes)

>python3 client.py

Para ejecutar el cliente Kafka del **Entregable 2**:

>python remotetypes/kafkaclient.py

**IMPORTANTE**

Puedes cambiar la configuración de kafka en el archivo kafka.config

Puedes probar las distintas operaciones con este comando:
>echo '[{"id":"op1","object_identifier":"my_list","object_type":"RList","operation":"append","args":{"item":"Hola Kafka"}}]' \
  | kcat -b localhost:9092 -P -t requests_topic

He intentado utilizar kcat, y dentro de su editor mandar el mensaje json, pero me devolvía mensaje inválido y no era capaz de que se ejecutaran correctamente las operaciones, por lo que he optado por un comando así.
Otro tipo de ejemplos para probar las operaciones:

**RList**
Append (Ejemplo anterior), pop (sin índice), pop (con índice) y getItem, respectivamente:
>echo '[{"id":"op1","object_identifier":"my_list","object_type":"RList","operation":"append","args":{"item":"Hola Kafka"}}]' \
  | kcat -b localhost:9092 -P -t requests_topic

>echo '[{"id":"op2","object_identifier":"my_list","object_type":"RList","operation":"pop"}]' \
  | kcat -b localhost:9092 -P -t requests_topic

>echo '[{"id":"op3","object_identifier":"my_list","object_type":"RList","operation":"pop","args":{"index":0}}]' \
  | kcat -b localhost:9092 -P -t requests_topic

>echo '[{"id":"op4","object_identifier":"my_list","object_type":"RList","operation":"getItem","args":{"index":0}}]' \
  | kcat -b localhost:9092 -P -t requests_topic

**RDict**
setItem, getItem y pop, respectivamente:
>echo '[{"id":"op5","object_identifier":"my_dict","object_type":"RDict","operation":"setItem","args":{"key":"foo","item":"bar"}}]' \
  | kcat -b localhost:9092 -P -t requests_topic

>echo '[{"id":"op6","object_identifier":"my_dict","object_type":"RDict","operation":"getItem","args":{"key":"foo"}}]' \
  | kcat -b localhost:9092 -P -t requests_topic

>echo '[{"id":"op7","object_identifier":"my_dict","object_type":"RDict","operation":"pop","args":{"key":"foo"}}]' \
  | kcat -b localhost:9092 -P -t requests_topic

**RSet**
add, remove y pop, respectivamente:
>echo '[{"id":"op8","object_identifier":"my_set","object_type":"RSet","operation":"add","args":{"item":"elem1"}}]' \
  | kcat -b localhost:9092 -P -t requests_topic

>echo '[{"id":"op9","object_identifier":"my_set","object_type":"RSet","operation":"remove","args":{"item":"elem1"}}]' \
  | kcat -b localhost:9092 -P -t requests_topic

>echo '[{"id":"op10","object_identifier":"my_set","object_type":"RSet","operation":"pop"}]' \
  | kcat -b localhost:9092 -P -t requests_topic



**Para consumir y ver la respuesta de cada una de las operaciones:**
>kcat -b localhost:9092 -C -t responses_topic



## 4. Descripción de archivos

src/client.py: Script principal para probar los requisitos de la práctica.

src/server.py: Servidor que expone los objetos remotos para que el cliente los utilice.

src/remotetypes.ice: Definición de los tipos remotos utilizados en el proyecto.

src/remotetypes/: Implementaciones de RDict, RList, RSet, y los iteradores.

remotelist.py: Implementación de la clase RList.

remotedict.py: Implementación de la clase RDict.

remoteset.py: Implementación de la clase RSet.

iterable.py: Implementación de la clase base para los iteradores.

requirements.txt: Lista de dependencias necesarias para el proyecto.

kafkaclient.py: Cliente Kafka para el Entregable 2. Consume operaciones de un topic y publica respuestas en otro.

kafka.config: Configuración [kafka] indicando bootstrap_servers=localhost:9092, input_topic, output_topic, group_id.

docker-compose.yml: Define contenedores Kafka/Zookeeper, crea topics requests_topic y responses_topic.

Hay una carpeta .data con todos los .json generados mediante las pruebas, asegurando la persistencia.
Y también una carpeta tests donde intenté probar los requisitos pero tras varios días de fallos, abandoné esta opción por probar un cliente dedicado para ello.

## 5. Notas adicionales

Puedes ajustar el puerto y el host del servidor editando el archivo server.py o el cliente client.py. Por defecto, el servidor escucha en localhost:10000.

Como ya he comentado antes, el cliente está diseñado para probar automáticamente todos los requisitos definidos en la práctica. Los resultados se muestran en la consola, indicando si cada requisito fue cumplido.

Para cambiar los topics o el bootstrap_servers, ajusta kafka.config y docker-compose.yml.

Puedes lanzar múltiples instancias de kafkaclient.py para demostrar que con group_id=my_consumer_group se reparte la carga y no se procesan dos veces las mismas operaciones, cumpliendo así uno de los requisitos del entregable 2.

Otra cosa que he de decir es que no he utilizado confluent-kafka, si no la biblioteca kafka-python-ng ya que no me daba diversos problemas.


## 6. Autor

Marcos Isabel Lumbreras

Correo UCLM: marcos.isabel@alu.uclm.es
