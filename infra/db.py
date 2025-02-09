import json

from model.Usuario import Usuario
from model.Personagem import Personagem
from model.Monstro import Monstro
from model.Mesa import Mesa

def encoder(obj):
    if isinstance(obj, Usuario):
        return obj.__dict__()
    if isinstance(obj, Mesa):
        return {
            'uid': obj.uid,
            'nome': obj.nome,
            'personagens': [personagem.__dict__() for personagem in obj.personagens or []],
            'descricao': obj.descricao,
            'mestre': obj.mestre.__dict__(),
            'monstros': [monstro.__dict__() for monstro in obj.monstros or []]
        }

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    data = {}

    def __init__(self):
        with open("./infra/db.json", 'r') as db:
            loaded = json.load(db)
            loaded['usuarios'] = [Usuario(**usuario) for usuario in loaded.get('usuarios', [])]
            mesas = []

            for mesa in loaded.get('mesas', []):
                mesa['mestre'] = Usuario(**mesa['mestre'])

                pers = []
                for personagem in mesa.get('personagens', []):
                    personagem['usuario'] = Usuario(**personagem['usuario'])
                    pers.append(Personagem(**personagem))
                mesa['personagens'] = pers

                mesa['monstros'] = [Monstro(**monstro) for monstro in mesa.get('monstros', [])]

                mesas.append(Mesa(**mesa))

            loaded['mesas'] = mesas
            self.data = loaded
        print(self.data)

    def dump_db(self):
        with open("./infra/db.json", "w") as db:
            json.dump(self.data, db, default=encoder)

    def add(self, obj, array_key):
        if array_key not in self.data:
            self.data[array_key] = []
            obj.uid = 1
        else:
            self.data[array_key].sort(key=lambda x: x.uid)
            obj.uid = self.data[array_key][-1].uid + 1
            self.data[array_key].append(obj)
            self.dump_db()

    def update(self, obj, array_key):
        if array_key not in self.data:
            return False

        for i, item in enumerate(self.data[array_key]):
            if item.uid == obj.uid:
                self.data[array_key][i] = obj
                self.dump_db()
                return True

        return False

    def delete(self, obj, array_key):
        if array_key not in self.data:
            return False

        for i, item in enumerate(self.data[array_key]):
            if item.uid == obj.uid:
                self.data[array_key].pop(i)
                self.dump_db()
                return True

        return False

    def get_all(self, array_key):
        return self.data.get(array_key, [])

    def get_by_uid(self, uid, array_key):
        for item in self.data.get(array_key, []):
            if item.uid == uid:
                return item

        return None