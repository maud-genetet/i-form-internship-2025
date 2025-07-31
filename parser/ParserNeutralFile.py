from .models.Element import Element
from .models.Node import Node
from .models.NeutralFile import NeutralFile
from .models.Die import Die
import time
import logging
logger = logging.getLogger(__name__)

class ParserNeutralFile:

    @staticmethod
    def parser_file(nom_fichier):
        t1 = time.time()
        try:
            with open(nom_fichier, 'r', encoding='utf-8') as fichier:


                lignes = fichier.readlines()
                if not lignes:
                    logger.error("Le fichier est vide.")
                    return
                
                # Vérification du titre
                neu = NeutralFile(lignes[0].strip())

                nb_nodes = int(lignes[1].strip())
                #logger.info(f"Nombre de noeuds : {nb_nodes}")

                # Traitement des noeuds
                for i in range(2, 2 + nb_nodes):
                    ligne = lignes[i].strip()
                    if ligne:
                        parts = ligne.split()
                        if len(parts) < 7:
                            logger.info(f"Erreur de format pour le noeud à la ligne {i + 1}.")
                            continue

                        node = Node(int(parts[0]))
                        node.x = float(parts[1].replace('D', 'E'))
                        node.y = float(parts[2].replace('D', 'E'))
                        node.vx = float(parts[3].replace('D', 'E'))
                        node.vy = float(parts[4].replace('D', 'E'))
                        node.fx = float(parts[5].replace('D', 'E'))
                        node.fy = float(parts[6].replace('D', 'E'))

                        neu.add_node(node)

                actual_ligne = 2 + nb_nodes

                nb_elements = int(lignes[actual_ligne].strip())
                #logger.info(f"Nombre d'éléments : {nb_elements}")

                actual_ligne += 1

                # Traitement des éléments
                for i in range(nb_elements):
                    base_line = actual_ligne + i
                    
                    ligne = lignes[base_line].strip()
                    if ligne:
                        parts = ligne.split()
                        if len(parts) >= 9:
                            element = Element(int(parts[0]))

                            element.matno = int(parts[1])
                            element.lnods.append(neu.get_node_by_id(int(parts[2])))
                            element.lnods.append(neu.get_node_by_id(int(parts[3])))
                            element.lnods.append(neu.get_node_by_id(int(parts[4])))
                            element.lnods.append(neu.get_node_by_id(int(parts[5])))
                            element.rindx = float(parts[6].replace('D', 'E'))
                            element.densy = float(parts[7].replace('D', 'E'))
                            element.fract = float(parts[8].replace('D', 'E'))

                            neu.add_element(element)
                        else:
                            logger.error(f"Erreur de format pour l'élément à la ligne {base_line + 1}.")

                    strain_rate_line = actual_ligne + nb_elements + i
                    ligne = lignes[strain_rate_line].strip().replace('D', 'E')
                    if ligne:
                        parts = ligne.split()
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
                            logger.error(f"Erreur de format pour l'élément de taux de déformation à la ligne {strain_rate_line + 1}.")

                    strain_line = actual_ligne + 2 * nb_elements + i
                    ligne = lignes[strain_line].strip().replace('D', 'E')
                    if ligne:
                        parts = ligne.split()
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
                            logger.error(f"Erreur de format pour l'élément de déformation à la ligne {strain_line + 1}.")

                    stress_line = actual_ligne + 3 * nb_elements + i
                    ligne = lignes[stress_line].strip().replace('D', 'E')
                    if ligne:
                        parts = ligne.split()
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
                            logger.error(f"Erreur de format pour l'élément de contrainte à la ligne {stress_line + 1}.")

                actual_ligne += 4 * nb_elements

                # Temperature nodes
                for i in range(actual_ligne, actual_ligne + nb_nodes):
                    ligne = lignes[i].strip()
                    if ligne:
                        parts = ligne.split()
                        if len(parts) < 3:
                            logger.error(f"Erreur de format pour le noeud de température à la ligne {i + 1}.")
                            continue

                        node = neu.get_node_by_id(int(parts[0]))

                        if node:
                            node.dtemp = float(parts[1].replace('D', 'E'))
                            node.temp = float(parts[2].replace('D', 'E'))
                actual_ligne += nb_nodes

                # Die elements
                nb_dies = int(lignes[actual_ligne].strip())
                actual_ligne += 2
                #logger.info(f"Nombre de dies : {nb_dies}")
                
                for die_index in range(actual_ligne, actual_ligne + nb_dies):

                    ligne = lignes[actual_ligne].strip()
                    if ligne:
                        parts = ligne.split()
                        if len(parts) < 3:
                            logger.error(f"Erreur de format pour le die à la ligne {actual_ligne + 1}.")
                        else:
                            die = Die(int(parts[0]))
                            neu.add_die(die)

                            actual_ligne += 1

                            ligne_die = lignes[actual_ligne].strip()
                            if ligne_die:
                                parts_die = ligne_die.split()
                                if len(parts_die) < 7:
                                    logger.error(f"Erreur de format pour le die à la ligne {actual_ligne + 1}.")
                                
                                main_node = Node(-1) # ID temporaire
                                main_node.x = float(parts_die[0].replace('D', 'E'))
                                main_node.y = float(parts_die[1].replace('D', 'E'))
                                main_node.vx = float(parts_die[2].replace('D', 'E'))
                                main_node.vy = float(parts_die[3].replace('D', 'E'))
                                main_node.fx = float(parts_die[5].replace('D', 'E'))
                                main_node.fy = float(parts_die[6].replace('D', 'E'))
                                die.main_node = main_node
                                die.m = float(parts_die[4].replace('D', 'E'))
                                die.temp = float(parts[2].replace('D', 'E'))

                                actual_ligne += 1

                            for j in range(actual_ligne, actual_ligne + int(parts[1])):
                                ligne_node = lignes[j].strip()
                                if ligne_node:
                                    node_parts = ligne_node.split()
                                    if len(node_parts) < 2:
                                        logger.error(f"Erreur de format pour le noeud du die à la ligne {j + 1}.")
                                        continue

                                    node = Node(-1) # ID temporaire
                                    node.x = float(node_parts[0].replace('D', 'E'))
                                    node.y = float(node_parts[1].replace('D', 'E'))
                                    die.nodes.append(node)
                            
                            actual_ligne += int(parts[1])

                # Contact nodes
                nb_contact_elements = int(lignes[actual_ligne].strip())
                actual_ligne += 1

                # put the node n in contact with set_contact 
                for i in range(actual_ligne, actual_ligne + nb_contact_elements):
                    ligne = lignes[i].strip()
                    if ligne:
                        parts = ligne.split()
                        if len(parts) < 1:
                            logger.error(f"Erreur de format pour l'élément de contact à la ligne {i + 1}.")
                            continue

                        node = neu.get_node_by_id(int(parts[0]))
                        node.is_contact = True

                actual_ligne += nb_contact_elements

                #logger.info(f"Nombre d'éléments de contact : {nb_contact_elements}")     

                nb_code_elements = int(lignes[actual_ligne].strip())
                actual_ligne += 1

                #logger.info(f"Nombre de node avec code : {nb_code_elements}") 

                for i in range(actual_ligne, actual_ligne + nb_code_elements):
                    ligne = lignes[i].strip()
                    if ligne:
                        parts = ligne.split()
                        if len(parts) < 2:
                            logger.error(f"Erreur de format pour le noeud de code à la ligne {i + 1}.")
                            continue

                        node = neu.get_node_by_id(int(parts[0]))
                        if node:
                            node.code = float(parts[1].replace('D', 'E'))

                actual_ligne += nb_code_elements
                # Temps
                ligne_temps = lignes[actual_ligne].strip()
                if ligne_temps:
                    try:
                        neu.t_time = float(ligne_temps.replace('D', 'E'))
                        #logger.info(f"Temps : {float(ligne_temps.replace('D', 'E'))}")
                    except ValueError:
                        logger.error(f"Erreur de format pour le temps à la ligne {actual_ligne + 1}.")
                else:
                    logger.error(f"Aucune donnée de temps trouvée à la ligne {actual_ligne + 1}.")

                t2 = time.time()
                logger.info(f"Temps de traitement du fichier : {t2 - t1:.2f} secondes")
                return neu

        except FileNotFoundError:
            logger.error(f"Erreur : Le fichier '{nom_fichier}' est introuvable.")
        except Exception as e:
            logger.error(f"Une erreur est survenue : {e}")

    @staticmethod
    def parser_file_graphics(nom_fichier):
        t1 = time.time()
        try:
            with open(nom_fichier, 'r', encoding='utf-8') as fichier:

                lignes = fichier.readlines()
                if not lignes:
                    logger.error("Le fichier est vide.")
                    return
                
                neu = NeutralFile(lignes[0].strip())
                
                nb_nodes = int(lignes[1].strip())

                actual_ligne = 2 + nb_nodes

                nb_elements = int(lignes[actual_ligne].strip())

                actual_ligne += 1 + 4 * nb_elements + nb_nodes

                # Die elements
                nb_dies = int(lignes[actual_ligne].strip())
                actual_ligne += 2
                #logger.info(f"Nombre de dies : {nb_dies}")
                
                for die_index in range(actual_ligne, actual_ligne + nb_dies):

                    ligne = lignes[actual_ligne].strip()
                    if ligne:
                        parts = ligne.split()
                        if len(parts) < 3:
                            logger.error(f"Erreur de format pour le die à la ligne {actual_ligne + 1}.")
                        else:
                            die = Die(int(parts[0]))
                            neu.add_die(die)

                            actual_ligne += 1

                            ligne_die = lignes[actual_ligne].strip()
                            if ligne_die:
                                parts_die = ligne_die.split()
                                if len(parts_die) < 7:
                                    logger.error(f"Erreur de format pour le die à la ligne {actual_ligne + 1}.")
                                
                                main_node = Node(-1) # ID temporaire
                                main_node.x = float(parts_die[0].replace('D', 'E'))
                                main_node.y = float(parts_die[1].replace('D', 'E'))
                                main_node.vx = float(parts_die[2].replace('D', 'E'))
                                main_node.vy = float(parts_die[3].replace('D', 'E'))
                                main_node.fx = float(parts_die[5].replace('D', 'E'))
                                main_node.fy = float(parts_die[6].replace('D', 'E'))
                                die.main_node = main_node
                                die.m = float(parts_die[4].replace('D', 'E'))
                                die.temp = float(parts[2].replace('D', 'E'))

                                actual_ligne += 1

                            for j in range(actual_ligne, actual_ligne + int(parts[1])):
                                ligne_node = lignes[j].strip()
                                if ligne_node:
                                    node_parts = ligne_node.split()
                                    if len(node_parts) < 2:
                                        logger.error(f"Erreur de format pour le noeud du die à la ligne {j + 1}.")
                                        continue

                                    node = Node(-1) # ID temporaire
                                    node.x = float(node_parts[0].replace('D', 'E'))
                                    node.y = float(node_parts[1].replace('D', 'E'))
                                    die.nodes.append(node)
                            
                            actual_ligne += int(parts[1])

                # Contact nodes
                nb_contact_elements = int(lignes[actual_ligne].strip())
                actual_ligne += 1

                actual_ligne += nb_contact_elements

                nb_code_elements = int(lignes[actual_ligne].strip())
                actual_ligne += 1

                actual_ligne += nb_code_elements
                
                # Temps
                ligne_temps = lignes[actual_ligne].strip()
                if ligne_temps:
                    try:
                        neu.t_time = float(ligne_temps.replace('D', 'E'))
                        #logger.info(f"Temps : {float(ligne_temps.replace('D', 'E'))}")
                    except ValueError:
                        logger.error(f"Erreur de format pour le temps à la ligne {actual_ligne + 1}.")
                else:
                    logger.error(f"Aucune donnée de temps trouvée à la ligne {actual_ligne + 1}.")

                t2 = time.time()
                logger.info(f"GRAPHICS : Temps de traitement du fichier : {t2 - t1:.2f} secondes")
                return neu

        except FileNotFoundError:
            logger.error(f"Erreur : Le fichier '{nom_fichier}' est introuvable.")
        except Exception as e:
            logger.error(f"Une erreur est survenue : {e}")