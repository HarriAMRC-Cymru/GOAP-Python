from WorldState import WorldState, calculate_move_cost

class Action:
    def __init__(self, name, preconditions, effects, base_cost=1, target_pos=None, cost_modifiers=None):
        # Changed 'cost' to 'base_cost' for clarity
        self.name = name
        self.preconditions = preconditions
        self.effects = effects
        self.base_cost = base_cost
        self.target_pos = target_pos
        # Modifier structure: [{'condition': {'key': value}, 'adjustment': amount}]
        self.cost_modifiers = cost_modifiers if cost_modifiers is not None else []

    def get_cost(self, world_state_dict):
        # Calculates the actual cost, applying movement costs, reductions, and penalties.
        current_cost = self.base_cost
        # 1. Apply Dynamic Movement Cost
        if self.name.startswith('Move to'):
            current_pos = world_state_dict['agent_position']
            current_cost = calculate_move_cost(current_pos, self.target_pos)
        # 2. Apply Optional Cost Modifiers (Penalties and Reductions)
        for modifier in self.cost_modifiers:
            condition_met = True
            # Check all conditions in the modifier
            for key, value in modifier['condition'].items():
                if world_state_dict.get(key) != value:
                    condition_met = False
                    break
            # If all conditions for the modifier are met, apply the adjustment
            if condition_met:
                current_cost += modifier['adjustment'] 
                # Positive adjustment increases cost (Penalty), Negative adjustment decreases cost (Reduction)
        # Ensure cost is at least 1
        return max(1, current_cost)

    def check_preconditions(self, world_state_dict):
        # Check general preconditions
        if not all(world_state_dict.get(k) == v for k, v in self.preconditions.items()):
            return False
        # Prevent moving to the same spot
        if self.name.startswith('Move to'):
            if world_state_dict['agent_position'] == self.target_pos:
                return False
        
        return True
    
    def apply_effects(self, world_state_copy):
        # Applies static effects
        world_state_copy.update(self.effects)
        
        # Dynamic Position Update
        if self.name.startswith('Move to') and self.target_pos is not None:
            world_state_copy['agent_position'] = self.target_pos
        
        return world_state_copy

# Shorthand for locations
LOC = WorldState 

# 🏭 Manufacturing Action List with Penalties
ACTIONS = [
    # --- MOVEMENT ACTIONS ---
    Action(name='Move to Receiving', base_cost=1, preconditions={}, effects={}, target_pos=LOC.LOC_RECEIVING),
    
    Action(name='Move to Cutter', base_cost=1, preconditions={}, effects={}, target_pos=LOC.LOC_CUTTER,
           cost_modifiers=[
               {
                   'condition': {'has_raw_steel': True}, 
                   'adjustment': 5 # ➕ PENALTY: Moving steel is slow and tiring
               }
           ]),
    
    Action(name='Move to Assembler', base_cost=1, preconditions={}, effects={}, target_pos=LOC.LOC_ASSEMBLER,
           cost_modifiers=[
               {
                   'condition': {'has_raw_steel': True}, 
                   'adjustment': 5 # ➕ PENALTY: Still penalized for carrying raw steel
               }
           ]),
           
    Action(name='Move to Tool Rack', base_cost=1, preconditions={}, effects={}, target_pos=LOC.LOC_TOOL_RACK),
    
    # --- SETUP ACTIONS ---
    Action(
        name='Set Cutter to Optimal', # New Action: Agent can improve machine state
        preconditions={'agent_position': LOC.LOC_CUTTER, 'cutter_status': 'Suboptimal'},
        effects={'cutter_status': 'Optimal'},
        base_cost=3
    ),

    # --- ACQUIRE TOOL AND MATERIAL ACTIONS (Unchanged) ---
    Action(name='Fetch Cutting Tool', preconditions={'agent_position': LOC.LOC_TOOL_RACK, 'has_cutting_tool': False}, effects={'has_cutting_tool': True}, base_cost=1),
    Action(name='Fetch Raw Steel', preconditions={'agent_position': LOC.LOC_RECEIVING, 'has_raw_steel': False}, effects={'has_raw_steel': True}, base_cost=15),

    # --- INTERMEDIATE PROCESS ACTION (Cutter) ---
    Action(
        name='Cut Raw Material', 
        preconditions={'agent_position': LOC.LOC_CUTTER, 'has_raw_steel': True, 'has_cut_plate': False},
        effects={'has_raw_steel': False, 'has_cut_plate': True}, 
        base_cost=20, 
        cost_modifiers=[
            {
                'condition': {'has_cutting_tool': True}, 
                'adjustment': -15 # ➖ REDUCTION: Tool provides a large cost saving
            },
            {
                'condition': {'cutter_status': 'Suboptimal'}, 
                'adjustment': 10 # ➕ PENALTY: Cutting with a sub-optimal machine increases processing time
            }
        ]
    ),

    # --- FINAL PROCESS ACTION (Assembler) ---
    Action(
        name='Assemble Part', 
        preconditions={'agent_position': LOC.LOC_ASSEMBLER, 'has_cut_plate': True, 'has_finished_widget': False},
        effects={'has_cut_plate': False, 'has_finished_widget': True, 'has_cutting_tool': False}, 
        base_cost=8 
    )
]