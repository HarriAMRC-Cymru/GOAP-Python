# Fixed locations on the factory floor (2D grid coordinates)
class WorldState:
    LOC_RECEIVING = (0, 0)
    LOC_CUTTER = (10, 5)
    LOC_ASSEMBLER = (5, 0)
    LOC_PRESS = (2, 8)
    
    def __init__(self, agent_pos=LOC_RECEIVING):
        self.state = {
            'has_raw_steel': 1,             
            'has_cut_plate': 0,             
            'has_machined_part': 0,         # Intermediate part for Agent B's goal
            'has_finished_widget': 0,
            'has_heavy_duty_assembly': 0,   # Agent B's final product
            'cutter_status': 'Optimal',
            # Note: Agent position is handled locally by the Agent class for simplicity
        }

def calculate_move_cost(start_pos, end_pos):
    """Calculates Manhattan distance as cost for movement."""
    dx = abs(end_pos[0] - start_pos[0])
    dy = abs(end_pos[1] - start_pos[1])
    return dx + dy