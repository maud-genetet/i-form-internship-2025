""" Parser for neutral files """

from .models.element import Element
from .models.node import Node
from .models.neutral_file import NeutralFile
from .models.die import Die
import time
import logging
logger = logging.getLogger(__name__)


class ParserNeutralFile:

    @staticmethod
    def parser_file(filename):
        t1 = time.time()
        try:
            with open(filename, 'r', encoding='utf-8') as file:

                lines = file.readlines()
                if not lines:
                    logger.error("The file is empty.")
                    return

                # Title verification
                neu = NeutralFile(lines[0].strip())

                nb_nodes = int(lines[1].strip())
                # logger.info(f"Number of nodes: {nb_nodes}")

                # Node processing
                for i in range(2, 2 + nb_nodes):
                    line = lines[i].strip()
                    if line:
                        parts = line.split()
                        if len(parts) < 7:
                            logger.info(
                                f"Format error for node at line {i + 1}.")
                            continue

                        node = Node(int(parts[0]))
                        node.x = float(parts[1].replace('D', 'E'))
                        node.y = float(parts[2].replace('D', 'E'))
                        node.vx = float(parts[3].replace('D', 'E'))
                        node.vy = float(parts[4].replace('D', 'E'))
                        node.fx = float(parts[5].replace('D', 'E'))
                        node.fy = float(parts[6].replace('D', 'E'))

                        neu.add_node(node)

                current_line = 2 + nb_nodes

                nb_elements = int(lines[current_line].strip())
                # logger.info(f"Number of elements: {nb_elements}")

                current_line += 1

                # Element processing
                for i in range(nb_elements):
                    base_line = current_line + i

                    line = lines[base_line].strip()
                    if line:
                        parts = line.split()
                        if len(parts) >= 9:
                            element = Element(int(parts[0]))

                            element.matno = int(parts[1])
                            element.lnods.append(
                                neu.get_node_by_id(int(parts[2])))
                            element.lnods.append(
                                neu.get_node_by_id(int(parts[3])))
                            element.lnods.append(
                                neu.get_node_by_id(int(parts[4])))
                            element.lnods.append(
                                neu.get_node_by_id(int(parts[5])))
                            element.rindx = float(parts[6].replace('D', 'E'))
                            element.densy = float(parts[7].replace('D', 'E'))
                            element.fract = float(parts[8].replace('D', 'E'))

                            neu.add_element(element)
                        else:
                            logger.error(
                                f"Format error for element at line {base_line + 1}.")

                    strain_rate_line = current_line + nb_elements + i
                    line = lines[strain_rate_line].strip().replace('D', 'E')
                    if line:
                        parts = line.split()
                        if len(parts) >= 6:
                            element = neu.get_element_by_id(int(parts[0]))

                            if element:
                                element.srnrt_exx = float(parts[1])
                                element.srnrt_eyy = float(parts[2])
                                element.srnrt_ezz = float(parts[3])
                                element.srnrt_exy = float(parts[4])
                                element.srnrt_e = float(parts[5])
                                element.srnrt_ev = float(parts[6])
                        else:
                            logger.error(
                                f"Format error for strain rate element at line {strain_rate_line + 1}.")

                    strain_line = current_line + 2 * nb_elements + i
                    line = lines[strain_line].strip().replace('D', 'E')
                    if line:
                        parts = line.split()
                        if len(parts) >= 8:
                            element = neu.get_element_by_id(int(parts[0]))

                            if element:
                                element.strain_exx = float(parts[1])
                                element.strain_eyy = float(parts[2])
                                element.strain_ezz = float(parts[3])
                                element.strain_exy = float(parts[4])
                                element.strain_e = float(parts[5])
                                element.strain_e1 = float(parts[6])
                                element.strain_e3 = float(parts[7])
                                element.angle13 = float(parts[8])

                        else:
                            logger.error(
                                f"Format error for strain element at line {strain_line + 1}.")

                    stress_line = current_line + 3 * nb_elements + i
                    line = lines[stress_line].strip().replace('D', 'E')
                    if line:
                        parts = line.split()
                        if len(parts) >= 7:
                            element = neu.get_element_by_id(int(parts[0]))

                            if element:
                                element.stress_oxx = float(parts[1])
                                element.stress_oyy = float(parts[2])
                                element.stress_ozz = float(parts[3])
                                element.stress_oxy = float(parts[4])
                                element.stress_o = float(parts[5])
                                element.stress_orr = float(parts[6])
                        else:
                            logger.error(
                                f"Format error for stress element at line {stress_line + 1}.")

                current_line += 4 * nb_elements

                # Temperature nodes
                for i in range(current_line, current_line + nb_nodes):
                    line = lines[i].strip()
                    if line:
                        parts = line.split()
                        if len(parts) < 3:
                            logger.error(
                                f"Format error for temperature node at line {i + 1}.")
                            continue

                        node = neu.get_node_by_id(int(parts[0]))

                        if node:
                            node.dtemp = float(parts[1].replace('D', 'E'))
                            node.temp = float(parts[2].replace('D', 'E'))
                current_line += nb_nodes

                # Die elements
                nb_dies = int(lines[current_line].strip())
                current_line += 2
                # logger.info(f"Number of dies: {nb_dies}")

                for die_index in range(current_line, current_line + nb_dies):

                    line = lines[current_line].strip()
                    if line:
                        parts = line.split()
                        if len(parts) < 3:
                            logger.error(
                                f"Format error for die at line {current_line + 1}.")
                        else:
                            die = Die(int(parts[0]))
                            neu.add_die(die)

                            current_line += 1

                            die_line = lines[current_line].strip()
                            if die_line:
                                parts_die = die_line.split()
                                if len(parts_die) < 7:
                                    logger.error(
                                        f"Format error for die at line {current_line + 1}.")

                                main_node = Node(-1)  # Temporary ID
                                main_node.x = float(
                                    parts_die[0].replace('D', 'E'))
                                main_node.y = float(
                                    parts_die[1].replace('D', 'E'))
                                main_node.vx = float(
                                    parts_die[2].replace('D', 'E'))
                                main_node.vy = float(
                                    parts_die[3].replace('D', 'E'))
                                main_node.fx = float(
                                    parts_die[5].replace('D', 'E'))
                                main_node.fy = float(
                                    parts_die[6].replace('D', 'E'))
                                die.main_node = main_node
                                die.m = float(parts_die[4].replace('D', 'E'))
                                die.temp = float(parts[2].replace('D', 'E'))

                                current_line += 1

                            for j in range(current_line, current_line + int(parts[1])):
                                node_line = lines[j].strip()
                                if node_line:
                                    node_parts = node_line.split()
                                    if len(node_parts) < 2:
                                        logger.error(
                                            f"Format error for die node at line {j + 1}.")
                                        continue

                                    node = Node(-1)  # Temporary ID
                                    node.x = float(
                                        node_parts[0].replace('D', 'E'))
                                    node.y = float(
                                        node_parts[1].replace('D', 'E'))
                                    die.nodes.append(node)

                            current_line += int(parts[1])

                # Contact nodes
                nb_contact_elements = int(lines[current_line].strip())
                current_line += 1

                # put the node n in contact with set_contact
                for i in range(current_line, current_line + nb_contact_elements):
                    line = lines[i].strip()
                    if line:
                        parts = line.split()
                        if len(parts) < 1:
                            logger.error(
                                f"Format error for contact element at line {i + 1}.")
                            continue

                        node = neu.get_node_by_id(int(parts[0]))
                        node.is_contact = True

                current_line += nb_contact_elements

                # logger.info(f"Number of contact elements: {nb_contact_elements}")

                nb_code_elements = int(lines[current_line].strip())
                current_line += 1

                # logger.info(f"Number of nodes with code: {nb_code_elements}")

                for i in range(current_line, current_line + nb_code_elements):
                    line = lines[i].strip()
                    if line:
                        parts = line.split()
                        if len(parts) < 2:
                            logger.error(
                                f"Format error for code node at line {i + 1}.")
                            continue

                        node = neu.get_node_by_id(int(parts[0]))
                        if node:
                            node.code = float(parts[1].replace('D', 'E'))

                current_line += nb_code_elements
                # Time
                time_line = lines[current_line].strip()
                if time_line:
                    try:
                        neu.t_time = float(time_line.replace('D', 'E'))
                    except ValueError:
                        logger.error(
                            f"Format error for time at line {current_line + 1}.")
                else:
                    logger.error(
                        f"No time data found at line {current_line + 1}.")

                t2 = time.time()
                logger.info(f"File processing time: {t2 - t1:.2f} seconds")
                return neu

        except FileNotFoundError:
            logger.error(f"Error: File '{filename}' not found.")
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    @staticmethod
    def parser_file_graphics(filename):
        t1 = time.time()
        try:
            with open(filename, 'r', encoding='utf-8') as file:

                lines = file.readlines()
                if not lines:
                    logger.error("The file is empty.")
                    return

                neu = NeutralFile(lines[0].strip())

                nb_nodes = int(lines[1].strip())

                current_line = 2 + nb_nodes

                nb_elements = int(lines[current_line].strip())

                current_line += 1 + 4 * nb_elements + nb_nodes

                # Die elements
                nb_dies = int(lines[current_line].strip())
                current_line += 2
                # logger.info(f"Number of dies: {nb_dies}")

                for die_index in range(current_line, current_line + nb_dies):

                    line = lines[current_line].strip()
                    if line:
                        parts = line.split()
                        if len(parts) < 3:
                            logger.error(
                                f"Format error for die at line {current_line + 1}.")
                        else:
                            die = Die(int(parts[0]))
                            neu.add_die(die)

                            current_line += 1

                            die_line = lines[current_line].strip()
                            if die_line:
                                parts_die = die_line.split()
                                if len(parts_die) < 7:
                                    logger.error(
                                        f"Format error for die at line {current_line + 1}.")

                                main_node = Node(-1)  # Temporary ID
                                main_node.x = float(
                                    parts_die[0].replace('D', 'E'))
                                main_node.y = float(
                                    parts_die[1].replace('D', 'E'))
                                main_node.vx = float(
                                    parts_die[2].replace('D', 'E'))
                                main_node.vy = float(
                                    parts_die[3].replace('D', 'E'))
                                main_node.fx = float(
                                    parts_die[5].replace('D', 'E'))
                                main_node.fy = float(
                                    parts_die[6].replace('D', 'E'))
                                die.main_node = main_node
                                die.m = float(parts_die[4].replace('D', 'E'))
                                die.temp = float(parts[2].replace('D', 'E'))

                                current_line += 1

                            for j in range(current_line, current_line + int(parts[1])):
                                node_line = lines[j].strip()
                                if node_line:
                                    node_parts = node_line.split()
                                    if len(node_parts) < 2:
                                        logger.error(
                                            f"Format error for die node at line {j + 1}.")
                                        continue

                                    node = Node(-1)  # Temporary ID
                                    node.x = float(
                                        node_parts[0].replace('D', 'E'))
                                    node.y = float(
                                        node_parts[1].replace('D', 'E'))
                                    die.nodes.append(node)

                            current_line += int(parts[1])

                # Contact nodes
                nb_contact_elements = int(lines[current_line].strip())
                current_line += 1

                current_line += nb_contact_elements

                nb_code_elements = int(lines[current_line].strip())
                current_line += 1

                current_line += nb_code_elements

                # Time
                time_line = lines[current_line].strip()
                if time_line:
                    try:
                        neu.t_time = float(time_line.replace('D', 'E'))
                    except ValueError:
                        logger.error(
                            f"Format error for time at line {current_line + 1}.")
                else:
                    logger.error(
                        f"No time data found at line {current_line + 1}.")

                t2 = time.time()
                logger.info(
                    f"GRAPHICS: File processing time: {t2 - t1:.2f} seconds")
                return neu

        except FileNotFoundError:
            logger.error(f"Error: File '{filename}' not found.")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
