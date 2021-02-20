from itertools import combinations


class Node:
    """
    The class creates Node object with data and children and the main methods
    are getters and setters.
    """
    def __init__(self, data, positive_child=None, negative_child=None):
        """
        A constructor for a Node object
        :param data: A string of the node
        :param positive_child: Node object
        :param negative_child: Node object
        """
        self.data = data
        self.positive_child = positive_child
        self.negative_child = negative_child

    def get_data(self):
        """
        :return: object data
        """
        return self.data

    def get_positive_child(self):
        """
        :return: object positive child (node object)
        """
        return self.positive_child

    def get_negative_child(self):
        """
        :return: object negative child (node object)
        """
        return self.negative_child

    def set_positive_child(self, node):
        """
        The method updates positive_child
        :param node: positive_child object
        """
        self.positive_child = node

    def set_negative_child(self, node):
        """
        The method updates negative_child
        :param node: negative_child object
        """
        self.negative_child = node


class Record:
    """
    The class creates Record object with illness and it symptoms and the main
    methods are getters.
    """
    def __init__(self, illness, symptoms):
        """
        A constructor for a Record object
        :param illness: illness as string
        :param symptoms: symptoms as list
        """
        self.illness = illness
        self.symptoms = symptoms

    def get_illness(self):
        """
        :return: illness
        """
        return self.illness

    def get_symptoms(self):
        """
        :return: symptoms
        """
        return self.symptoms


def parse_data(filepath):
    with open(filepath) as data_file:
        records = []
        for line in data_file:
            words = line.strip().split()
            records.append(Record(words[0], words[1:]))
        return records


def update_path(path, flag):
    """General function to return new list with the flag appended"""
    new_path = path[:]
    new_path.append(flag)
    return new_path


class Diagnoser:
    """
    The class creates Diagnoser object as a tree. The main methods are to find
    diagnose by symptoms, find all illnesses and paths.
    """
    def __init__(self, root):
        """
        A constructor for the tree
        :param root: root of the tree
        """
        self.root = root

    def diagnose(self, symptoms):
        """
        The method check recursively which illness diagnosed by those symptoms
        :param symptoms: symptoms to search the right illness, as list
        :return: illness
        """
        if not self.root.get_positive_child():
            return self.root.get_data()
        if self.root.get_data() in symptoms:
            d = Diagnoser(self.root.get_positive_child())
            return d.diagnose(symptoms)
        else:
            d = Diagnoser(self.root.get_negative_child())
            return d.diagnose(symptoms)

    def calculate_success_rate(self, records):
        """
        The method calculates the successful rate by counting each illness in
        the records which diagnosed
        :param records: list of record objects
        :return: the rate
        """
        count = 0
        for record in records:
            illness = record.get_illness()
            symptoms = record.get_symptoms()
            if self.diagnose(symptoms) == illness:
                count += 1
        return count / len(records)

    def _all_illnesses_helper(self, lst):
        """
        The method go over the tree leaves and add them to the list
        :param lst: result list of all illnesses
        :return: the list after added all leaves (illnesses)
        """
        if not self.root.get_positive_child():
            lst.append(self.root.get_data())
            return lst
        positive_diagnoser = Diagnoser(self.root.get_positive_child())
        negative_diagnoser = Diagnoser(self.root.get_negative_child())
        lst = positive_diagnoser._all_illnesses_helper(lst)
        lst = negative_diagnoser._all_illnesses_helper(lst)
        return lst

    def set_list(self, lst):
        """
        The method remove duplicates and keep the order of the original list
        :param lst: list to change
        :return: new list without duplicates
        """
        new_list = []
        for item in lst:
            if item not in new_list:
                new_list.append(item)
        return new_list

    def all_illnesses(self):
        """
        The method get all illnesses by helper function and order them by their
        count and return the list without duplicates
        :return: a list of all illnesses
        """
        lst = self._all_illnesses_helper([])
        lst = list(sorted(lst, key=lambda x: lst.count(x), reverse=True))
        return self.set_list(lst)

    def _paths_to_illness_helper(self, illness, path, lst):
        """
        The method find paths to an illness
        :param illness: illness to find
        :param path: current path
        :param lst: result list - add the path if the illness found
        :return: the list
        """
        if not self.root.get_positive_child():
            if self.root.get_data() == illness:
                lst.append(path)
            return lst
        positive_diagnoser = Diagnoser(self.root.get_positive_child())
        negative_diagnoser = Diagnoser(self.root.get_negative_child())
        lst = positive_diagnoser._paths_to_illness_helper(illness,
                                                          update_path(path, True),
                                                          lst)
        lst = negative_diagnoser._paths_to_illness_helper(illness,
                                                          update_path(path, False),
                                                          lst)
        return lst

    def paths_to_illness(self, illness):
        """
        The method returns the paths to the illness by using helper function
        :param illness: illness to find
        :return: list of paths
        """
        return self._paths_to_illness_helper(illness, [], [])


def build_tree_helper(symptoms, root, records):
    """
    The method bulid tree decision of symptoms and at the end it adds the most
    relevant illness from records
    :param symptoms: list of symptoms to create the tree
    :param root: current root to create its children
    :param records: list of record object to decide at the end which illness to
    add
    :return: nothing. the function just create the tree (the original root
    already saved
    """
    if symptoms:
        child_data = symptoms[0]
        negative_child = Node(child_data)
        positive_child = Node(child_data)
        root.set_negative_child(negative_child)
        root.set_positive_child(positive_child)
        build_tree_helper(symptoms[1:], negative_child, bad_symptom(records,
                                                                    root.get_data()))
        build_tree_helper(symptoms[1:], positive_child, good_symptom(records,
                                                                     root.get_data()))
    else:
        positive_illness_dict = {}
        negative_illness_dict = {}
        for record in records:
            if root.get_data() in record.get_symptoms():
                update_dict(record.get_illness(), positive_illness_dict)
            else:
                update_dict(record.get_illness(), negative_illness_dict)
        illness_node = node_to_update(positive_illness_dict)
        root.set_positive_child(illness_node)
        illness_node = node_to_update(negative_illness_dict)
        root.set_negative_child(illness_node)


def update_dict(illness, dct):
    """
    The function update dictionary counting - if exists add 1, else create the
    key with 1 value
    :param illness: key of the dictionary
    :param dct: dictionary
    :return: nothing - the dictionary is mutable
    """
    if illness not in dct:
        dct[illness] = 1
    else:
        dct[illness] += 1


def node_to_update(dct):
    """
    The function creates Node of the first illness in the dictionary with the
    max value
    :param dct: illnesses dictionary
    :return: Node of illness - or None Node if not found
    """
    for key in dct:
        if dct[key] == max(dct.values()):
            illness = Node(key)
            return illness
    return Node(None)


def bad_symptom(records, symptom):
    """
    The function creates new records list by adding only those without the bad
    symptom
    :param records: list of record objects
    :param symptom: bad symptom
    :return: new records list
    """
    new_list = []
    for record in records:
        if symptom not in record.get_symptoms():
            new_list.append(record)
    return new_list


def good_symptom(records, symptom):
    """
    The function creates new records list by adding only those with the good
    symptom
    :param records: list of record objects
    :param symptom: good symptom
    :return: new records list
    """
    new_list = []
    for record in records:
        if symptom in record.get_symptoms():
            new_list.append(record)
    return new_list


def build_tree(records, symptoms):
    """
    The function build the tree using helper function and returns the root
    :param records: list of record objects
    :param symptoms: list of symptoms
    :return: root of the tree
    """
    if symptoms:
        root = Node(symptoms[0])
        build_tree_helper(symptoms[1:], root, records)
    else:
        if not records:
            root = Node(None)
        else:
            illness_dict = {}
            for record in records:
                update_dict(record.get_illness(), illness_dict)
            root = Node(max(illness_dict, key=lambda x: illness_dict[x]))
    return root


def optimal_tree(records, symptoms, depth):
    """
    The function calculates which tree has the best rate of symptoms
    combinations in size of depth. It returns the root of that tree
    :param records: list of record objects
    :param symptoms: list of symptoms
    :param depth: size of group combinations (of symptoms)
    :return: root of the best tree
    """
    max_rate = -1
    root = Node(None)
    if records:
        for group in list(combinations(symptoms, depth)):
            temp_root = build_tree(records, group)
            diagnoser_group = Diagnoser(temp_root)
            rate = diagnoser_group.calculate_success_rate(records)
            if rate > max_rate:
                root = temp_root
                max_rate = rate
    return root
