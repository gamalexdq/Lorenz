import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QOpenGLWidget
from PyQt5.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLU import *

class LorenzAttractorWidget(QOpenGLWidget):
    def __init__(self):
        super(LorenzAttractorWidget, self).__init__()
        # Configurar la ventana para que sea transparente y sin bordes
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        
        # Generar los datos del atractor de Lorenz
        self.generate_data()
        self.timer_interval = 16  # Intervalo del temporizador en milisegundos (aprox. 60 FPS)
        self.startTimer(self.timer_interval)

    def generate_data(self):
        # Parámetros del Atractor de Lorenz
        sigma = 10.0
        rho = 28.0
        beta = 8.0 / 3.0

        dt = 0.01
        num_steps = 10000

        self.x = np.empty(num_steps)
        self.y = np.empty(num_steps)
        self.z = np.empty(num_steps)

        # Condiciones iniciales
        self.x[0], self.y[0], self.z[0] = (0., 1., 1.05)

        # Integrar las ecuaciones de Lorenz
        for i in range(1, num_steps):
            dx = sigma * (self.y[i-1] - self.x[i-1])
            dy = self.x[i-1] * (rho - self.z[i-1]) - self.y[i-1]
            dz = self.x[i-1] * self.y[i-1] - beta * self.z[i-1]
            self.x[i] = self.x[i-1] + dx * dt
            self.y[i] = self.y[i-1] + dy * dt
            self.z[i] = self.z[i-1] + dz * dt

        self.num_steps = num_steps
        self.current_step = 0

        # Calcular los límites para centrar la vista
        self.xmin, self.xmax = self.x.min(), self.x.max()
        self.ymin, self.ymax = self.y.min(), self.y.max()
        self.zmin, self.zmax = self.z.min(), self.z.max()

        self.x_center = (self.xmin + self.xmax) / 2
        self.y_center = (self.ymin + self.ymax) / 2
        self.z_center = (self.zmin + self.zmax) / 2

        self.max_range = max(self.xmax - self.xmin, self.ymax - self.ymin, self.zmax - self.zmin)

    def initializeGL(self):
        glClearColor(0, 0, 0, 0)  # Establecer el color de limpieza a transparente
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_DEPTH_TEST)
        glLineWidth(2)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = w / h if h != 0 else 1
        gluPerspective(45, aspect, 1, 1000)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        # Configurar la cámara
        eye_distance = self.max_range * 1.5
        gluLookAt(self.x_center, self.y_center, eye_distance,
                  self.x_center, self.y_center, self.z_center,
                  0, 1, 0)
        
        glColor3f(1.0, 1.0, 1.0)

        # Dibujar el atractor de Lorenz hasta el paso actual
        glBegin(GL_LINE_STRIP)
        for i in range(self.current_step):
            glVertex3f(self.x[i], self.y[i], self.z[i])
        glEnd()

        # Actualizar el paso actual
        self.current_step += 10  # Controla la velocidad de la animación
        if self.current_step >= self.num_steps:
            self.current_step = 0

    def timerEvent(self, event):
        self.update()

    # Opcional: métodos para mover la ventana al arrastrar con el ratón
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LorenzAttractorWidget()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())
