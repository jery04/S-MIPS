import os
import subprocess
import optparse


verbose_level = 0
verbose_level_all = 4
verbose_level_compile_detail = 3
verbose_level_test_detail = 2
verbose_level_test_basic_detail = 1


def print_verbose(verbose_level_required: int, *args):
    if verbose_level >= verbose_level_required:
        print(*args)


class TestCase:
    def __init__(
        self,
        test_name: str,
        file: str,
        expected_result: str | None,
        expected_speed: int | None = None,
    ):
        self.file = file
        self.expected_result = expected_result
        self.expected_speed = expected_speed
        self.test_name = test_name
        self.runned = False
        self.failed = False
        self.error = False

    def run(self, logisim: str, circ: str, template: str) -> None:
        result = ""
        cmd = [
            logisim,
            template,
            "-tty",
            "halt,tty,speed",
            "-load",
            self.file,
            "-sub",
            template,
            circ,
        ]
        try:
            print_verbose(
                verbose_level_test_detail, "Ejecutando el test: ", self.test_name
            )
            result = subprocess.run(cmd, stdout=subprocess.PIPE)
            self.runned = True
            if result.returncode != 0:
                print("Error al ejecutar test: ", self.test_name)
                print(result.stdout)
                print(result.stderr)
                self.error = True
                self.failed = True
                return
            output = bytes.decode(result.stdout)
            r = output.find("halted due to halt pin")
            self.result = output[:r].strip()
            s = output.find("Hz (")
            e = output.find(" ticks", s)
            self.speed = output[s + 4 : e]

            self.failed = self.result != self.expected_result or (
                self.expected_speed != None and self.speed > self.expected_speed
            )

        except subprocess.CalledProcessError as e:
            print("Error al ejecutar test: ", self.test_name)
            print(result.stdout)
            print(result.stderr)
            self.error = True
            self.failed = True

    def print(self) -> None:
        if self.error:
            print("El test no pudo ejecutarse correctamente")

        elif self.runned:
            status = self.result == self.expected_result
            print(
                "Resultado:",
                self.test_name,
                " ===============================================> ",
                "OK" if status else "FAIL",
            )
            print_verbose(
                verbose_level_test_detail,
                "Resultado Esperado: ",
                self.expected_result,
                "Resultado Obtenido: ",
                self.result,
            )
            if self.expected_speed != None:
                status = self.speed <= self.expected_speed
                print(
                    "Tiempo:",
                    self.test_name,
                    " ===============================================> ",
                    "OK" if status else "FAIL",
                )
                print_verbose(
                    verbose_level_test_detail,
                    "Tiempo Esperado: ",
                    self.expected_speed,
                    "Tiempo Obtenido: ",
                    self.speed,
                )
            else:
                print_verbose(
                    verbose_level_test_detail,
                    "Tiempo Obtenido: ",
                    self.speed,
                )

        else:
            print("Test:", self.test_name, "Debe correr el test antes")

        print(
            "---------------------------------------------------------------------------------------"
        )


class TestSuite:
    def __init__(self, dir: str, base_dir: str, circ: str, template: str):
        self.base_dir = base_dir
        self.circ = circ
        self.path = dir
        self.test: list[TestCase] = []
        self.template = template
        for file, path in self.searchAsmFiles():
            self.compile(file, path)
            expected = self.extractExpectedResult(path)
            excepted_time = self.extractExpectedSpeed(path)
            self.test.append(
                TestCase(
                    file,
                    os.path.join(self.base_dir, file, "Bank"),
                    expected,
                    excepted_time,
                )
            )
        self.failed: bool = False

    def searchAsmFiles(self):
        for root, _, files in os.walk(self.path):
            print_verbose(verbose_level_all, "Buscando archivos .asm en: ", root)
            for file in files:
                try:
                    if file.endswith(".asm"):
                        print_verbose(verbose_level_all, "Archivo encontrado: ", file)
                        path = os.path.join(root, file)
                        yield file[:-4], path
                except Exception as e:
                    print("e")

    def compile(self, file: str, path: str) -> None:
        base_dir = os.path.join(self.base_dir, file)
        print_verbose(verbose_level_all, "Creando directorio: ", base_dir)
        try:
            os.mkdir(base_dir)
        except FileExistsError as e:
            print_verbose(verbose_level_all, "Directorio existente: ", base_dir)
        print_verbose(verbose_level_all, "Compilando: ", path)
        status = os.system(f"python3 assembler.py {path} -o {base_dir}")
        if status != 0:
            print("Error al compilar: ", path)

    def extractExpectedResult(self, path: str) -> str | None:
        with open(path, "r") as file:
            content = file.readlines()

        expected = None

        for line in content:
            if line.startswith("#prints"):
                expected = line[8:].strip()
                break
        else:
            return None
        print_verbose(verbose_level_all, "Resultado esperado del test: ")
        print_verbose(verbose_level_all, expected)
        return expected

    def extractExpectedSpeed(self, path: str) -> int | None:
        with open(path, "r") as file:
            content = file.readlines()

        expected = None

        for line in content:
            if line.startswith("#limit"):
                expected = int(line[7:].strip())
                break
        else:
            return None
        print_verbose(verbose_level_all, "Tiempo esperado del test: ")
        print_verbose(verbose_level_all, expected)
        return expected

    def run_all(self) -> None:
        for test in self.test:
            test.run("logisim", self.circ, self.template)
            self.failed |= test.failed
            test.print()

    def run_test(self, test_name: str) -> None:
        for test in self.test:
            if test.name == test_name:
                test.run("logisim", self.circ, self.template)
                self.failed |= test.failed
                test.print()


if __name__ == "__main__":
    usage = "usage: %prog tests_dir circuit [options]"

    parser = optparse.OptionParser(usage=usage)
    parser.add_option(
        "-o",
        "--out",
        dest="output_folder",
        type="string",
        default=".",
        help="Specify output folder to compile tests",
    )
    parser.add_option(
        "-t",
        "--template",
        dest="template",
        type="string",
        default="s-mips-template.circ",
        help="The template .circ file without specific implementation",
    )
    parser.add_option(
        "-v",
        "--verbose",
        dest="verbose",
        type="int",
        default=0,
        help="Verbose debug mode",
    )
    options, args = parser.parse_args()
    if len(args) != 2:
        parser.error("Incorrect command line arguments")
        exit(1)

    verbose_level: int = options.verbose

    output_folder: str = options.output_folder
    template: str = options.template
    input_dir: str = args[0]
    circ: str = args[1]

    try:
        os.mkdir(output_folder)
    except FileExistsError as e:
        print_verbose(verbose_level_all, "Directorio existente: ", output_folder)

    if not os.path.exists(template):
        print("El archivo de template no existe")
        exit(1)

    test_suite = TestSuite(input_dir, output_folder, circ, template)
    test_suite.run_all()
    if test_suite.failed:
        exit(1)
