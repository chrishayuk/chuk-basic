from .ast_node import ASTNode

class Variable:
    def __init__(self, name, indices=None):
        self.name = name
        self.indices = indices if indices is not None else []

    def __str__(self):
        if self.indices:
            # Assuming indices is a list of expressions, join their string representations
            indices_str = ", ".join(str(index) for index in self.indices)
            return f"{self.name}({indices_str})"
        return self.name

    def to_dict(self):
        return {
            "type": "Variable",
            "name": self.name,
            "indices": [index.to_dict() for index in self.indices] if self.indices else None
        }