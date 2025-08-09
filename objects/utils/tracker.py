from component import Printer
from engine import EngineObject, EnginePublic


class VariableTracker(EngineObject):
    def __str__(self):
        return "Tracker " + self.tag

    def __init__(self, Variables: list[str], SeparateOutput = False , tag ="", activation = True):
        super().__init__(tag, activation)

        self.printer = self.RegisterComponent(Printer())

        self.variables = Variables
        self.LastKnown = dict()
        self.Separate = SeparateOutput

    def Update(self, data: EnginePublic):
        super().Update(data)

        for var in self.variables:

            if var not in self.LastKnown.keys():
                self.printer.Print(f"Start Tracking {var}")
                self.LastKnown[var] = None
                continue


            val = data.FetchVariable(var)

            if val != self.LastKnown[var]:
                self.printer.Print(f"{var} Changed from {self.LastKnown[var]} to {val}")
                self.LastKnown[var] = val

                if self.Separate:
                    print("\n\n", "-" * 20, "\n\n")