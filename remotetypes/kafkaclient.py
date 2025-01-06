"""
kafkaclient.py
Cliente Kafka para consumir operaciones definidas en mensajes JSON,
ejecutarlas sobre objetos remotos (RDict, RList, RSet) a través de ICE,
y publicar las respuestas.
"""

import json
import configparser
import sys
from typing import Optional

# kafka-python (o confluent-kafka, ajusta según tu librería):
from kafka import KafkaConsumer, KafkaProducer

# Importa tu librería ICE y tus definiciones Slice generadas:
import Ice
import RemoteTypes as rt  # pylint: disable=import-error

def load_kafka_config(config_path: str = "../config/kafka.config") -> dict:
    """
    Carga la configuración de Kafka desde un archivo .ini.

    Returns:
        dict: Diccionario con 'bootstrap_servers', 'input_topic',
              'output_topic', 'group_id'.
    """
    parser = configparser.ConfigParser()
    parser.read(config_path)
    kafka_cfg = parser["kafka"]
    return {
        "bootstrap_servers": kafka_cfg["bootstrap_servers"],
        "input_topic": kafka_cfg["input_topic"],
        "output_topic": kafka_cfg["output_topic"],
        "group_id": kafka_cfg["group_id"]
    }

def execute_operation(factory: rt.FactoryPrx, op: dict) -> Optional[dict]:
    """
    Ejecuta una sola operación sobre un objeto remoto.

    Args:
        factory (FactoryPrx): Proxy a la factoría remota ICE.
        op (dict): Operación en formato JSON, con claves:
            - 'id' (str): Identificador único de la operación.
            - 'object_identifier' (str): Identificador del objeto remoto.
            - 'object_type' (str): "RDict", "RList" o "RSet".
            - 'operation' (str): Nombre del método a invocar.
            - 'args' (dict): Parámetros necesarios para la operación.

    Returns:
        dict or None: Un dict con la respuesta (id, status, result/error).
                      Si no se puede responder, se devuelve None.
    """
    # Validar estructura mínima
    required_keys = ["id", "object_identifier", "object_type", "operation"]
    for key in required_keys:
        if key not in op:
            # Si no tenemos 'id', no podemos responder
            if "id" in op:
                return {"id": op["id"], "status": "error", "error": "InvalidFormat"}
            return None

    # Extraer información
    op_id = op["id"]
    obj_id = op["object_identifier"]
    obj_type = op["object_type"]
    operation = op["operation"]
    args = op.get("args", {})

    # Obtener proxy del objeto remoto según tipo
    try:
        if obj_type == "RDict":
            remote_obj = rt.RDictPrx.checkedCast(factory.get(rt.TypeName.RDict, obj_id))
        elif obj_type == "RList":
            remote_obj = rt.RListPrx.checkedCast(factory.get(rt.TypeName.RList, obj_id))
        elif obj_type == "RSet":
            remote_obj = rt.RSetPrx.checkedCast(factory.get(rt.TypeName.RSet, obj_id))
        else:
            return {"id": op_id, "status": "error", "error": "OperationNotSupported"}
    except Exception:
        # Error al obtener la factoría o el objeto
        return {"id": op_id, "status": "error", "error": "FactoryError"}

    # Manejar la operación iter
    if operation == "iter":
        return {"id": op_id, "status": "error", "error": "OperationNotSupported"}

    # Ejecutar operación según tu Slice
    try:
        if obj_type == "RList":
            # Ejemplo de operaciones RList
            if operation == "append":
                remote_obj.append(args["item"])
                return {"id": op_id, "status": "ok"}
            elif operation == "pop":
                index = args.get("index", None)
                result = remote_obj.pop(index)
                return {"id": op_id, "status": "ok", "result": result}
            elif operation == "getItem":
                result = remote_obj.getItem(args["index"])
                return {"id": op_id, "status": "ok", "result": result}
            else:
                return {"id": op_id, "status": "error", "error": "OperationNotSupported"}

        elif obj_type == "RDict":
            # Ejemplo de operaciones RDict
            if operation == "setItem":
                remote_obj.setItem(args["key"], args["item"])
                return {"id": op_id, "status": "ok"}
            elif operation == "getItem":
                result = remote_obj.getItem(args["key"])
                return {"id": op_id, "status": "ok", "result": result}
            elif operation == "pop":
                result = remote_obj.pop(args["key"])
                return {"id": op_id, "status": "ok", "result": result}
            else:
                return {"id": op_id, "status": "error", "error": "OperationNotSupported"}

        elif obj_type == "RSet":
            # Ejemplo de operaciones RSet
            if operation == "add":
                remote_obj.add(args["item"])
                return {"id": op_id, "status": "ok"}
            elif operation == "remove":
                remote_obj.remove(args["item"])
                return {"id": op_id, "status": "ok"}
            elif operation == "pop":
                result = remote_obj.pop()
                return {"id": op_id, "status": "ok", "result": result}
            else:
                return {"id": op_id, "status": "error", "error": "OperationNotSupported"}

        # Por si no coinciden con nada
        return {"id": op_id, "status": "error", "error": "OperationNotSupported"}

    except rt.KeyError:
        return {"id": op_id, "status": "error", "error": "KeyError"}
    except rt.IndexError:
        return {"id": op_id, "status": "error", "error": "IndexError"}
    except Exception:
        # Cualquier otra excepción
        return {"id": op_id, "status": "error", "error": "UnexpectedError"}


def main():
    """
    Punto de entrada principal del cliente Kafka.
    1. Carga la configuración de kafka.config
    2. Inicializa Ice y obtiene el proxy de la factoría
    3. Crea un consumidor y un productor de Kafka
    4. Consume mensajes, ejecuta operaciones, envía las respuestas
    """
    # 1. Cargar config de Kafka
    kafka_cfg = load_kafka_config()

    # 2. Inicializar Ice y crear factoría
    with Ice.initialize(sys.argv) as communicator:
        try:
            factory_proxy = communicator.stringToProxy("Factory:tcp -h localhost -p 10000")
            factory = rt.FactoryPrx.checkedCast(factory_proxy)
            if not factory:
                print("No se pudo contactar con la factoría remota.")
                sys.exit(1)
        except Exception as exc:
            print(f"Error inicializando ICE o factoría: {exc}")
            sys.exit(1)

        # 3. Crear Consumer y Producer
        consumer = KafkaConsumer(
            kafka_cfg["input_topic"],
            bootstrap_servers=kafka_cfg["bootstrap_servers"],
            group_id=kafka_cfg["group_id"],
            auto_offset_reset='earliest',
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )

        producer = KafkaProducer(
            bootstrap_servers=kafka_cfg["bootstrap_servers"],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

        print(f"Consumidor escuchando en topic '{kafka_cfg['input_topic']}' y produciendo en '{kafka_cfg['output_topic']}'...")

        # 4. Bucle principal de consumo
        try:
            for msg in consumer:
                # msg.value debería ser un array JSON de operaciones
                operations = msg.value
                if not isinstance(operations, list):
                    # No es un array => no procesar
                    continue

                responses = []
                for op in operations:
                    response = execute_operation(factory, op)
                    if response:
                        responses.append(response)

                # Enviar array de respuestas, si hay, al output_topic
                if responses:
                    producer.send(kafka_cfg["output_topic"], responses)
                    producer.flush()
        except KeyboardInterrupt:
            print("Interrumpido por el usuario. Saliendo...")
        finally:
            consumer.close()
            producer.close()

if __name__ == "__main__":
    main()
