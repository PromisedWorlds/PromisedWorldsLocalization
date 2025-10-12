# Localization formatter and synchronizer script
# Script made by Leo-Mathguy (@leomathguy on discord) originally for Promised Worlds under the same CC-BY-NC-SA licence as PromisedWorlds/PromisedWorlds
# Script formatted with black formatter please keep it that way

from multiprocessing import Value
import os
import random
from enum import Enum
from logging import WARNING
from math import ceil, floor
from re import S
import shutil
from time import sleep
from typing import Dict, List

from yaspin import Spinner, yaspin
from yaspin.core import Yaspin
from yaspin.spinners import Spinners

DEBUG = False
PROGSIZE = 40

BANNER = """\
.............................................:=+##*=-:............
.........................................-#@@@%%##++=---:.........
.......................................+@@%#%#*=-:................
.....................................:@@%###+=-...................
...................................:@@%%*+=:......................
...................................#@@#+++=:+=-==:................
...................................@@%+++-+@=+==*#:...............
...................................@%#%++@#%@@+=%*=.:.............
...................................%##==*++%#-=+%@+==.............
...............-+#@@%%%%%%%#=-.....#@#=.:=#%##%+#@%:.:............
...........:#@@%%#**+==++==-=-=*=...@%-..:=+##++%%+--=-...........
.........+@@%%%*#+=-==-:.-:...:.....:%+:...:+=+++++=+-............
.......=@@@%###**+--................:.*-......:...-.-=............
......%%%#*++++=--::....................:.........................
.....%%#**+++=-:................==................................
...:@%%++++=-...................=+:...............................
...#%%%#-=-::.-..-..---................:-:........................
..=%%%#*+-========--=-::..........:-:....:........................
..#%#+*+=-======:.....-=-.........-=:....:-.......................
..#%#++--.:==---:..................-:.....-.......................
..%%====:.....-:.........................::.......................
..##*++=.....:--:.......................::........................
..+##+=-....:..-::................................................
...=%=..........:=.................=+..:+.........................
....=*:..........................-*==.............................
.....-=........==::.............=+=:..............................
........................-:.........-..............................
................:---:.............................................
................:======..........................................."""
BASE = "en-us"


# ANSI Terminal colors
class Colors:
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    STRIKE = "\033[9m"

    RED = "\033[31m"
    BLACK = "\033[30m"


# Log prefixes
class Logs:
    FAIL = f"[{Colors.FAIL}{Colors.BOLD}X{Colors.ENDC}]"
    OK = f"[{Colors.OKGREEN}{Colors.BOLD}✓{Colors.ENDC}]"
    INFO = "[*]"
    WARN = f"[{Colors.WARNING}{Colors.BOLD}!{Colors.ENDC}]"


def print_banner():
    colors = {
        "#": Colors.RED,
        "*": Colors.RED,
        "%": Colors.RED + Colors.BOLD,
        "@": Colors.RED + Colors.BOLD,
        "=": Colors.BLACK + Colors.BOLD,
        "+": Colors.RED,
        "-": Colors.RED,
        ":": Colors.BLACK + Colors.BOLD,
    }

    for line in BANNER.splitlines():
        sleep(0.01)
        line = line.replace(".", " ")
        for char, color in colors.items():
            line = line.replace(char, color + char + Colors.ENDC)
        print(line)


dir_path = os.getcwd().split("/")[-1]

# Localization file classes


class LineType(Enum):
    DATA = 0
    DATACOMMENT = 1
    HEADING = 2
    SUBHEADING = 3
    MICROHEADING = 4
    PLANET = 5


class LocLine:
    def __init__(self, type: LineType, content: str, key: str = "", glued=None):
        self.type: LineType = type
        self.content = content
        self.key = key
        self.glued: LocLine = glued

    def __str__(self) -> str:
        ret = ""

        if self.glued is not None:
            ret += str(self.glued)

        ret += " " * 8  # 2 Indentations
        match self.type:
            case LineType.DATA:
                ret += self.key + " = " + self.content
            case LineType.DATACOMMENT:
                ret += "// " + self.content
            case LineType.HEADING:
                ret = "\n" + ret
                ret += "// " + "*" * 8 + " " + self.content + " " + "*" * 8 + "\n"
            case LineType.SUBHEADING:
                ret = "\n" + ret
                ret += "// " + "*" * 4 + " " + self.content + " " + "*" * 4
            case LineType.MICROHEADING:
                ret = "\n" + ret
                ret += "// " + "*" * 2 + " " + self.content + " " + "*" * 2
            case LineType.PLANET:
                ret = "\n" + ret
                ret += "// " + "-" * 20 + " " + self.content + " " + "-" * 20 + "\n"

        ret += "\n"

        return ret


## IMPORTANT: Only one language per file ##
class Localization:
    def __init__(self, language_code: str):
        self.code: str = language_code
        self.lines: List[LocLine] = []

    def add_line(self, line: LocLine):
        self.lines.append(line)

    def read_file(
        self, filename: str, code: str = None, spinner: Yaspin = None
    ) -> tuple:
        """Read a file into the current Localization object. Clear lines beforehand

        Args:
            filename (str): Filename to read from
            code (str): Language code (optional)

        Raises:
            ValueError: Errors during reading

        Returns:
            tuple: Amount of definitions, headings and comments
        """

        loc = Localization(code if code else self.code)
        amounts = [0, 0, 0]

        num_lines = 0
        if spinner:
            num_lines = sum(1 for _ in open(filename))

        with open(filename, "r") as lg:
            enter_root_loc = False
            enter_loc = False
            glue_comment: LocLine = None

            for i, line in enumerate(lg.readlines()):
                if spinner:
                    if i % ceil(num_lines / 100) == 0:
                        prognum = floor(i / num_lines * PROGSIZE)
                        prog = f"[{'#' * prognum}{'-' * (PROGSIZE-prognum)}]"

                        spinner.text = (
                            str(i).rjust(len(str(num_lines)), "0")
                            + "/"
                            + str(num_lines)
                            + " "
                            + prog
                        )
                        sleep(random.randint(2, 10) / 1000)

                line = line.removesuffix("\n")
                if DEBUG:
                    print(f"Line {i}: " + '"' + line + '"')
                match i:
                    case 0:
                        if line.strip() != "Localization":
                            raise ValueError("No root Localization object")
                    case 2:
                        if not enter_root_loc:
                            raise ValueError("Unexpected language code")
                    case _:
                        # Brackets
                        if line.strip() == "{":
                            if enter_loc and enter_root_loc:
                                raise ValueError(f"Unexpected {'{'} on line {i+1}")
                            elif enter_root_loc:
                                enter_loc = True
                            else:
                                enter_root_loc = True
                        if line.strip() == "}":
                            if not enter_loc and not enter_root_loc:
                                raise ValueError(f"Unexpected {'}'} on line {i+1}")
                            elif enter_root_loc:
                                enter_root_loc = False
                            else:
                                enter_loc = False

                        # Actual locs
                        line = line.strip()

                        # Comments
                        if line[:2] == "//":
                            t = LineType.DATACOMMENT
                            comment = line.removeprefix("//").strip()
                            if comment:
                                if comment[0] == "*":
                                    star_amount = len(comment) - len(
                                        comment.lstrip("*")
                                    )

                                    match star_amount:
                                        case 8:
                                            t = LineType.HEADING
                                        case 4:
                                            t = LineType.SUBHEADING
                                        case 2:
                                            t = LineType.MICROHEADING
                                        case _:
                                            print(
                                                Logs.WARN,
                                                f"Possible mistyped heading on line {i+1}",
                                            )

                                    if t != LineType.DATACOMMENT:
                                        comment = (
                                            comment.lstrip("*").rstrip("*").strip()
                                        )
                                    else:
                                        print(
                                            f"{Logs.WARN} Possible mistyped heading on line {i-1}! (* at the start)"
                                        )
                                elif comment[0] == "-":
                                    dash_amount = len(comment) - len(
                                        comment.lstrip("-")
                                    )

                                    if dash_amount >= 2:
                                        t = LineType.PLANET
                                        comment = (
                                            comment.lstrip("-").rstrip("-").strip()
                                        )

                            if t == LineType.DATACOMMENT:
                                glue_comment = LocLine(
                                    t,
                                    comment,
                                    glued=glue_comment,
                                )
                                amounts[2] += 1
                            else:
                                loc.add_line(LocLine(t, comment, glued=glue_comment))
                                amounts[1] += 1
                                glue_comment = None

                        if len(line) == 0:
                            continue

                        # Loc
                        if line[0] == "#":
                            separated = line.split("=", 1)
                            if len(separated) != 2:
                                raise ValueError(
                                    f"Invalid localization on line {i+1} (= not detected?)"
                                )
                            key = separated[0].strip()
                            value = separated[1].strip()
                            loc.add_line(
                                LocLine(LineType.DATA, value, key, glue_comment)
                            )
                            amounts[0] += 1
                            glue_comment = None
            if enter_loc or enter_root_loc:
                raise ValueError(f"Brackets not closed (check end of file)")

        self.lines = loc.lines
        self.code = code if code else self.code

        return tuple(amounts)

    def __str__(self) -> str:
        ret = """Localization
{
    en-us
    {\n"""
        for line in self.lines:
            ret += str(line)

        ret += """    }
}"""

        while ret.splitlines()[4].strip("\n").strip() == "":
            ret = "\n".join(
                [line for i, line in enumerate(ret.splitlines()) if i != 4]
            )  # I know bandaid solution but it works

        return ret


print_banner()
print(
    Colors.OKGREEN + Colors.BOLD + "=" * 15 + Colors.ENDC,
    Colors.UNDERLINE
    + Colors.BOLD
    + Colors.OKBLUE
    + "LOCALIZATION SYNCHRONIZER"
    + Colors.ENDC,
    Colors.OKGREEN + Colors.BOLD + "=" * 15 + Colors.ENDC,
)
sleep(0.2)

basefile = BASE + ".cfg"
base = Localization(BASE)

with yaspin(Spinner(Spinners.line.frames, 40), f"Loading {basefile}") as sp:
    sleep(0.2)
    if not os.path.exists(basefile):
        sp.text = f'Error loading file: "{basefile}" does not exist'
        sp.fail(Logs.FAIL)
        exit()

    sp.text = f"Reading {basefile}"
    try:
        amounts = base.read_file(basefile, BASE, sp)
    except ValueError as e:
        sp.text = f'Error reading file "{basefile}": {str(e)}'
        sp.fail(Logs.FAIL)
        exit()

    sp.text = f"{basefile} loaded successfuly"
    sp.ok(Logs.OK)

sleep(0.03)
print(Logs.INFO, f"Loaded {amounts[0]} definitions")
sleep(0.03)
print(Logs.INFO, f"Loaded {amounts[1]} headings")
sleep(0.03)
print(Logs.INFO, f"Loaded {amounts[2]} comments")
sleep(0.03)

original = ""
with open(basefile) as f:
    original = f.read()
reformatted = str(base)

same = reformatted == original

base_defs = [x for x in base.lines if x.type == LineType.DATA]
base_keys = [x.key for x in base_defs]


def print_selection():
    print(
        Colors.BOLD
        + Colors.OKGREEN
        + "=" * 16
        + " "
        + Colors.OKBLUE
        + Colors.UNDERLINE
        + "Please make a selection"
        + Colors.ENDC
        + Colors.BOLD
        + Colors.OKGREEN
        + " "
        + "=" * 16
        + Colors.ENDC
    )


def print_cursor() -> str:
    return input(f"\n[{Colors.BLACK}{Colors.BOLD}>{Colors.ENDC}] ").lower().strip()


if not same:
    print(Logs.WARN, "Main bundle is not formatted")
    print()
    sleep(0.05)
    print_selection()
    sleep(0.05)
    print(f"[1] Reformat {basefile} (will create a backup)")
    sleep(0.05)
    print(f"[2] Reformat {basefile}")
    sleep(0.05)
    print(f"[x] Exit")
    sleep(0.05)
    i = print_cursor()
    print()

    if i == "x":
        exit()

    try:
        i = int(i)
        if i not in [1, 2]:
            raise ValueError
    except:
        print(Logs.FAIL, "Invalid input")
        exit()

    if i == 1:
        shutil.copyfile(basefile, basefile + ".bak")
        sleep(0.1)
        print(Logs.OK, f"Copied {basefile} to {basefile}.bak")

    try:
        with open(basefile, "w") as f:
            f.write(reformatted)
            sleep(0.1)
    except Exception as e:
        print(Logs.FAIL, f"Error during write: {e}")
        print("Dumping original file:\n")
        print(original)
        exit()

    print(Logs.OK, f"Wrote to {basefile}")

files = [f for f in os.listdir(".") if os.path.isfile(f) and f.endswith(".cfg")]
files.remove(basefile)


print()
sleep(0.05)
print_selection()
sleep(0.05)
if files:
    print(f"[1] Synchronize other language files")
else:
    print(
        f"[{Colors.STRIKE}1{Colors.ENDC}] {Colors.STRIKE}Synchronize other language files{Colors.ENDC}"
    )

sleep(0.05)
print(f"[2] Create a new language")
sleep(0.05)
print(f"[x] Exit")
sleep(0.05)
i = print_cursor()
sleep(0.1)
print()

if i == "x":
    exit()

try:
    i = int(i)
    if i not in ([1, 2] if files else [2]):
        raise ValueError
except:
    print(Logs.FAIL, "Invalid input")
    exit()

if i == 1:
    print(f"Files to be affected: {', '.join(files)}")
    print("Is this correct? (y/n)")
    sleep(0.05)
    i = print_cursor() == "y"
    sleep(0.05)
    if not i:
        print("Okay then, keep your secrets")
        exit()
    print()

    for file in files:
        code = file.removesuffix(".cfg")

        language = Localization(code)

        with yaspin(Spinner(Spinners.line.frames, 40), f"Loading {file}") as sp:
            sleep(0.05)

            sp.text = f"Reading {file}"
            try:
                language.read_file(file)
            except ValueError as e:
                sp.text = f'Error reading file "{file}": {str(e)}'
                sp.fail(Logs.FAIL)
                exit()

            sp.text = f"{file} loaded successfuly"
            sp.ok(Logs.OK)

        file_defs = [x for x in language.lines if x.type == LineType.DATA]
        keys = [x.key for x in file_defs]
        file_dict = {}
        file_dict_2: Dict[str, LocLine] = {}
        for d in file_defs:
            file_dict_2[d.key] = d
            file_dict[d.key] = d.content

        for key in keys:
            if key not in base_keys:
                sleep(0.05)
                print(Logs.WARN, f"{key} is in {code} but not in {BASE}, delete? (Y/n)")
                i = print_cursor()
                if i != "y" and i:
                    exit()

        new_file = Localization(code)

        for line in base.lines:
            match line.type:
                case LineType.DATA:
                    if line.key in keys:
                        new_file.add_line(
                            LocLine(
                                line.type,
                                file_dict.get(line.key, line.content),
                                line.key,
                                line.glued,
                            )
                        )

                        if line.glued or file_dict_2[line.key].glued:
                            glued_lines: List[LocLine] = []
                            l = line
                            while l.glued:
                                glued_lines.append(l.glued)
                                l = l.glued

                            lang_glued: List[LocLine] = []

                            if l := file_dict_2.get(line.key):
                                while l.glued:
                                    lang_glued.append(l.glued)
                                    l = l.glued

                            for l in lang_glued:
                                if l.content not in [x.content for x in glued_lines]:
                                    glued_lines.insert(0, l)
                                    if len(glued_lines) > 1:
                                        glued_lines[0].glued = glued_lines[1]

                            new_file.lines[-1].glued = glued_lines[0]
                    else:
                        new_file.lines.append(line)
                case _:
                    new_file.lines.append(line)

        with open(code + ".cfg", "w") as f:
            f.write(str(new_file))
            sleep(0.03)
            print(Logs.OK, f"Wrote to {code}.cfg")

elif i == 2:
    print("NOTE: Will overwrite existing file if it exists")
    print("Please enter language code")
    name = print_cursor()
    sleep(0.1)
    name.replace("_", "-")

    new = reformatted
    new = new.replace(BASE.replace("_", "-"), name.replace("_", "-"))

    with open(name + ".cfg", "w") as f:
        f.write(new)
        sleep(0.1)
        print(Logs.OK, f"Wrote to {name}.cfg")
