import heapq

def plan_actions(start_state_dict, goal_state, available_actions):
    
    def get_state_tuple(state_dict):
        """Converts the state dictionary into a stable, hashable tuple."""
        # The agent_position tuple is already hashable, but we sort the dict items 
        # to ensure the order is consistent regardless of dictionary implementation.
        return tuple(sorted(state_dict.items()))

    # Initial state setup
    start_state_tuple = get_state_tuple(start_state_dict)
    
    # Priority Queue: (g_cost, state_tuple, plan)
    pq = [(0, start_state_tuple, [])]
    
    # Visited states: {state_tuple: total_cost}
    visited = {start_state_tuple: 0}

    while pq:
        cost, current_state_tuple, plan = heapq.heappop(pq)
        current_state_dict = dict(current_state_tuple)

        # 1. Goal Check
        if all(current_state_dict.get(k) == v for k, v in goal_state.items()):
            return cost, plan

        # 2. Explore Actions
        for action in available_actions:
            if action.check_preconditions(current_state_dict):
                
                # 3. Calculate new state and cost
                next_state_dict = current_state_dict.copy()
                next_state_dict = action.apply_effects(next_state_dict)
                
                action_cost = action.get_cost(current_state_dict)
                new_cost = cost + action_cost
                
                next_state_tuple = get_state_tuple(next_state_dict)

                # 4. A* check (If this is a cheaper path to an already visited state)
                if next_state_tuple not in visited or new_cost < visited[next_state_tuple]:
                    visited[next_state_tuple] = new_cost
                    new_plan = plan + [(action.name, action_cost)]
                    heapq.heappush(pq, (new_cost, next_state_tuple, new_plan))

    return None, None