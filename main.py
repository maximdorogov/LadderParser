import re
from defines import ldr_opcodes, timer_opcodes, digi_inputs, digi_outputs, io_positions

class Op_code:
    """Representa una instruccion"""
    def __init__(self):
        self.id = None
        self.argA = None
        self.argB = None
        self.argC = None


def compile_code(code_lines, vars_dict, word_index):


    RESET_ADDR = 0  # Direccion del vector de bools donde se mapean los resets que no se dejan explicitos en timers
    RESET_POS = 4
    TR_POS  = 5

    TR_VAR_NAME = "Rem_Time"
    name_idx = 1
    rem_time_idx = word_index
    OP_CODE = 0

    compiled = []
    i = 0
    for instr in code_lines:
        if instr[OP_CODE] in timer_opcodes:
            # Agregar el caso de S_CUD
            for idx, arg in enumerate(instr):
                if arg != 'None':
                    if instr.index(arg) == OP_CODE:
                        compiled.append(ldr_opcodes[arg])
                    else:
                        compiled.append(vars_dict[arg])
                else:
                    if idx == RESET_POS:
                        compiled.append(RESET_ADDR)
                    if idx == TR_POS:
                        compiled.append(rem_time_idx)  # y agregar la variable al stack de variables
                        vars_dict[TR_VAR_NAME + str(name_idx)] = rem_time_idx
                        name_idx = name_idx + 1
                        rem_time_idx = rem_time_idx + 1
        else:
            for arg in instr:
                if instr.index(arg) == OP_CODE:
                    compiled.append(ldr_opcodes[arg])
                else:
                    compiled.append(vars_dict[arg])

    return compiled, vars_dict, rem_time_idx


def get_vars(delim, code, stop_msg):
    vars_tuple = []
    line = code.readline()

    while line:

        if line == '\n':                  # Si la linea esta vacia vuelvo a leer
            line = code.readline()
        line = re.sub('[;\s+]', '', line)
        line = re.sub('//\w+', '', line)  # Identifico y elimino comentarios

        if line == stop_msg:
            return vars_tuple

        splited = re.split(delim, line)
        if len(splited) > 1:
            vars_tuple.append(splited)
        line = code.readline()
    return


def process_line(code, stop_msg):

    delim = '[=(,]'
    line_ctr = 1
    vars_tuple = []
    line = code.readline()

    while line:
        if line == '\n':                  # Si la linea esta vacia vuelvo a leer
            line = code.readline()
            line_ctr = line_ctr + 1

        line = re.sub('[;)"\s+]', '', line)
        line = re.sub('//\w+', '', line)  # Identifico y elimino comentarios

        if line == stop_msg:
            return vars_tuple

        splited = re.split(delim, line)

        if len(splited) > 1:
            splited[0], splited[1] = splited[1], splited[0]
            vars_tuple.append(splited)
        line = code.readline()
        line_ctr = line_ctr + 1
    return


# Recibe una lista de tuplas para entradas y otra para salidas con nombres de variables de I/O mapeadas a PIN_ID
# Devuelve diccionario con nombres de variables de I/O mapeadas a direcciones de memoria

def map_io(inputs, outputs):

    io_dirs = dict()

    joined_io = outputs + inputs
    enum_io = []
    io_dirs = []
    for io in enumerate(joined_io, start=1):
        enum_io.append(io)

    for full_tuple in enum_io:
        dir, io_tuple = full_tuple
        var_name, pin_id = io_tuple
        io_dirs.append([var_name, dir])

    return dict(io_dirs)


def map_internal_variables(vars_dict, BOOL_START_ADDR):

    word_ctr = 0
    bool_ctr = BOOL_START_ADDR
    mapped_vars = dict()

    for key in vars_dict:
        if vars_dict[key] == 'BOOL':
            mapped_vars[key] =  bool_ctr
            bool_ctr = bool_ctr + 1
        else:
            if vars_dict[key] == 'WORD':
                mapped_vars[key] = word_ctr
                word_ctr = word_ctr + 1

    return mapped_vars, word_ctr


def search_tag(file, tag):
    found = False
    while not found:
        line = file.readline()
        if not line:
            break
        line = re.sub('[;\s+]', '', line)
        line = re.sub('//\w+', '', line)  # Identifico y elimino comentarios
        if line == tag:
            found = True
    return found


def main():

    io_defines = '[=]'
    internal_vars = '[:]'

    var_input_begin_tag  = "DECLAREVAR_INPUT"
    var_input_end_tag    = "ENDVAR_INPUT"
    var_output_begin_tag = "DECLAREVAR_OUT"
    var_output_end_tag   = "ENDVAR_OUT"
    inter_vars_begin_tag = "DECLAREVAR_TEMP"
    inter_vars_end_tag   = "ENDVAR_TEMP"
    program_begin_tag    = "BEGINPROCESS"
    program_end_tag      = "ENDPROCESS"

    code = open('ladder_completo.ldr', "r")

    if search_tag(code, var_input_begin_tag):
        input_vars = get_vars(io_defines, code, var_input_end_tag)
        code.seek(0)
        if input_vars is None:
            print("No hubo cierre de declaracion de variables de entrada")
        else:
            if search_tag(code, var_output_begin_tag):
                output_vars = get_vars(io_defines, code, var_output_end_tag)
                code.seek(0)
            else:
                print("No hubo declaracion apertura de variables de salida")
                return
            if output_vars is None:
                print("No hubo cierre de declaracion de variables de salida")
            else:
                if search_tag(code, inter_vars_begin_tag):
                    vars_tuple = get_vars(internal_vars, code, inter_vars_end_tag)
                    vars_dict = dict(vars_tuple)
                    code.seek(0)
                if vars_tuple is None:
                    print("No hubo cierre de declaracion de variables internas")
                else:
                    if search_tag(code, program_begin_tag):
                        code_lines = process_line(code, program_end_tag)
                        code.seek(0)
                    if code_lines is None:
                        print("No hubo cierre de programa")
                    else:

                        # ---------------------- Proceso de compilacion -------------------------------------

                        # Mapeo de I/O a direcciones de memoria
                        mapped_io = map_io(input_vars, output_vars)

                        # Obtengo la direccion de memoria inicial para almacenar bools
                        bool_mem_start = max(mapped_io.values()) + 1

                        # Genero el mapa de memoria de todas las variables
                        mapped_internal, word_ctr = map_internal_variables(vars_dict, bool_mem_start)
                        memory_map = dict(mapped_io)
                        memory_map.update(mapped_internal)

                        #print(memory_map)

                        # Genero lenguaje de maquina y ademas devuelvo un mapa de memoria actualizado
                        compiled_code, memory_map_new, word_ctr = compile_code(code_lines, memory_map, word_ctr)

                        compiled_io = [0]*12               # Reservo memoria para la lista
                        all_io = output_vars + input_vars  # Concateno todo el i/o en una sola lista

                        for var, pin_id in all_io:
                            compiled_io[io_positions[pin_id]] = mapped_io[var]
                        compiled_full = compiled_io + compiled_code
                        print(compiled_full)
    else:
        print("No hay declaracion de variables de entrada")

    code.close()
    return


main()

