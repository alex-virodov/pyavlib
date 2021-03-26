import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R
import numpy as np

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

    def __mul__(self, other):
        if isinstance(other, Vector4):
            raise NotImplementedError('Vector4 * Vector4')
        elif isinstance(other, (int, float, np.int32)):
            v_result = Vector4()
            v_result.v = other * self.v
            return v_result
        else:
            raise TypeError(f'unsupported operand type {type(other)} for object {other}')

    def __sub__(self, other):
        if isinstance(other, Vector4):
            v_result = Vector4()
            v_result.v = self.v - other.v
            return v_result
        else:
            raise TypeError(f'unsupported operand type {type(other)} for object {other}')
    def __add__(self, other):
        if isinstance(other, Vector4):
            v_result = Vector4()
            v_result.v = self.v + other.v
            return v_result
        else:
            raise TypeError(f'unsupported operand type {type(other)} for object {other}')

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

class Matrix4:
    def __init__(self, values=None):
        self.mtx = np.eye(4)
        if values is not None:
            values_mtx = np.array(values)
            if values_mtx.shape[0] < 4 and values_mtx.shape[1] < 4:
                self.mtx[0:values_mtx.shape[0], 0:values_mtx.shape[1]] = values_mtx
            else:
                self.mtx = values_mtx
            #print(f'shape={self.mtx.shape} values={values} mtx=\n{self.mtx}')
            assert self.mtx.shape == (4, 4)

    def euler_rotate(self, ex, ey, ez):
        m_rotate_x = Matrix4(R.from_euler('x', ex, degrees=True).as_matrix())
        m_rotate_y = Matrix4(R.from_euler('y', ey, degrees=True).as_matrix())
        m_rotate_z = Matrix4(R.from_euler('z', ez, degrees=True).as_matrix())
        return m_rotate_z * m_rotate_y * m_rotate_x * self

    def translate(self, x, y, z):
        m_translate = Matrix4()
        m_translate.mtx[0, 3] = x
        m_translate.mtx[1, 3] = y
        m_translate.mtx[2, 3] = z
        return m_translate * self

    def __mul__(self, other):
        if isinstance(other, Vector4):
            v_result = np.dot(self.mtx, other.v)
            return Vector4(v_result[0], v_result[1], v_result[2], v_result[3])
        elif isinstance(other, Matrix4):
            m_result = np.dot(self.mtx, other.mtx)
            return Matrix4(m_result)
        else:
            raise TypeError(f'unsupported operand type {type(other)} for object {other}')

    def invert(self):
        return Matrix4(np.linalg.inv(self.mtx))

def plot_vector(ax, v, color):
    ax.plot([0, v.x], [0, v.y], [0, v.z], color)

def plot_line(ax, v1, v2, color):
    ax.plot([v1.x, v2.x], [v1.y, v2.y], [v1.z, v2.z], color)

def plot_axes(ax, m, style=''):
    plot_vector(ax, m * Vector4(1, 0, 0), 'r' + style)
    plot_vector(ax, m * Vector4(0, 1, 0), 'g' + style)
    plot_vector(ax, m * Vector4(0, 0, 1), 'b' + style)

def plot_frustrum(ax, m, fovx, fovy, color):
    ccenter = Vector4(0, 0, 0)
    cfwd = Vector4(0, 0, -1)
    c00 = m * Matrix4().euler_rotate(0, fovy, fovx) * cfwd
    c01 = m * Matrix4().euler_rotate(0, fovy, -fovx) * cfwd
    c10 = m * Matrix4().euler_rotate(0, -fovy, fovx) * cfwd
    c11 = m * Matrix4().euler_rotate(0, -fovy, -fovx) * cfwd
    cfwd = m * cfwd
    ccenter = m * ccenter
    plot_line(ax, ccenter, cfwd, color + '--')
    plot_line(ax, ccenter, c00, color)
    plot_line(ax, ccenter, c01, color)
    plot_line(ax, ccenter, c10, color)
    plot_line(ax, ccenter, c11, color)
    plot_line(ax, c00, c01, color)
    plot_line(ax, c01, c10, color)
    plot_line(ax, c11, c10, color)
    plot_line(ax, c11, c00, color)
    return (cfwd, ccenter, c00, c01, c10, c11)

def plot_plane(ax, v_center, v_normal, step, steps, color):
    # Find first non-collinear (in loose sense) vector to normal. That will be the tangent (after orthonormalization).
    v_normal = Vector4(v_normal.x, v_normal.y, v_normal.z, 0).normalize()
    v_tangent = Vector4(1, 0, 0, 0)
    if (v_tangent.dot(v_normal) > 0.8):
        v_tangent = Vector4(0, 1, 0, 0)
    if (v_tangent.dot(v_normal) > 0.8):
        v_tangent = Vector4(0, 0, 1, 0)
    if (v_tangent.dot(v_normal) > 0.8):
        raise ValueError(f'failed to build v_tangent vector to normal {v_normal}')
    print(f'pre-orthonormalization normal={v_normal} v_tangent={v_tangent}')
    v_tangent = (v_tangent - v_normal * v_tangent.dot(v_normal)).normalize()
    v_bitangent = v_normal.cross(v_tangent)
    print(f'post-orthonormalization normal={v_normal} v_tangent={v_tangent} v_bitangent={v_bitangent}')
    for i in np.arange(-steps, steps+1):
        line_start = v_center + v_tangent * (step * steps) + v_bitangent * (step * i)
        line_end   = v_center + v_tangent * (step * -steps) + v_bitangent * (step * i)
        plot_line(ax, line_start, line_end, color)
        line_start = v_center + v_bitangent * (step * steps) + v_tangent * (step * i)
        line_end   = v_center + v_bitangent * (step * -steps) + v_tangent * (step * i)
        plot_line(ax, line_start, line_end, color)
