#==================================================================================================
#  python_scripts/toggle_bool.py
#  toggle a boolean entity state
#==================================================================================================

input_entity = data.get('entity_id')
if input_entity is None:
    logger.critical('entity_id is required')
else:
    input_state_object = hass.states.get(input_entity)
    if input_state_object is None and not data.get('allow_create'):
        logger.warning(f'Unknown entity_id: {input_entity}')
    else:
        if not input_state_object is None:
            input_state = input_state_object.state
            input_attributes_object = input_state_object.attributes.copy()
        else:
            input_attributes_object = {}

        if input_state == 'off':
            new_state = 'on'
        elif input_state == 'on':
            new_state = 'off'

        try:
            logger.info(f'Changing state of {input_entity} to {new_state}')
            hass.states.set(input_entity, new_state, input_attributes_object)
        except NameError:
            logger.warning(f'Could not determine new boolean state for entity "{input_entity}" from current state "{input_state}". Current state must be "on" or "off".')
