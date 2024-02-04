import ast
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

# 
def modify_source_code(file_path):
    with open(file_path, 'r') as file:
        source_code = file.read()

    tree = ast.parse(source_code)
    # Add the import statement at the beginning of the file
    tree.body.insert(0, ast.ImportFrom(module='numba', names=[ast.alias(name='jit', asname=None)], level=0))
    tree = DecoratorAdder().visit(tree)
    modified_code = ast.unparse(tree)

    with open(file_path, 'w') as file:
        file.write(modified_code)
 # Function to measure execution time
def measure_execution_time(executable):
    start = time.time()
    run(["python", executable])
    end = time.time()
    return end - start

def benchmark_code(executable):
    return measure_execution_time(executable)

if __name__ == '__main__':
    # Step 2: Modify source code (add @jit decorator to all functions) as a copy
    source_code_directory = 'src'
    if not os.path.exists('energy'):
        os.makedirs('energy')
    for root, dirs, files in os.walk(source_code_directory):
        for file in files:
            if file.endswith('.py'):
                shutil.copy(os.path.join(root, file), 'energy')
                modify_source_code(os.path.join('energy', file))

  # Step 1 : Measure performance before optimization
    pre_time = benchmark_code("src")
    # Step 3: Measure performance after optimization
    post_time = benchmark_code("energy")
    # Step 4: Commit changes if performance improved
    if post_time < pre_time:
        print("Success: The optimized code is faster")
        exit(0)
    else:
        print("Failure: The optimized code is not faster")
        exit(1)    