import ast
import astunparse
import os
import time
from subprocess import run, PIPE
import shutil

class DecoratorAdder(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        # This example assumes all functions are candidates for optimization.
        # You might want to add conditions to filter specific functions.
        node.decorator_list.append(ast.Name(id='jit', ctx=ast.Load()))
        return node

# Function to modify source code (add @jit decorator to all functions)
def modify_source_code(file_path):
    with open(file_path, 'r') as source:
        tree = ast.parse(source.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name != 'main':
                node.decorator_list.append(ast.Name(id='jit', ctx=ast.Load()))
    with open(file_path, 'w') as source:
        source.write(astunparse.unparse(tree))

 # Function to measure execution time
def measure_execution_time(executable):
    start = time.time()
    run(["python", executable])
    end = time.time()
    return end - start

def benchmark_code(directory, executable='main.py'):
    executable = os.path.join(directory, executable)
    return measure_execution_time(executable)

if __name__ == '__main__':
    initial_time = benchmark_code("src")  
    source_code_directory = 'src'
    optimized_directory = 'energy'
    if not os.path.exists(optimized_directory):
        os.makedirs(optimized_directory)
    for root, dirs, files in os.walk(source_code_directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as source:
                    lines = source.readlines()
                with open(file_path, 'w') as source:
                    if "main" not in file:
                        source.write("from numba import jit\n")
                    source.writelines(lines)
                shutil.copy(file_path, optimized_directory)
                if "main" in file:
                    continue
                file_path = os.path.join(optimized_directory, file)
                with open(file_path, 'r') as source:
                    tree = ast.parse(source.read())
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            shutil.copy(file_path, 'temp.py')
                            node.decorator_list.append(ast.Name(id='jit', ctx=ast.Load()))
                            with open(file_path, 'w') as source:
                                source.write(astunparse.unparse(tree))
                                post_time = benchmark_code(optimized_directory)
                            if post_time >= initial_time:
                                shutil.copy('temp.py', file_path)
    final_time = benchmark_code(optimized_directory)
    if final_time < initial_time:
        print("Success: The optimized code is faster")
        exit(0)
    else:
        print("Failure: The optimized code is not faster")
        exit(1)