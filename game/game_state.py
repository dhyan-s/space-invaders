from dataclasses import dataclass
from typing import Any, List

@dataclass
class GameState:
    name: str
    obj: Any
    overlay_on: str = None # Name of the state to overlay on

class GameStateManager:
    def __init__(self) -> None:
        self.states: List[GameState] = []
        self._state: GameState = None
        
    def add_state(self, name, state, overlay_on = None): 
        if self.get_state_by_name(name) is not None:
            raise ValueError(f"State '{name}' already exists.")
        self.states.append(GameState(name, state, overlay_on))
        if len(self.states) == 1:
            self._state = self.states[0]
        
    def remove_state(self, name): 
        state = self.get_state_by_name(name)
        if state is not None: 
            raise ValueError(f"State '{name}' doesn't exist.")
        self.states.remove(state)
        
    def get_state_by_name(self, name) -> GameState:
        for state in self.states:
            if state.name == name:
                return state
        
    def get_current_state(self) -> GameState: 
        return self._state
    
    def set_current_state(self, name): 
        state = self.get_state_by_name(name)
        if state:
            self._state = state
        else:
            raise ValueError(f"State '{name}' doesn't exist.")
    
    def render(self):
        self._state.obj.render()
        