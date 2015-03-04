from __future__ import print_function
import sys

# This is not required if you've installed pycparser into
# your site-packages/ with setup.py
#
sys.path.extend(['.', '..'])

from pycparser import c_parser, c_ast

def set_parent(node,parent):
    node.parent = parent
    for (attr,child_node) in node.children():
        set_parent(child_node,node)

def get_ids(node):
    #print(type(node).__name__)
    if type(node).__name__ == "ID" and type(node.parent).__name__!="FuncCall":
        yield node
    else:
        for (attr,child_node) in node.children():
            for n in get_ids(child_node):
                yield n


def siblings(node):
    siblings = []
    if(node.parent is not None):
        for (attr,child_node) in node.parent.children():
                siblings.append(child_node)
    return siblings


def get_global_decl(ast):
    globli = []
    for (attr,child_node) in ast.children():
            if(type(child_node).__name__ == "Decl"):
                globli.append(child_node)
    return globli

def get_parent_decl(node,visited):
    if type(node).__name__ == "Decl" and type(node.parent).__name__ != "FuncDef" and node not in visited:
        visited.append(node)
        yield node
    if node.parent is not None:
        for sibling in siblings(node.parent):
            yield from get_parent_decl(sibling,visited)
            

def get_func_args_decls(node):
    func_def = node
    while(func_def is not None and type(func_def).__name__ != "FuncDef"):
        func_def = func_def.parent

    args = func_def.decl.type.args
    if hasattr(args,"params"):
        return args.params
    return []

def is_global(id_node,global_variables):

    # check if an argument has the same name as this ID
    func_args_decls = get_func_args_decls(id_node)
    for decl in func_args_decls:
        if(decl.name == id_node.name and decl not in global_variables):
            return False

    # check for declarations of the same name in parent scopes
    for d in get_parent_decl(id_node,[]):
        if d.name == id_node.name and d not in global_variables:
            return False
    return True

def find_globals(ast):
    set_parent(ast,None)
    global_variables = get_global_decl(ast)

    for i in get_ids(ast):
        if is_global(i,global_variables):
            global_variables.append(i)
    return global_variables

def find_file_globals(filename):
    parser = c_parser.CParser()
    with open(filename, 'r') as content_file:
        content = content_file.read()
        ast = parser.parse(content, filename=filename)
        return find_globals(ast)


if __name__ == "__main__":
    if(len(sys.argv)>=2):
        for g in find_file_globals(sys.argv[1]):
            if type(g).__name__ == "Decl":
                t = "declaration"
            else:
                t = "usage"
            print(str(g.coord) + ":"+t+":"+g.name)