"""
Utilities for testing the dump_to_neo4j management command
"""
from __future__ import unicode_literals

from py2neo import Node


class MockGraph(object):
    """
    A stubbed out version of py2neo's Graph object, used for testing
    """
    def __init__(self, **kwargs):
        self.nodes = set()
        self.number_commits = 0
        self.number_rollbacks = 0

    def begin(self):
        """
        :return: a MockTransaction object (instead of a py2neo Transaction)
        """
        return MockTransaction(self)


class MockTransaction(object):
    """
    A stubbed out version of py2neo's Transaction object, used for testing.
    """
    def __init__(self, graph):
        self.temp = set()
        self.graph = graph

    def run(self, query):
        """
        Deletes all nodes associated with a course. Normally `run` executes
        an arbitrary query, but in our code, we only use it to delete nodes
        associated with a course.
        :param query: query string to be executed (in this case, to delete all
         nodes associated with a course)
        """
        start_string = "WHERE n.course_key='"
        start = query.index(start_string) + len(start_string)
        query = query[start:]
        end = query.find("'")
        course_key = query[:end]

        self.graph.nodes = set([
            node for node in self.graph.nodes if node['course_key'] != course_key
        ])

    def create(self, element):
        """
        Adds elements to the transaction's temporary backend storage
        :param element: a py2neo Node object
        """
        if isinstance(element, Node):
            self.temp.add(element)

    def commit(self):
        """
        Takes elements in the transaction's temporary storage and adds them
        to the mock graph's storage.
        """
        for element in self.temp:
            self.graph.nodes.add(element)
        self.temp.clear()
        self.graph.number_commits += 1

    def rollback(self):
        """
        Clears the transactions temporary storage
        """
        self.temp.clear()
        self.graph.number_rollbacks += 1


class MockNodeSelector(object):
    """
    Mocks out py2neo's NodeSelector class. Used to select a node from a graph.
    """
    def __init__(self, graph):
        self.graph = graph

    def select(self, label, course_key):
        """
        Selects nodes that match a label and course_key
        :param label: the string of the label we're selecting nodes by
        :param course_key: the string of the course key we're selecting node by
        :return: a MockResult of matching nodes
        """
        nodes = []
        for node in self.graph.nodes:
            if node.has_label(label) and node["course_key"] == course_key:
                nodes.append(node)
        return MockNodeSelection(nodes)


class MockNodeSelection(list):
    """
    Mocks out py2neo's NodeSelection class: this is the type of what
    MockNodeSelector's `select` method returns.
    """
    def first(self):
        """
        :return: the first element of a list if the list has elements.
        Otherwise, None.
        """
        return self[0] if self else None
