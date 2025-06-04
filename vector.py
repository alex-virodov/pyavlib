import numpy as np


def _vector_mul(vector_type, self_v, other):
    if isinstance(other, vector_type):
        raise NotImplementedError(f'vector_type * vector_type with {vector_type=}')
    elif isinstance(other, (int, float, np.int32)):
        return vector_type(*(other * self_v))
    else:
        raise TypeError(f'unsupported operand type {type(other)} for object {other}')

def _vector_sub(vector_type, self, other):
    if isinstance(other, vector_type):
        return vector_type(*(self.v - other.v))
    else:
        raise TypeError(f'unsupported operand type {type(other)} for object {other}')

def _vector_add(vector_type, self, other):
    if isinstance(other, vector_type):
        return vector_type(*(self.v + other.v))
    else:
        raise TypeError(f'unsupported operand type {type(other)} for object {other}')


class Vector2:
    def __init__(self, x=0.0, y=0.0):
        self.v = np.array([x, y])

    @property
    def x(self) -> float:
        return self.v[0]

    @property
    def y(self) -> float:
        return self.v[1]

    @x.setter
    def x(self, value):
        self.v[0] = value

    @y.setter
    def y(self, value):
        self.v[1] = value

    def __getitem__(self, i):
        return self.v[i]

    def __mul__(self, other):
        return _vector_mul(Vector2, self.v, other)

    def __add__(self, other):
        return _vector_add(Vector2, self, other)

    def __sub__(self, other):
        return _vector_sub(Vector2, self, other)

    def __str__(self):
        return str(self.v)

    def __repr__(self):
        return 'Vector2(' + str(self.v) + ')'

    def cross2(self, other):
        # https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect/565282#565282
        return self.v[0] * other.v[1] - self.v[1] * other.v[0]


class Vector3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.v = np.array([x, y, z])

    @property
    def x(self) -> float:
        return self.v[0]

    @property
    def y(self) -> float:
        return self.v[1]

    @property
    def z(self) -> float:
        return self.v[2]

    @x.setter
    def x(self, value):
        self.v[0] = value

    @y.setter
    def y(self, value):
        self.v[1] = value

    @z.setter
    def z(self, value):
        self.v[2] = value

    @property
    def xy(self):
        return Vector2(self.v[0], self.v[1])

    @property
    def xz(self):
        return Vector2(self.v[0], self.v[2])

    def __getitem__(self, i):
        return self.v[i]

    def __mul__(self, other):
        return _vector_mul(Vector3, self.v, other)

    def __add__(self, other):
        return _vector_add(Vector3, self, other)

    def __sub__(self, other):
        return _vector_sub(Vector3, self, other)

    def __str__(self):
        return str(self.v)

    def __repr__(self):
        return 'Vector3(' + str(self.v) + ')'


class Vector4:
    def __init__(self, x=0, y=0, z=0, w=1):
        self.v = np.array([x, y, z, w])

    @property
    def x(self):
        return self.v[0]

    @property
    def y(self):
        return self.v[1]

    @property
    def z(self):
        return self.v[2]

    @property
    def w(self):
        return self.v[3]

    def dot(self, other):
        return np.dot(self.v, other.v)

    def __str__(self):
        return str(self.v)

    def __repr__(self):
        return 'Vector4(' + str(self.v) + ')'

    def __getitem__(self, i):
        return self.v[i]

    def __mul__(self, other):
        return _vector_mul(Vector4, self.v, other)

    def __add__(self, other):
        return _vector_add(Vector4, self, other)

    def __sub__(self, other):
        return _vector_sub(Vector4, self, other)

    def normalize(self):
        v_result = Vector4()
        v_result.v = self.v / np.linalg.norm(self.v)
        return v_result

    def homogenize(self):
        v_result = Vector4()
        v_result.v = self.v / self.w
        return v_result

    def cross(self, other):
        print(f'cross={np.cross([self.x, self.y, self.z], [other.x, other.y, other.z])}')
        cross = np.cross([self.x, self.y, self.z], [other.x, other.y, other.z])
        return Vector4(cross[0], cross[1], cross[2], 0)
