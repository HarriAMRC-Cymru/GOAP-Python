from Planner import plan_actions
from Actions import ACTIONS

class Agent:
    def __init__(self, name, start_pos, goal):
        self.name = name
        self.plan = []
        self.goal = goal
        self.agent_state = {
            'agent_position': start_pos,
            'agent_has_steel': False,
            'agent_has_plate': False,
            'agent_has_machined_part': False,  # Local State for Agent B's item
            # ... other agent-local inventory
        }
        self.exectued_plan = []  # To track executed actions for visualization

    def update_plan(self, world_state):
        # Plans a new action sequence.
        cost, plan = plan_actions(
            world_state, 
            self.agent_state, 
            self.goal, 
            ACTIONS
        )
        self.plan = plan
        self.exectued_plan = []  # Reset executed plan on new planning
        if self.plan:
            self.exectued_plan = list(self.plan)  # Copy current plan to executed_plan
            print(f"[{self.name}] New Plan: {' -> '.join([a[0] for a in self.plan])}")
        else:
            print(f"[{self.name}] No plan found.")

    def execute_action(self, action, world_state):
            """
            Attempts to execute the given action. 
            
            Args:
                action (Action): The next action object from the agent's plan.
                world_state (dict): The current, shared global state.
                
            Returns:
                bool: True if the action executed successfully, False otherwise.
            """
            
            # 1. CONFLICT CHECK (Decentralized Execution Validation)
            # Check if the action's preconditions are STILL met against the current world state.
            # This catches if another agent has consumed a resource or changed a machine status.
            if not action.check_preconditions(world_state, self.agent_state):
                print(f"[{self.name}] ❌ Plan FAILED: Preconditions not met for {action.name}. Re-planning...")
                self.plan = None # Force the agent to calculate a new, valid plan
                return False

            # 2. APPLY SHARED EFFECTS (Update the Global World State)
            # We update the 'world_state' dictionary *in place* because it is the single source of truth.
            # We pass a copy to the action method to prevent accidental modification during calculation.
            world_state.update(action.apply_shared_effects(world_state.copy()))
            
            # 3. APPLY LOCAL EFFECTS (Update the Agent's Private State)
            # Update the agent's inventory and position.
            self.agent_state.update(action.apply_local_effects(self.agent_state.copy()))
            
            # 4. SUCCESS LOGGING
            cost = action.get_cost(self.agent_state)
            print(f"[{self.name}] Executed: {action.name}. Cost: {cost}")
            
            return True