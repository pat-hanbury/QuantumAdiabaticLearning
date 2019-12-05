from visdom import Visdom
import numpy as np

class VisdomManager:
    def __init__(self, port, server):
        self.viz = self.get_viz(port=port, server=server)
        self.windows = []
        self.energy_history = []
        
    def get_viz(self, port, server):
        viz = Visdom(port=port, server=server)
        assert viz.check_connection(timeout_seconds=3), \
        'Visdom connection could be formed quickly'
        return viz
        
    def initialize_window(self, title):
        return self.viz.line(
                X=[0], Y=[0],
                opts=dict(title=title,
                         xlabel='Iteration',
                         ylabel='Energy')
                )
    
    def update_loss(self, X, Y, win):
        self.viz.line(
            X=X,
            Y=Y,
            win=win,
            name="Loss",
            update="append"
        )
        
    def new_window(self, title):
        self.windows.append(self.initialize_window(title))
        
    def update_energy_history(self, energy):
        self.energy_history.append(energy)
        self.iteration_count.append(len(self.iteration_count))
        self.update_loss(self, self.iteration_count, self.energy_history, self.windows[-1])