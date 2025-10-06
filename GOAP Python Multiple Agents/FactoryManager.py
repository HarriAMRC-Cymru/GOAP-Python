import time
import matplotlib.pyplot as plt
from WorldState import WorldState, calculate_move_cost
from Agent import Agent
from Actions import ACTIONS

class FactoryManager:
    def __init__(self):
        self.world_state = WorldState().state
        
        # 🎯 Agent A Goal: Finished Widget
        goal_A = {'has_finished_widget': 1}
        
        # 🎯 Agent B Goal: Heavy Duty Assembly (Requires Machined Part)
        goal_B = {'has_heavy_duty_assembly': 1}
        
        self.agents = [
            Agent("Agent A", WorldState.LOC_RECEIVING, goal_A),
            Agent("Agent B", WorldState.LOC_ASSEMBLER, goal_B)
        ]
        
        # New tracking variables
        self.agent_status = {agent.name: 'IN_PROGRESS' for agent in self.agents}
        self.world_state['has_raw_steel'] = 2 # Ensure resources for both

    def _check_agent_goal(self, agent):
        """Checks if an agent's specific goal is met in the shared world state."""
        goal_met = all(self.world_state.get(k) == v for k, v in agent.goal.items())
        
        if goal_met and self.agent_status[agent.name] == 'IN_PROGRESS':
            self.agent_status[agent.name] = 'COMPLETED'
            print(f"\n🎉 GOAL ACCOMPLISHED! {agent.name} has produced the required item.")
        
        return self.agent_status[agent.name] == 'COMPLETED'
    
    def visualize_plan(self, agent_name, final_plan, agent_locations):
        """
        Plots the factory floor and the movement path of a single agent.
        """
        if not final_plan:
            print(f"Cannot visualize: {agent_name} did not complete a plan.")
            return

        # 1. Factory Setup: Define all fixed locations
        loc_map = {
            'Receiving': WorldState.LOC_RECEIVING,
            'Cutter': WorldState.LOC_CUTTER,
            'Assembler': WorldState.LOC_ASSEMBLER,
            'Press': WorldState.LOC_PRESS
        }
        loc_names = list(loc_map.keys())
        X = [p[0] for p in loc_map.values()]
        Y = [p[1] for p in loc_map.values()]

        fig, ax = plt.subplots(figsize=(10, 6))

        # 2. Plot all fixed locations
        ax.scatter(X, Y, color='blue', s=100, zorder=5) # Plot locations
        
        # Label locations
        for i, name in enumerate(loc_names):
            ax.annotate(name, (X[i] + 0.5, Y[i]), fontsize=9)

        # 3. Plot Agent Path
        path_x = [p[0] for p in agent_locations]
        path_y = [p[1] for p in agent_locations]
        
        # Draw the path lines
        ax.plot(path_x, path_y, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label=f'{agent_name} Path')
        
        # Plot markers at each stop
        ax.scatter(path_x, path_y, color='red', s=50, zorder=4) 

        # 4. Final Touches
        ax.set_title(f'GOAP Agent Movement: {agent_name} (Goal: {final_plan[-1][0]})')
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')
        ax.grid(True, linestyle=':', alpha=0.5)
        ax.legend()
        plt.show()

    def run_simulation(self, max_steps=50):
        """
        Runs the turn-based simulation, processing each agent's next action 
        until all goals are met or max_steps is reached.
        """
        
        # Tracking list for visualization (starts at initial position)
        agent_A_path = [self.agents[0].agent_state['agent_position']]
        agent_B_path = [self.agents[1].agent_state['agent_position']]
        
        final_plan_A = None
        final_plan_B = None
        all_goals_met = False

        print("\n--- Starting Multi-Agent Factory Simulation ---")
        
        for step in range(max_steps):
            
            # 1. Check if ALL goals are met before running the step
            all_goals_met = all(self._check_agent_goal(agent) for agent in self.agents)
            if all_goals_met:
                print(f"\n✅ ALL GOALS ACHIEVED: Both products manufactured in {step} steps.")
                break

            print(f"\n--- Step {step+1} ---")
            
            # --- 2. Process Agent A ---
            agent_A = self.agents[0]
            if not self._check_agent_goal(agent_A):
                self._process_agent(agent_A)
                
                # Update path and check for final completion
                agent_A_path.append(agent_A.agent_state['agent_position'])
                if self._check_agent_goal(agent_A) and not final_plan_A:
                    # Capture the full plan on the step the goal is achieved
                    final_plan_A = agent_A.exectued_plan
            else:
                print(f"[{agent_A.name}] Status: Goal already achieved (Completed).")

            # --- 3. Process Agent B ---
            agent_B = self.agents[1]
            if not self._check_agent_goal(agent_B):
                self._process_agent(agent_B)
                
                # Update path and check for final completion
                agent_B_path.append(agent_B.agent_state['agent_position'])
                if self._check_agent_goal(agent_B) and not final_plan_B:
                    # Capture the full plan on the step the goal is achieved
                    final_plan_B = agent_B.exectued_plan
            else:
                print(f"[{agent_B.name}] Status: Goal already achieved (Completed).")
            
            # 4. Display current overall progress
            print(f"\n[Overall Status] Agent A: {self.agent_status['Agent A']}, Agent B: {self.agent_status['Agent B']}")
        
        # 5. POST-SIMULATION VISUALIZATION
        print("\n--- Generating Visualization ---")
        if final_plan_A:
            self.visualize_plan(agent_A.name, final_plan_A, agent_A_path)
        if final_plan_B:
            self.visualize_plan(agent_B.name, final_plan_B, agent_B_path)
        
        if not all_goals_met:
            print("\n❌ Simulation ended without achieving all goals.")

    def _process_agent(self, agent):
        if not agent.plan:
            agent.update_plan(self.world_state)
            if not agent.plan:
                # If no plan is found and goal is not met, the agent is stuck.
                print(f"[{agent.name}] Status: STUCK (No possible plan found to complete goal).")
                return

        # Get the next action and attempt execution
        action_name, _ = agent.plan.pop(0)
        action = next(a for a in ACTIONS if a.name == action_name)
        
        # Attempt to execute. If it fails, force re-plan.
        agent.execute_action(action, self.world_state)
        
        # Current shared state after action
        print(f"  Shared State: Steel={self.world_state['has_raw_steel']}, Widget={self.world_state['has_finished_widget']}, Heavy={self.world_state['has_heavy_duty_assembly']}")