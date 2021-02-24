import unittest


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

    def _get_name(self):
        print("Getter executado!")
        return self._name

    def _set_name(self, _name):
        print("Setter executado!")
        self._name = _name

    def _del_name(self):
        print("Deletter executado!")
        raise AttributeError("Não pode deletar esse atributo.")

    name = property(_get_name, _set_name, _del_name)

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


from decimal import Decimal


class Column:
    """ Representa uma coluna em um DataTable

        Essa classe contém as informações de uma coluna
        e deve validar um dado de acordo com o tipo de
        dado configurado no construtor.

        Attributes:
            name: Nome da Coluna
            kind: Tipo do Dado (varchar, bigint, numeric)
            description: Descrição da coluna
    """

    def __init__(self, name, kind, description=""):
        """ Construtor:

            Args:
                name: Nome da Coluna
                kind: Tipo do dado (varchar, bigint, numeric)
                description: Descrição da coluna
        """
        self._name = name
        self._kind = kind
        self._description = description

    @staticmethod
    def validate(kind, data):
        if kind == 'bigint':
            if isinstance(data, int):
                return True
            return False
        elif kind == 'varchar':
            if isinstance(data, str):
                return True
            return False
        elif kind == 'numeric':
            try:
                val = Decimal(data)
            except:
                return False
            return True

    
class ColumnTest(unittest.TestCase):
    def test_validate_bigint(self):
        self.assertTrue(Column.validate('bigint', 100))
        self.assertTrue(not Column.validate('bigint', 10.1))
        self.assertTrue(not Column.validate('bigint', 'Texto'))

    def test_validate_numeric(self):
        self.assertTrue(Column.validate('numeric', 10.1))
        self.assertTrue(Column.validate('numeric', 100))
        self.assertTrue(not Column.validate('numeric', 'Texto'))

    def test_validate_varchar(self):
        self.assertTrue(Column.validate('varchar', 'Texto'))
        self.assertTrue(not Column.validate('varchar', 100))
        self.assertTrue(not Column.validate('varchar', 10.1))


if __name__ == "__main__":
    unittest.main()


class PrimaryKey(Column):
    def __init__(self, table, name, kind, description=""):
        super().__init__(name, kind, description=description)
        self._is_pk = True

    def __str__(self):
        _str = "Col: {} : {} {}".format(self._name,
                                        self._kind,
                                        self._description)

        return "{} - {}".format('PK', _str)


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


# coding: utf-8

import os


def extract_name(name):
    return name.split(".")[0]


def read_lines(filename):
    _file = open(os.path.join("data/meta-data", filename), "rt")
    data = _file.read().split("\n")
    _file.close()
    return data


def read_metadata(filename):
    metadata = []
    for column in read_lines(filename):
        if column:
            metadata.append(tuple(column.split('\t')[:3]))
    return metadata


def prompt():
    print("\nO que deseja ver?")
    print("(l) Listar entidades")
    print("(d) Exibir atributos de uma entidade")
    print("(r) Exibir referências de uma entidade")
    print("(s) Sair do programa")
    return input('')


def main():
    # dicionário nome entidade -> atributos
    meta = {}
    # dicionário identificador -> nome entidade
    keys = {}
    # dicionário de relacionamentos

    relationships = {}
    for meta_data_file in os.listdir("data/meta-data"):
        table_name = extract_name(meta_data_file)
        attributes = read_metadata(meta_data_file)
        identifier = attributes[0][0]

        meta[table_name] = attributes
        keys[identifier] = table_name

    for key, val in meta.items():
        for col in val:
            if col[0] in keys:
                if not col[0] == meta[key][0][0]:
                    relationships[key] = keys[col[0]]

    opcao = prompt()
    while opcao != 's':
        if opcao == 'l':
            for entity_name in meta.keys():
                print(entity_name)
        elif opcao == 'd':
            entity_name = input('Nome da entidade: ')
            for col in meta[entity_name]:
                print(col)
        elif opcao == 'r':
            entity_name = input('Nome da entidade: ')
            other_entity = relationships[entity_name]
            print(other_entity)
        else:
            print("Inexistente\n")
        opcao = prompt()


if __name__ == '__main__':
    main()
