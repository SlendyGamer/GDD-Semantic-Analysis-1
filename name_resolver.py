from __future__ import annotations

from ast_nodes import (
    Assignment,
    BinaryExpr,
    Block,
    CallExpr,
    CallStmt,
    Expr,
    FunctionDecl,
    IdentifierExpr,
    IfStmt,
    IntLiteral,
    BoolLiteral,
    Node,
    Parameter,
    PrintStmt,
    Program,
    ReturnStmt,
    Stmt,
    StringLiteral,
    TypeName,
    UnaryExpr,
    VarDecl,
    WhileStmt,
)
from semantic_errors import (
    SemanticDiagnostic,
    SemanticError,
    SemanticErrorKind,
)
from symbols import FunctionSymbol, Scope, Symbol, SymbolKind

class NameResolver:
    def __init__(self) -> None:
        self.diagnostics: list[SemanticDiagnostic] = []
        self.functions: dict[str, FunctionSymbol] = {}
        self.current_scope: Scope | None = None
        
    def resolve(self, program: Program) -> None:
        self._collect_functions(program)
        self._check_main(program)
        for func in program.functions:
            self._resolve_function(func)
        if self.diagnostics:
            raise SemanticError(self.diagnostics)
        
    def _collect_functions(self, program: Program) -> None:
        for func in program.functions:
            functionName = func.name
            
            if functionName in self.functions:
                self._error(
                    SemanticErrorKind.DUPLICATE_FUNCTION,
                    f"Função '{functionName}' não pode estar duplicada.",
                    func.span,
                )
                continue
            
            parameterTypes = tuple(param.type for param in func.parameters)
            symbol = FunctionSymbol(
                name = functionName,
                kind = func.return_type,
                type = func.return_type,
                declaration = func,
                parameter_types = parameterTypes,
            )
            self.functions[functionName] = symbol
            func.metadata["Symbol"] = symbol
            
    def _check_main(self, program: Program) -> None:
        mainFunction = self.functions.get("main")
        if mainFunction is None:
            self._error(
                SemanticErrorKind.INVALID_MAIN,
                f"Função {mainFunction} não foi encontrada",
                program.span,
            )
            return
        
        if (mainFunction.type is not TypeName.INT or len(mainFunction.parameter_types) != 0):
            self._error(
                SemanticErrorKind.INVALID_MAIN,
                f"Função {mainFunction} deve ser do tipo int",
                mainFunction.declaration.span,
            )
            
    def _resolve_function(self, function: FunctionDecl) -> None:
        functionScope = Scope(parent = None)
        self.current_scope = functionScope
        
        for param in function.parameters:
            self._declare_parameter(param)
            
        self._resolve_block(function.body)
        
        self.current_scope = None
    
    def _declare_parameter(self, parameter: Parameter) -> None:
        assert self.current_scope is not None
        
        if parameter.name in self.current_scope.symbols:
            self._error (
                SemanticErrorKind.DUPLICATE_DECLARATION,
                f"O parâmetro {function} já foi declarado",
                parameter.span,
            )
            return
        
        symbol = Symbol (
            name = parameter.name,
            kind = SymbolKind.PARAMETER,
            type = parameter.type,
            declaration = parameter,
        )
        self.current_scope.symbols[parameter.name] = symbol
        parameter.metadata["symbol"] = symbol
        
    def _resolve_block(self, block: Block) -> None:
        newScope = Scope(parent = self.current_scope)
        previousScope = self.current_scope
        self.current_scope = newScope
        
        block.metadata["scope"] = newScope
        for stat in block.statements:
            self._resolve_statement(stat)
        
        self.current_scope = previousScope
        
    def _resolve_statement(self, stmt: Stmt) -> None:
        raise NotImplementedError("nao implementado ainda (_resolve_statement)")
    
    def _resolve_var_decl(self, decl: VarDecl) -> None:
        raise NotImplementedError("nao implementado ainda (_resolve_var_decl)")
    
    def _resolve_assignment(self, assign: Assignment) -> None:
        raise NotImplementedError("nao implementado ainda (_resolve_assignment)")
        
    def _resolve_if(self, stmt: IfStmt) -> None:
        raise NotImplementedError("nao implementado ainda (_resolve_if)")
        
    def _resolve_while(self, stmt: WhileStmt) -> None:
        raise NotImplementedError("nao implementado ainda (_resolve_while)")
        
    def _resolve_return(self, stmt: ReturnStmt) -> None:
        raise NotImplementedError("nao implementado ainda (_resolve_return)")
        
    def _resolve_print(self, stmt: PrintStmt) -> None:
        raise NotImplementedError("nao implementado ainda (_resolve_print)")
    
def resolve_names(program: Program) -> None:
    """Construa escopos, símbolos e vínculos entre usos e declarações."""

    # 1. Colete todas as assinaturas de função.
    # 2. Valide a existência e a assinatura de main.
    # 3. Percorra os corpos em ordem, criando um escopo para cada bloco.
    # 4. Anote declarações, usos e blocos na AST.
    # 5. Acumule os diagnósticos desta passagem antes de lançar SemanticError.
    raise NotImplementedError("implemente a resolução de nomes")
