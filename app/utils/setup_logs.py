import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,  # Define o nível de log
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Formato das mensagens de log
        datefmt='%Y-%m-%d %H:%M:%S',  # Formato da data/hora
        handlers=[
            logging.StreamHandler(),  # Envia logs para o console            
        ]
    )
    logging.info("Setup logging complete")