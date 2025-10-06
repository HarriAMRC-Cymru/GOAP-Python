from WorldState import WorldState
from Planner import plan_actions
from Actions import ACTIONS

# Initialize
initial_state_obj = WorldState()
initial_state_dict = initial_state_obj.state
goal = {'has_finished_widget': True}

print(f"--- GOAP Planning for 2D Environment ---")
print(f"Agent Start Position: {initial_state_dict['agent_position']}")
print(f"Goal: {goal}")

# The planning step
total_cost, plan_with_costs = plan_actions(initial_state_dict, goal, ACTIONS)

# --- Execution ---
if plan_with_costs:
    print(f"\n✅ Plan Found! (Total Cost: {total_cost})")
    print("---------------------------------------")
    
    current_state = initial_state_dict.copy()
    
    for i, (action_name, cost) in enumerate(plan_with_costs):
        action = next(a for a in ACTIONS if a.name == action_name)
        
        # Apply effects and update the state for the next step
        current_state = action.apply_effects(current_state)
        
        # Display the result
        print(f"  Step {i+1} (Cost: {cost}): {action_name}")
        print(f"    -> State: Pos={current_state['agent_position']}, Raw={current_state['has_raw_steel']}, Cut={current_state['has_cut_plate']}, Finished={current_state['has_finished_widget']}")

    print("---------------------------------------")
    print("Final State satisfies Goal:", 
          all(current_state.get(k) == v for k, v in goal.items()))

else:
    print("\n❌ No plan could be found to satisfy the goal. Check action chains and costs.")