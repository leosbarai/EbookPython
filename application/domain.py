class DataTable:
    """ Representa uma Tabela de dados.

        Essa classe representa uma tabela de dados do portal
        da transparência. Deve ser capaz de validar linhas
        inseridas de acordo com as colunas que possui. As
        linhas inseridas ficam registradas dentro dela.

        Attributes:
        name: Nome da tabela
        columns: [Lista de colunas]
        data: [Lista de dados]
    """

    def __init__(self, name):
        """Construtor

            Args:
            name: Nome da Tabela
        """
        self._name = name
        self._columns = []
        self._references = []
        self._referenced = []
        self._data = []

    def add_column(self, name, kind, description=""):
        column = Column(name, kind, description=description)
        self._columns.append(column)
        return column

    def add_references(self, name, to, on):
        """ Cria uma referencia dessa tabela para uma outra tabela

            Args:
                name: nome da relação
                to: instância da tabela apontada
                on: instância coluna em que existe a relação
        """
        relationship = Relationship(name, self, to, on)
        self._references.append(relationship)

    def add_referenced(self, name, by, on):
        """ Cria uma referência para outra tabela que aponta para essa.

            Args:
                name: nome da relação
                by: instância da tabela que aponta para essa
                on: instância coluna em que existe a relação
        """
        relationship = Relationship(name, by, self, on)
        self._referenced.append(relationship)


class Column:
    """ Representa uma coluna em um DataTable

        Essa classe contém as informações de uma coluna
        e deve validar um dado de acordo com o tipo de
        dado configurado no construtor.

        Attributes:
            name: Nome da Coluna
            king: Tipo do Dado (varchar, bigint, numeric)
            description: Descrição da coluna
    """

    def __init__(self, name, kind, descripton=""):
        """ Construtor:

            Args:
                name: Nome da Coluna
                kind: Tipo do dado (varchar, bigint, numeric)
                description: Descrição da coluna
        """
        self._name = name
        self._kind = kind
        self._description = descripton


class Relationship:
    """ Classe que representa um relacionamento entre DataTables
        Essa classe tem todas as informações que identificam um
        relacionamento entre tabelas. Em qual coluna ele existe,
        de onde vem e pra onde vai.
    """

    def __init__(self, name, _from, to, on):
        """ Construtor

            Args:
                name: Nome
                from: Tabela de onde sai
                to: Tabela pra onde vai
                on: instância de coluna onde existe
        """
        self._name = name
        self._from = _from
        self._to = to
        self._on = on
