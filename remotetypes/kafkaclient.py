"""
kafkaclient.py
Cliente Kafka necesario para el entregable 2, que se encarga de consumir operaciones definidas en mensajes JSON,
ejecutarlas sobre objetos remotos (RDict, RList, RSet) a través de ICE, y publicar las respuestas.
"""

import json
import configparser
import sys
from typing import Optional
from kafka import KafkaConsumer, KafkaProducer
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
    Método que ejecuta una sola operación sobre un objeto remoto.
    Si falta 'id', no podemos informar de error en el canal de salida (None). (Requisito del entregable)
    Si la operación es inválida pero sí tenemos 'id', devolvemos un dict con error.
    """
    required_keys = ["id", "object_identifier", "object_type", "operation"]
    for key in required_keys:
        if key not in op:
            if "id" in op:
                return {"id": op["id"], "status": "error", "error": "InvalidFormat"}
            return None 

    op_id = op["id"]
    obj_id = op["object_identifier"]
    obj_type = op["object_type"]
    operation = op["operation"]
    args = op.get("args", {})

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
        return {"id": op_id, "status": "error", "error": "FactoryError"}

    # Bloquea operación `iter` (Requisito entregable)
    if operation == "iter":
        return {"id": op_id, "status": "error", "error": "OperationNotSupported"}

    # Lógica de todos los tipos RList, RDict, RSet
    try:
        if obj_type == "RList":
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

        return {"id": op_id, "status": "error", "error": "OperationNotSupported"}

    except rt.KeyError:
        return {"id": op_id, "status": "error", "error": "KeyError"}
    except rt.IndexError:
        return {"id": op_id, "status": "error", "error": "IndexError"}
    except Exception:
        return {"id": op_id, "status": "error", "error": "UnexpectedError"}


def safe_json_deserialize(raw_bytes):
    """
    Función auxiliar para deserializar JSON sin que se rompa el consumidor.
    Si falla, devolvemos None.
    """
    try:
        return json.loads(raw_bytes.decode('utf-8'))
    except json.JSONDecodeError:
        return None

def main():
    """
    Punto de entrada principal del cliente Kafka.
    1. Lee configuración kafka.config
    2. Inicializa Ice y factoría
    3. Crea Consumer + Producer con group_id (varias instancias no duplicarán ops)
    4. Consume y produce respuestas (en output_topic)
    """
    
    kafka_cfg = load_kafka_config()  
    print("DEBUG: kafka_cfg =", kafka_cfg)

   
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

        
        consumer = KafkaConsumer(
            kafka_cfg["input_topic"],
            bootstrap_servers=kafka_cfg["bootstrap_servers"],
            group_id=kafka_cfg["group_id"],  
            auto_offset_reset='earliest',
            value_deserializer=lambda raw_bytes: safe_json_deserialize(raw_bytes)
        )

        producer = KafkaProducer(
            bootstrap_servers=kafka_cfg["bootstrap_servers"],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

        print(f"Consumidor escuchando topic '{kafka_cfg['input_topic']}' y "
              f"produciendo en '{kafka_cfg['output_topic']}'...")

        
        try:
            for msg in consumer:
                operations = msg.value
                if not operations:
                    print("Advertencia: mensaje inválido o vacío")
                    continue
                if not isinstance(operations, list):
                    print("Advertencia: mensaje no es un array. Se ignora.")
                    continue

                responses = []
                for op in operations:
                    resp = execute_operation(factory, op)
                    if resp:
                        responses.append(resp)
                        
                if responses:
                    producer.send(kafka_cfg["output_topic"], responses)
                    producer.flush()

        except KeyboardInterrupt:
            print("Interrumpido por el usuario.")
        finally:
            consumer.close()
            producer.close()


if __name__ == "__main__":
    main()
