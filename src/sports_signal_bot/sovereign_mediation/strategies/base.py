from abc import ABC, abstractmethod

class BaseSovereignMediationStrategy(ABC):

    @abstractmethod
    def evaluate_quorum(self, evidence_refs, caveat_refs):
        pass

    @abstractmethod
    def evaluate_backplane_flow(self, backpressure_state):
        pass

    @abstractmethod
    def evaluate_mesh_projection(self, currentness_state, drift_state):
        pass

    @abstractmethod
    def evaluate_dispute(self, sovereignty_constraints, replay_state):
        pass
