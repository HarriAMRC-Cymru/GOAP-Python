from WorldState import WorldState, calculate_move_cost

class Action:
    def __init__(self, name, preconditions, local_effects, shared_effects, base_cost=1, target_pos=None, cost_modifiers=None):
            self.name = name
            self.preconditions = preconditions
            self.local_effects = local_effects        # Affects agent_state_dict
            self.shared_effects = shared_effects      # Affects world_state_dict
            self.base_cost = base_cost
            self.target_pos = target_pos
            self.cost_modifiers = cost_modifiers if cost_modifiers is not None else []

    def get_cost(self, world_state_dict):
        current_cost = self.base_cost
        if self.name.startswith('Move to'):
            current_pos = world_state_dict['agent_position']
            current_cost = calculate_move_cost(current_pos, self.target_pos)
        
        for modifier in self.cost_modifiers:
            condition_met = all(world_state_dict.get(k) == v for k, v in modifier['condition'].items())
            if condition_met:
                current_cost += modifier['adjustment']
        return max(1, current_cost)

    def check_preconditions(self, world_state_dict, agent_state_dict):
        # Merge shared and local state for precondition check
        combined_state = {**world_state_dict, **agent_state_dict}
        
        if not all(combined_state.get(k) == v for k, v in self.preconditions.items()):
            return False

        if self.name.startswith('Move to'):
            if agent_state_dict['agent_position'] == self.target_pos:
                return False
        
        return True
    
    def apply_local_effects(self, agent_state_copy):
        """Applies local inventory and position changes."""
        agent_state_copy.update(self.local_effects)
        
        # Dynamic Position Update
        if self.name.startswith('Move to') and self.target_pos is not None:
            agent_state_copy['agent_position'] = self.target_pos
        
        return agent_state_copy

    def apply_shared_effects(self, world_state_copy):
        """Applies changes to shared resources."""
        world_state_copy.update(self.shared_effects)
        return world_state_copy
    
LOC = WorldState 

ACTIONS = [
    # --- MOVEMENT ACTIONS (No direct effects, only update position dynamically) ---
    Action(name='Move to Receiving', preconditions={}, local_effects={}, shared_effects={}, base_cost=1, target_pos=LOC.LOC_RECEIVING),
    Action(name='Move to Cutter', preconditions={}, local_effects={}, shared_effects={}, base_cost=1, target_pos=LOC.LOC_CUTTER),
    Action(name='Move to Assembler', preconditions={}, local_effects={}, shared_effects={}, base_cost=1, target_pos=LOC.LOC_ASSEMBLER),
    Action(name='Move to Press', preconditions={}, local_effects={}, shared_effects={}, base_cost=1, target_pos=LOC.LOC_PRESS),

    # --- RESOURCE ACQUISITION (The resource must be available and agent must not have it) ---
    Action(
        name='Fetch Raw Steel (Qty 2 -> 1)', 
        preconditions={'agent_position': LOC.LOC_RECEIVING, 'has_raw_steel': 2, 'agent_has_steel': False},
        local_effects={'agent_has_steel': True}, 
        shared_effects={'has_raw_steel': 1}, 
        base_cost=15
    ),
    Action(
        name='Fetch Raw Steel (Qty 1 -> 0)', 
        preconditions={'agent_position': LOC.LOC_RECEIVING, 'has_raw_steel': 1, 'agent_has_steel': False},
        local_effects={'agent_has_steel': True}, 
        shared_effects={'has_raw_steel': 0}, 
        base_cost=15
    ),

    # --- INTERMEDIATE PROCESSES ---
    Action(
        name='Cut Raw Material', 
        preconditions={'agent_position': LOC.LOC_CUTTER, 'agent_has_steel': True, 'agent_has_plate': False},
        local_effects={'agent_has_steel': False, 'agent_has_plate': True}, 
        shared_effects={}, 
        base_cost=5 
    ),
    Action(
        name='Use Press', 
        preconditions={'agent_position': LOC.LOC_PRESS, 'agent_has_plate': True, 'agent_has_machined_part': False},
        local_effects={'agent_has_plate': False, 'agent_has_machined_part': True}, 
        shared_effects={}, 
        base_cost=7 
    ),

    # --- FINAL ASSEMBLY ACTIONS (Consuming local parts, producing shared product) ---
    Action(
        name='Assemble Widget', 
        preconditions={'agent_position': LOC.LOC_ASSEMBLER, 'agent_has_plate': True},
        local_effects={'agent_has_plate': False}, 
        shared_effects={'has_finished_widget': 1}, 
        base_cost=8
    ),
    Action(
        name='Heavy Duty Assembly', 
        preconditions={'agent_position': LOC.LOC_ASSEMBLER, 'agent_has_machined_part': True},
        local_effects={'agent_has_machined_part': False}, 
        shared_effects={'has_heavy_duty_assembly': 1}, 
        base_cost=12
    )
]