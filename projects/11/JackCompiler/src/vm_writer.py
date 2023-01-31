
from JackCompiler.src import enums

class VMWriter:
    def __init__(self, output_path: str) -> None:
        self.destination = open(output_path, "w")

    def write_push(self, segment: enums.SegmentEnum, index: int) -> None:
        self.destination.write(f"push {segment.lower()} {index}\n")

    def write_pop(self, segment: enums.SegmentEnum, index: int) -> None:
        self.destination.write(f"pop {segment.lower()} {index}\n")

    def write_arithmetic(self, command: enums.ArithmentCommandEnum) -> None:
        self.destination.write(f"{command.lower()}\n")

    def write_label(self, label: str) -> None:
        self.destination.write(f"label {label}\n")

    def write_goto(self, label: str) -> None:
        self.destination.write(f"goto {label}\n")

    def write_if(self, label: str) -> None:
        self.destination.write(f"if-goto {label}\n")

    def write_call(self, name: str, n_args: int) -> None:
        self.destination.write(f"call {name} {n_args}\n")

    def write_function(self, name: str, n_vars: int) -> None:
        """Hard to tell from the book whether we're intended to do the
        require pops and pushes here, or if the compilation engine should
        handle that. Will be obvious when looking at the final output though"""
        self.destination.write(f"function {name} {n_vars}\n")

    def write_return(self) -> None:
        self.destination.write("return\n")

    def close(self) -> None:
        self.destination.close()
