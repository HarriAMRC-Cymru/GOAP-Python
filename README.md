# GOAP-Python
# Multi-Agent Goal-Oriented Action Planner (GOAP) for Manufacturing 🏭

This repository contains a Python implementation of a **Goal-Oriented Action Planner (GOAP)** system designed to simulate agents working collaboratively in a manufacturing environment. It features a decentralized planning model enhanced with a novel **Resource Reservation** mechanism to prevent deadlocks and conflicts over shared resources (like raw materials).

The system allows multiple agents to pursue heterogeneous goals simultaneously while dynamically finding the optimal path for each.

---

## ✨ Features

* **Multi-Agent Decentralized Planning:** Two or more independent agents (Agent A, Agent B, etc.) run their own A\* GOAP search concurrently.
* **Heterogeneous Goals:** Each agent can be assigned a unique final goal (e.g., Agent A produces a Widget, Agent B produces a Heavy-Duty Assembly).
* **Cost Modification:** Actions have dynamic costs that can be reduced or penalized based on optional world state conditions (e.g., reduced cost for using a machine in the 'Optimal' state).
* **Resource Reservation (Coordination):** Agents negotiate shared resources (Raw Steel) by reserving them in the global state, forcing other agents to re-plan immediately if a conflict occurs.
* **Simulation Visualization:** Generates a Matplotlib plot of the factory floor, illustrating the movement path and steps taken by each agent.

---

## 🚀 Getting Started

### Prerequisites

You need Python 3.8+ and the following libraries:

pip install matplotlib

## 🧠 Core Concepts: GOAP Architecture
The system is built on four main components:

1. WorldState
Defines the static coordinates of factory locations (e.g., LOC_CUTTER) and tracks shared resources and machine status (e.g., raw_steel_available).

2. Agent
Each agent has its own local state (inventory, position), a specific goal dictionary, and a planning logic (update_plan) that uses the A* search.

3. Action
Defines the verbs of the system. Each action contains:

preconditions: What must be true to run the action.

local_effects: Changes to the agent's inventory/position.

shared_effects: Changes to the global WorldState (resources, machine status).

base_cost / cost_modifiers: Allows for dynamic penalty/reduction based on state.

4. plan_actions (The Planner)
An A* forward-search algorithm that finds the lowest-cost sequence of actions to transition from the current combined state (World + Agent) to a state that satisfies the goal.

## 🔒 Resource Reservation Mechanism
The system uses placeholders and action specialization to manage shared resources like Raw Steel (raw_steel_available). This makes the system generic for any number of agents (N).

Generic Actions: The central ACTIONS list contains generic coordination steps:

Reserve Raw Steel: Sets the shared state raw_steel_reserved_by to the placeholder RESERVING_AGENT.

Fetch Reserved Raw Steel: Requires the placeholder EXECUTING_AGENT to match the current reservation.

Specialization: Before an agent runs plan_actions, the agent's logic replaces these placeholders (RESERVING_AGENT, EXECUTING_AGENT) with the agent's actual name ('Agent A', 'Agent B').

Conflict Resolution: If Agent A successfully reserves the steel, Agent B's GOAP planner will see that the precondition for its specialized Reserve Raw Steel action is failed, forcing it to find a path that avoids the reserved resource or wait until it is free.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📜 License
Distributed under the MIT License. See LICENSE for more information.

Created with the GOAP methodology, inspired by AI for game development.
