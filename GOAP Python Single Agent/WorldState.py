class WorldState:
    # Fixed locations on the factory floor (2D grid coordinates)
    LOC_RECEIVING = (0, 0)      # Where raw material is stored
    LOC_CUTTER = (10, 5)        # Machine 1: Processes raw material
    LOC_ASSEMBLER = (5, 0)      # Machine 2: Finishes the part
    LOC_TOOL_RACK = (2, 8)      # Where the Cutting Tool is stored
    
    def __init__(self, agent_pos=LOC_RECEIVING):
        self.state = {
            'has_raw_steel': False,     # Inventory
            'has_cut_plate': False,     # Inventory (Intermediate Product)
            'has_finished_widget': False, # Inventory (Final Product)
            'has_cutting_tool': False,  # Inventory (Tool)
            'cutter_status': 'Idle',    # Machine State
            'agent_position': agent_pos  # Agent's (x, y) coordinates
        }

# Helper function for cost remains the same
def calculate_move_cost(start_pos, end_pos):
    dx = abs(end_pos[0] - start_pos[0])
    dy = abs(end_pos[1] - start_pos[1])
    return dx + dy