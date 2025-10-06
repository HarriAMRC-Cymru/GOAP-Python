import heapq

def plan_actions(world_state_dict, agent_state_dict, goal_state, available_actions):
    
    # 1. Capture the initial keys to use for splitting the state later
    initial_world_keys = set(world_state_dict.keys())
    initial_agent_keys = set(agent_state_dict.keys())

    def get_state_tuple(world_state, agent_state):
        """Converts the combined state into a stable, hashable tuple."""
        combined = {**world_state, **agent_state} 
        return tuple(sorted(combined.items()))

    start_state_tuple = get_state_tuple(world_state_dict, agent_state_dict)
    
    pq = [(0, start_state_tuple, [])]
    visited = {start_state_tuple: 0}

    while pq:
        cost, current_tuple, plan = heapq.heappop(pq)
        
        # 2. Convert the tuple back to a combined dictionary
        # THIS LINE is where the error happens if current_tuple is corrupted.
        current_combined = dict(current_tuple) 

        # 3. GOAL CHECK: Check against the full combined state
        # The goal_state is a dict, so .items() works here.
        if all(current_combined.get(k) == v for k, v in goal_state.items()):
            return cost, plan

        # 4. DEFENSIVE STATE SPLITTING: Use initial keys to split the combined state
        current_world = {k: current_combined[k] for k in current_combined if k in initial_world_keys}
        current_agent = {k: current_combined[k] for k in current_combined if k in initial_agent_keys}

        # 5. Explore Actions
        for action in available_actions:
            # Pass the split states to the precondition check
            if action.check_preconditions(current_world, current_agent):
                
                # Apply effects to copies of the world and agent states
                next_world = action.apply_shared_effects(current_world.copy())
                next_agent = action.apply_local_effects(current_agent.copy())
                
                action_cost = action.get_cost(current_agent)
                new_cost = cost + action_cost
                
                # Generate the next hashable tuple
                next_tuple = get_state_tuple(next_world, next_agent)

                # A* check
                if next_tuple not in visited or new_cost < visited[next_tuple]:
                    visited[next_tuple] = new_cost
                    new_plan = plan + [(action.name, action_cost)]
                    heapq.heappush(pq, (new_cost, next_tuple, new_plan))
    
    return None, None