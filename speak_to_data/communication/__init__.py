from speak_to_data.communication import network, persistence

persist_event = persistence.persist_event
read_full_dataset = persistence.read_full_dataset

call_tapas = network.call_model_api