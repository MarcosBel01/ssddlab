# Práctica de Sistemas Distribuidos 2024/2025

Este proyecto implementa una solución distribuida usando Ice en Python. Contiene ejemplos de RDict, RList y RSet, así como un sistema de iteradores para probar los requisitos definidos.

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

## 2. Instalar dependecias y compilar archivos ice

Para instalar las dependecias del proyecto: 

pip install -r requirements.txt

Para compilar los archivos ice:

slice2py src/remotetypes.ice



## 3. Ejecución del proyecto

Para iniciar el servidor, debes situarte en la raíz del proyecto y ejecutar:
(Sustituyendo mi ruta por la de tu caso)

python remotetypes/server.py --Ice.Config=/home/marcos/Escritorio/Universidad/Dist/venv/ssdd-remote-types/config/remotetypes.config

Normalmente con compilar el server.py debería ir, pero en mi caso, no me ha sido posible de otra forma que con este comando.

Para iniciar el cliente (El cual prueba todos los requisitos) se hace con la siguiente instrucción:

python3 client.py

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

Hay una carpeta .data con todos los .json generados mediante las pruebas, asegurando la persistencia.
Y también una carpeta tests donde intenté probar los requisitos pero tras varios días de fallos, abandoné esta opción por probar un cliente dedicado para ello.

## 5. Notas adicionales

Puedes ajustar el puerto y el host del servidor editando el archivo server.py o el cliente client.py. Por defecto, el servidor escucha en localhost:10000.

Como ya he comentado antes, el cliente está diseñado para probar automáticamente todos los requisitos definidos en la práctica. Los resultados se muestran en la consola, indicando si cada requisito fue cumplido.

## 6. Autor

Marcos Isabel Lumbreras

Correo UCLM: marcos.isabel@alu.uclm.es
